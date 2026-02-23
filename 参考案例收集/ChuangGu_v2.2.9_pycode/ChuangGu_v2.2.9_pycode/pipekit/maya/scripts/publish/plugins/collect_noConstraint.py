# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectNoConstraint(plugin.MayaCollector):
    label = '收集：Geometry层级下没有约束节点'
    order = plugin.MayaCollector.order + 1.0
    actions = ['select']
    ignoreType = ['asm', 'cfx', 'shots']

    def getInvalid(self):
        constraints = cmds.listRelatives('Geometry', ad=1, type=['parentConstraint', 'pointConstraint',
                                                                 'orientConstraint', 'scaleConstraint',
                                                                 'aimConstraint'])
        return constraints

    def process(self, **kwargs):
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')
        else:
            constraints = self.getInvalid()
            if constraints:
                raise RuntimeError('Geometry总组下禁止存放约束节点: {}'.format(constraints))

    def select(self):
        cmds.select(self.getInvalid())