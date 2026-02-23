# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidatePlaybackSpeed(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：播放速度/帧速率'
    ignoreType = ['assets']

    def process(self, **kwargs):
        self.fps = kwargs['playbackSpeed']
        fps = cmds.currentUnit(q=1, time=1)
        if fps == 'film':
            fps = '24fps'
        elif fps == 'pal':
            fps = '25fps'
        elif fps == 'ntscf':
            fps = '60fps'
        if fps != self.fps:
            raise ValueError('播放速度为 {}'.format(self.fps))

    def repair(self, args):
        cmds.currentUnit(time=self.fps)