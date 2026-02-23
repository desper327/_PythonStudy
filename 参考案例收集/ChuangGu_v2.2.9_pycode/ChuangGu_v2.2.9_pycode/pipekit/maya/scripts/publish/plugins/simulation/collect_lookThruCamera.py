# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectLookThruCamera(plugin.MayaCollector):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.MayaCollector.order + 0.5
    label = '收集：动画组摄像机'

    def process(self, **kwargs):
        camera = cmds.lookThru(q=True)
        if 'sim:' not in camera:
            raise ValueError('请手动切换[sim:*]类型摄像机作为当前视窗.')