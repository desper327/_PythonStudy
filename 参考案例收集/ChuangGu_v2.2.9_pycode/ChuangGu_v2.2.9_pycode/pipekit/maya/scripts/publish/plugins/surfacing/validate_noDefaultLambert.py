# -*- coding: utf-8 -*-

from publish import plugin
import maya.cmds as cmds


class ValidateNoDefaultLambert(plugin.Validator):
    ''' Check there are no mesh items with default "Lambert1" '''
    label = '验证：没有默认材质球'
    actions = ['select']

    def process(self, **kwargs):
        self.error = []
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复.')
        else:
            meshes = cmds.filterExpand('Geometry', ex=1, sm=12)
            if not meshes:
                null = ['aniNUL', 'srfNUL', 'simNUL']
                raise ValueError('Geometry总组下未找到任何模型,请将模型存放至 {} 对应组内.'.format(null))

            self.error = cmds.listConnections('initialShadingGroup.dagSetMembers', source=True, destination=False)
            if self.error:
                raise RuntimeError('模型禁止添加lambert1材质球: {}'.format(self.error))

    def select(self):
        cmds.select(self.error)