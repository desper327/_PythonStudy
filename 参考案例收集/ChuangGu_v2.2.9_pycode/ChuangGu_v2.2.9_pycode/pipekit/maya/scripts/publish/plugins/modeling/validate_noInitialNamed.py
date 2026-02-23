# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoInitialNamed(plugin.Validator):
    """Checks whether any meshes have lambert1 applied.
    """
    label = '验证：没有初始命名'
    actions = ['select']

    def process(self, **kwargs):
        self.error = []
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复.')
        else:
            objs = cmds.ls(type='transform')
            for i in objs:
                if 'polySurface' in i:
                    self.error.append(i)

            if self.error:
                raise RuntimeError("物体禁止以['polySurface']字段命名.\n"
                                   "请艺术家手动对其赋予新的物体命名.")

    def select(self):
        if self.error:
            cmds.select(self.error, r=1)