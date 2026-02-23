# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectExistsCamera(plugin.MayaCollector):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.MayaCollector.order + 0.5
    label = '收集：场景内至少存在一个新建摄像机'

    def process(self, **kwargs):
        cameras = []
        for cam in cmds.ls(type=['camera']):
            if ':' not in cam:
                cameras.append(cam)

        if len(cameras) < 5:
            raise ValueError('场景内至少存在一个新建摄像机而非只有4个默认相机')