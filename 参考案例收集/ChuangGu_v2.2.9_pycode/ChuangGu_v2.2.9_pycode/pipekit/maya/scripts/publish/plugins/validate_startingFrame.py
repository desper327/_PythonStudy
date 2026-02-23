# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateStartingFrame(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    label = '验证：项目起始帧'
    ignoreType = ['assets']

    def process(self, **kwargs):
        self.startFrame = kwargs['startFrame']
        start = cmds.playbackOptions(q=1, minTime=1)
        if start != self.startFrame:
            raise ValueError('起始帧为 {}'.format(self.startFrame))

    def repair(self, args):
        cmds.playbackOptions(e=1, minTime=self.startFrame)