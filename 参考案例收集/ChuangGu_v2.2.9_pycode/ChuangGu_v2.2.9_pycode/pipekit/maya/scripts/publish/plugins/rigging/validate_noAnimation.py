# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoAnimation(plugin.Validator):
    label = '验证：没有动画曲线'
    
    def getKeys(self):
        ts = cmds.ls(type=['animCurveTL', 'animCurveTA', 'animCurveTU'])
        return ts

    def process(self, **kwargs):
        keyframes = self.getKeys()
        if keyframes:
            raise ValueError('场景中有关键帧节点.')

    def repair(self, args):
        '''delete keyframes'''
        keyframes = self.getKeys()
        numKeys = len(keyframes)
        if keyframes:
            cmds.delete(keyframes)
            self.log.info('删除 {} 动画曲线节点'.format(numKeys))