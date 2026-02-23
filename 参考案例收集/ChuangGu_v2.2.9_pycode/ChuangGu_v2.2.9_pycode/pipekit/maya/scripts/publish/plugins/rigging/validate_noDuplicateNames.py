# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoDuplicateNames(plugin.Validator):
    order = plugin.Validator.order + 0.5
    label = '验证：禁止控制器重名'
    actions = ['select']
    optional = True

    def process(self, **kwargs):
        if not cmds.objExists('Group'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复.')

        self.error = []
        shapes = cmds.ls('Group', type=['nurbsCurve'], dag=1)
        for i in shapes:
            if '|' in i:
                self.error.append(i)

        # 选择错误，执行终止
        if self.error:
            raise RuntimeError('控制器重名错误,单击[select]按钮后请到大纲按F键查阅错误对象.\n'
                               '请手动完成控制器命名修改.')

    def select(self):
        if self.error:
            cmds.select(self.error)
            cmds.pickWalk(d='up')