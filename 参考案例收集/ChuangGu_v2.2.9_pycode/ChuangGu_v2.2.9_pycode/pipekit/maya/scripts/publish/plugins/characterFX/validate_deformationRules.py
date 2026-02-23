# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateDeformationRules(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.4
    label = '验证：变形关联规则'

    def process(self, **kwargs):
        nulls = ['clothNUL', 'hairGrmNUL', 'clothMeshNUL']
        for null in nulls:
            if not cmds.objExists(null):
                raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

        self.ddict = {
            "cloth": {
                "hierarchy": "clothNUL",
                "objects": []
            },
            "hairGrm": {
                "hierarchy": "hairGrmNUL",
                "objects": []
            },
            "clothMesh": {
                "hierarchy": "clothMeshNUL",
                "objects": []
            }
        }
        # clothNUL
        cloths = cmds.filterExpand('clothNUL', ex=1, sm=12)
        if cloths:
            for mesh in cloths:
                hist = cmds.listHistory(mesh, pdo=1, il=1)
                mSs = cmds.ls(hist, type=['blendShape'])
                if mSs:
                    self.ddict['cloth']['objects'].append(mesh)
            if self.ddict['cloth']['objects']:
                raise ValueError("['clothNUL']总组下禁止出现融合节点.\n"
                                 "单击['repair']按钮完成自动修复.")

        # hairGrmNUL
        hairGrms = cmds.filterExpand('hairGrmNUL', ex=1, sm=12)
        if hairGrms:
            wrap = []
            for mesh in hairGrms:
                hist = cmds.listHistory(mesh, pdo=1, il=1)
                mSs = cmds.ls(hist, type=['wrap'])
                if mSs:
                    wrap.extend(mSs)
            if wrap:
                wrap = list(set(wrap))
                self.ddict['hairGrm']['objects'].extend(wrap)
                raise ValueError("['hairGrmNUL']总组下禁止出现包裹节点.\n"
                                 "单击['repair']按钮完成自动修复.")

        # clothMeshNUL
        clothMeshes = cmds.filterExpand('clothMeshNUL', ex=1, sm=12)
        if clothMeshes:
            for mesh in clothMeshes:
                hist = cmds.listHistory(mesh, pdo=1, il=1)
                mSs = cmds.ls(hist, type=['wrap'])
                if not mSs:
                    self.ddict['clothMesh']['objects'].append(mesh)
            if self.ddict['clothMesh']['objects']:
                raise ValueError("['clothMeshNUL']总组下每个模型必须存在包裹节点.\n"
                                 "单击['repair']按钮选择未添加包裹节点的模型.")

    def repair(self, args):
        for k, v in self.ddict.items():
            objects = v['objects']
            if k in ['cloth']:
                if objects:
                    cmds.delete(objects, ch=1)
            elif k in ['hairGrm']:
                if objects:
                    cmds.delete(objects)
            else:
                if objects:
                    cmds.select(objects, r=1)