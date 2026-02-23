# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateFileOutputName(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    label = '验证：文件输出命名'
    order = plugin.Validator.order - 3.0

    def process(self, **kwargs):
        self.filename = kwargs['departmentDir'].split('/', 4)[-1].replace('/', '_')

        # 文件命名
        if cmds.getAttr("defaultRenderGlobals.imageFilePrefix") != self.filename:
            raise ValueError('File name prefix: 设置错误,应为 {}'.format([self.filename]))

    def repair(self, args):
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", self.filename, type="string")