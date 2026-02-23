# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoDuplicateNames(plugin.Validator):
    
    label = '验证：物体没有重复名称'
    actions = ['select']

    def process(self, **kwargs):
        if cmds.ls(['*:*', '*:*:*']):
            raise RuntimeError('空间字符错误,请先完成没有参考节点的修复.')

        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复.')

        self.error = []
        transforms = cmds.ls('Geometry', tr=1, dag=1)
        for i in transforms:
            if '|' in i:
                self.error.append(i)

        # 选择错误，执行终止
        if self.error:
            raise RuntimeError('发现重名错误,请到大纲查阅.')

    def select(self):
        if self.error:
            cmds.select(self.error)