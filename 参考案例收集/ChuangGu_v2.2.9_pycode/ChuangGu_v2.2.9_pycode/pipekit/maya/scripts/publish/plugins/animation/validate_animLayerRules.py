# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
from publish import plugin


class ValidateAnimLayerRules(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：动画层规则'

    def process(self, **kwargs):
        warning = []
        error = []
        layers = cmds.ls(type=['animLayer'])
        if layers:
            for i in layers:
                if i == 'BaseAnimation':
                    warning.append(i)
                else:
                    error.append(i)
        if error:
            raise ValueError("只允许['BaseAnimation']基础动画层存在,请单击['repair']按钮完成动画层合并.")
        elif warning:
            self.optional = True
            raise ValueError("['BaseAnimation']基础动画层存在,但允许跳过.")

    def repair(self, args):
        layers = cmds.ls(type=['animLayer'])
        if layers:
            objs = '{'
            for i in range(len(layers)):
                if i == len(layers) - 1:
                    objs += '\"' + str(layers[i]) + '\"'
                else:
                    print i
                    objs += '\"' + str(layers[i]) + '\",'
            objs += '}'
            mel.eval('layerEditorMergeAnimLayer(' + objs + ',0)')
        else:
            raise ValueError("对象为空禁止修复.")