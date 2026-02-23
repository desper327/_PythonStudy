# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectNoFrameHierarchy(plugin.MayaCollector):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.MayaCollector.order + 0.5
    label = '收集：没有多余平行组'
    ignoreType = ['shots', 'asm']
    actions = ['select']

    def process(self, **kwargs):
        category = kwargs['category']
        abbr = kwargs['department']

        if abbr == 'mod':
            null = 'Geometry'
        elif abbr == 'rig':
            null = 'Group'
        elif abbr == 'cfx':
            null = 'cfxNUL'
        elif abbr == 'srf':
            if category in ['set']:
                null = 'Group'
            else:
                null = 'Geometry'

        self.error = []
        assemblies = cmds.ls(assemblies=1)
        for i in assemblies:
            if i not in ['persp', 'top', 'front', 'side']:
                if i == null:
                    pass
                else:
                    self.error.append(i)

        if cmds.objExists(null):
            if self.error:
                raise ValueError('大纲内禁止出现多余平行组: {0} ,只能存在 {1} 总组其它多余平行组请手动整理.'.format(self.error, [null]))
        else:
            raise ValueError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

    def select(self):
        if self.error:
            cmds.select(self.error, r=1)
