# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateCameraNaming(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：摄像机规则命名'

    def process(self, **kwargs):
        taskDir = kwargs['taskDir']
        abbr = kwargs['department']
        self.camera = taskDir.split('/', 4)[-1].replace('/', '_') + '_' + abbr
        camera = cmds.lookThru(q=True)
        if camera.split('|')[-1] != self.camera:
            raise ValueError('摄像机命名: {}'.format(self.camera))
        else:
            shapes = cmds.listRelatives(camera, shapes=1, f=1)
            if shapes[0].split('|')[-1] != self.camera + 'Shape':
                raise ValueError('摄像机形状节点命名: {}'.format(self.camera + 'Shape'))

    def repair(self, args):
        cameras = ['persp', 'top', 'front', 'side']
        camera = cmds.lookThru(q=True)
        if camera in cameras:
            raise RuntimeError('当前摄像机 {} 不给与修复,请切换摄像机或创建摄像机'.format(cameras))
        else:
            ncam = cmds.rename(camera, self.camera)
            shapes = cmds.listRelatives(ncam, shapes=1, f=1)
            if shapes:
                cmds.rename(shapes[0], self.camera + 'Shape')