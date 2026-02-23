# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateClothHierarchyRules(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.2
    label = '验证：布料层级规则'

    def process(self, **kwargs):
        if not cmds.objExists('clothFxNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

        self.cdict = {
            "node": {
                "hierarchy": "clothNodeNUL",
                "objects": []
            },
            "constraint": {
                "hierarchy": "clothConstraintNUL",
                "objects": []
            },
            "collider": {
                "hierarchy": "clothColliderNUL",
                "objects": []
            },
            "wrapBase": {
                "hierarchy": "clothBaseNUL",
                "objects": []
            }
        }
        # clothNodeNUL
        nodes = cmds.ls(type=['nCloth', 'nucleus'], l=1)
        for i in nodes:
            c = None
            if cmds.nodeType(i) == 'nCloth':
                c = cmds.listRelatives(i, p=1, f=1)[0]
            elif cmds.nodeType(i) == 'nucleus':
                nucleus = cmds.listConnections(i, type='nCloth', s=0)
                if nucleus:
                    c = cmds.ls(i, l=1)[0]
            if c:
                if '|cfxNUL|fx2NUL|clothFxNUL|clothNodeNUL|' not in i:
                    self.cdict['node']['objects'].append(i)
        if self.cdict['node']['objects']:
            raise ValueError("布料节点存放错误.\n"
                             "布料和Nucleus节点应存放至['clothNodeNUL']总组下\n"
                             "单击['repair']按钮完成自动修复.")

        # clothConstraintNUL
        constraints = cmds.ls(type=['dynamicConstraint'], l=1)
        for i in constraints:
            if cmds.nodeType(i) == 'dynamicConstraint':
                i = cmds.listRelatives(i, p=1, f=1)[0]
            if '|cfxNUL|fx2NUL|clothFxNUL|clothConstraintNUL|' not in i:
                self.cdict['constraint']['objects'].append(i)
        if self.cdict['constraint']['objects']:
            raise ValueError("约束节点存放错误.\n"
                             "约束节点应存放至['clothConstraintNUL']总组下\n"
                             "单击['repair']按钮完成自动修复.")

        # clothColliderNUL
        colliders = cmds.ls(type=['nRigid'], l=1)
        for i in colliders:
            if cmds.nodeType(i) == 'nRigid':
                i = cmds.listRelatives(i, p=1, f=1)[0]
            if '|cfxNUL|fx2NUL|clothFxNUL|clothColliderNUL|' not in i:
                self.cdict['collider']['objects'].append(i)
        if self.cdict['collider']['objects']:
            raise ValueError("碰撞节点存放错误.\n"
                             "碰撞节点应存放至['clothColliderNUL']总组下\n"
                             "单击['repair']按钮完成自动修复.")

        # clothBaseNUL
        bases = cmds.ls('*Base', l=1)
        for i in bases:
            if cmds.nodeType(i) == 'transform':
                if '|cfxNUL|fx2NUL|clothFxNUL|clothBaseNUL|' not in i:
                    self.cdict['wrapBase']['objects'].append(i)
        if self.cdict['wrapBase']['objects']:
            raise ValueError("包裹节点存放错误.\n"
                             "包裹节点应存放至['clothBaseNUL']总组下\n"
                             "单击['repair']按钮完成自动修复.")

    def repair(self, args):
        for vdict in self.cdict.values():
            k = vdict['hierarchy']
            v = vdict['objects']
            if v:
                for i in v:
                    cmds.parent(i, k)