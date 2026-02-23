# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateBansDeformedString(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.5
    label = '验证：禁止存在Deformed字符'

    def process(self, **kwargs):
        self.deformed = cmds.ls('*Deformed')
        if self.deformed:
            raise ValueError('禁止出现Deformed字符,单击[repair]按钮完成修复')

    def repair(self, args):
        if self.deformed:
            for i in self.deformed:
                newname = i.replace('Deformed', '')
                cmds.rename(i, newname)