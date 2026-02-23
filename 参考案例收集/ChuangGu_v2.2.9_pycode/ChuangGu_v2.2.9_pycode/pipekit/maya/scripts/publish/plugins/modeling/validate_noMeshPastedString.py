# -*- coding: utf-8 -*-

from publish import plugin
import maya.cmds as cmds


class ValidateNoMeshPastedString(plugin.Validator):
    ''' Check there are no mesh items with default "Lambert1" '''
    order = plugin.Validator.order - 1.0
    label = '验证：没有粘贴字符'

    def process(self, **kwargs):
        self.error = cmds.ls(['*:pasted__*', '*pasted__*'])
        if self.error:
            raise RuntimeError("大纲内所有节点命名禁止出现['pasted__']字符.\n"
                               "单击['repair']按钮完成自动修复.")

    def repair(self, args):
        if self.error:
            for i in self.error:
                cmds.lockNode(i, lock=0)
                new = i.replace('pasted__', '')
                cmds.rename(i, new)