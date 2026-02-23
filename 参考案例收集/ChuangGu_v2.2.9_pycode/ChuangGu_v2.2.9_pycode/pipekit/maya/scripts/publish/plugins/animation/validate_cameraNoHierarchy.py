# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateCameraNoHierarchy(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：摄像机没有层级'
    # optional = True

    def process(self, **kwargs):
        camera = [cmds.lookThru(q=True)]
        if camera in ['persp', 'top', 'front', 'side']:
            raise ValueError('当前摄像机禁止为默认摄像机,请切换到新建摄像机窗口.')

        if cmds.listRelatives(camera[0], p=1):
            # raise ValueError('不建议摄像机 {} 之上还有组层级,但允许跳过.'.format(camera))
            raise ValueError('摄像机 {} 之上存在组层级.\n'
                             '如果组本身没有数值请将摄像机移除组外.\n'
                             '反之请自建新的摄像机完成命名及bake动画.'.format(camera))