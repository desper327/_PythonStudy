# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateHairHierarchyRules(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.1
    label = '验证：毛发层级规则'

    def process(self, **kwargs):
        if not cmds.objExists('hairFxNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

        self.hdict = {
            "node": {
                "hierarchy": "hairNodeNUL",
                "objects": []
            },
            "hairSystem": {
                "hierarchy": "hairSystemNUL",
                "objects": []
            },
            "follicle": {
                "hierarchy": "hairFollicleNUL",
                "objects": []
            },
            "nurbsCurve": {
                "hierarchy": "hairCurveNUL",
                "objects": []
            }
        }
        # hairNodeNUL
        nodes = cmds.ls(type=['xgmPalette'], l=1)
        for i in nodes:
            if '|cfxNUL|fx2NUL|hairFxNUL|hairNodeNUL|' not in i:
                self.hdict['node']['objects'].append(i)
        if self.hdict['node']['objects']:
            raise ValueError("xgmPalette节点存放错误.\n"
                             "xgmPalette节点应存放至['clothNodeNUL']总组下.\n"
                             "单击['repair']按钮完成自动修复.")

        # hairSystemNUL
        hairSystems = cmds.ls(type=['hairSystem', 'nucleus'], l=1)
        for i in hairSystems:
            h = None
            if cmds.nodeType(i) == 'hairSystem':
                h = cmds.listRelatives(i, p=1, f=1)[0]
            elif cmds.nodeType(i) == 'nucleus':
                nucleus = cmds.listConnections(i, type='hairSystem', s=0)
                if nucleus:
                    h = cmds.ls(i, l=1)[0]
            if h:
                if '|cfxNUL|fx2NUL|hairFxNUL|hairSystemNUL|' not in i:
                    self.hdict['hairSystem']['objects'].append(i)
        if self.hdict['hairSystem']['objects']:
            raise ValueError("hairSystem节点存放错误.\n"
                             "hairSystem节点应存放至['hairSystemNUL']总组下.\n"
                             "单击['repair']按钮完成自动修复.")

        # hairFollicleNUL
        follicles = cmds.ls(type=['follicle'], l=1)
        transform = []
        for i in follicles:
            if cmds.nodeType(i) == 'follicle':
                name = i.rsplit('|', 2)[0]
                if name == '':
                    name = i.rsplit('|', 1)[0]
                transform.append(name)
        for i in list(set(transform)):
            if '|cfxNUL|fx2NUL|hairFxNUL|hairFollicleNUL' not in i:
                self.hdict['follicle']['objects'].append(i)
        if self.hdict['follicle']['objects']:
            raise ValueError("输入铆钉平行组存放错误.\n"
                             "输入铆钉平行组应存放至['hairFollicleNUL']总组下.\n"
                             "单击['repair']按钮完成自动修复.")

        # hairCurveNUL
        follicles = cmds.ls(type=['follicle'], l=1)
        transform = []
        for i in follicles:
            curve = cmds.listConnections(i, type='nurbsCurve', s=0)
            if curve:
                crvLong = cmds.ls(curve[0], l=1)
                name = crvLong[0].rsplit('|', 1)[0]
                if name == '':
                    name = crvLong[0]
                transform.append(name)
        for i in list(set(transform)):
            if '|cfxNUL|fx2NUL|hairFxNUL|hairCurveNUL' not in i:
                self.hdict['nurbsCurve']['objects'].append(i)
        if self.hdict['nurbsCurve']['objects']:
            raise ValueError("输出曲线平行组存放错误.\n"
                             "输出曲线平行组应存放至['hairCurveNUL']总组下.\n"
                             "单击['repair']按钮完成自动修复.")

    def repair(self, args):
        for vdict in self.hdict.values():
            k = vdict['hierarchy']
            v = vdict['objects']
            if v:
                for i in v:
                    cmds.parent(i, k)