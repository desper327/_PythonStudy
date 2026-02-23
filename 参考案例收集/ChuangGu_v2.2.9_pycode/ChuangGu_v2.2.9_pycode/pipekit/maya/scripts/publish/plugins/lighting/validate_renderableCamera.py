# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateRenderableCamera(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    label = '验证：可渲染摄像机'
    order = plugin.Validator.order - 1.5

    def process(self, **kwargs):
        self.camera = 'lgt:' + kwargs['taskDir'].split('/', 4)[-1].replace('/', '_') + '_ani'
        self.error = {}
        if not cmds.objExists(self.camera):
            self.error['miss'] = '请通过灯光组assembly工具组装灯光镜头文件.'
            raise ValueError('场内未找到通过组装工具导入的摄像机: {} .'.format([self.camera]))
        else:
            cameras = cmds.ls(cameras=1)
            for i in cameras:
                if self.camera in i:
                    if cmds.getAttr(self.camera + '.renderable') == False:
                        self.error['renderable'] = False
                else:
                    cmds.setAttr(i + '.renderable', False)

            if self.error:
                raise ValueError("渲染设置面板中['Renderable Cameras'] 项未设置正确渲染的摄像机\n"
                                 "单击['repair']按钮完成自动修复.")

    def repair(self, args):
        if 'miss' in self.error:
            raise ValueError(self.error['miss'])
        elif 'renderable' in self.error:
            cmds.setAttr(self.camera + '.renderable', True)