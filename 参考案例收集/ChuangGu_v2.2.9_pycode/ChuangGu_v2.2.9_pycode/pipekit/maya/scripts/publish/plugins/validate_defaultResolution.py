# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateDefaultResolution(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    label = '验证：渲染尺寸'
    ignoreType = ['assets']

    def process(self, **kwargs):
        self.resolutions = kwargs['resolutions']
        w = cmds.getAttr('defaultResolution.width')
        h = cmds.getAttr('defaultResolution.height')
        if w == self.resolutions[0] and h == self.resolutions[1]:
            pass
        else:
            raise ValueError('渲染尺寸为 {}'.format(self.resolutions))

    def repair(self, args):
        cmds.setAttr('defaultResolution.width', self.resolutions[0])
        cmds.setAttr('defaultResolution.height', self.resolutions[1])