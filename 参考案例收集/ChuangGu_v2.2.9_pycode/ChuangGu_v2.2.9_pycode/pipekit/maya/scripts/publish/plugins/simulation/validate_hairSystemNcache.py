# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateHairSystemNcache(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.4
    label = '验证：毛发系统nCache缓存'
    optional = True
    actions = ['select']

    def process(self, **kwargs):
        self.miss = []

        # hairNodeNUL/子集个数判断
        nodes = cmds.ls(type=['hairSystem'])
        if nodes:
            for i in nodes:
                cache = i.replace(':', '_') + 'Cache1'
                if not cmds.objExists(cache):
                    self.miss.append(i)

        if self.miss:
            cmds.select(self.miss, r=1)
            raise ValueError("缺失hairSystem的nCache缓存.\n"
                             "单击[select]按钮在大纲按F键后查看缓存丢失对象.\n"
                             "请在[assembly]工具下完成挂在缓存工作.")

    def select(self):
        if self.miss:
            cmds.pickWalk(self.miss, d='up')
            cmds.select(r=1)