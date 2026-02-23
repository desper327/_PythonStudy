# -*- coding: utf-8 -*-

import os
import json
import maya.cmds as cmds
from publish import plugin


class ValidateFrameRange(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    label = '验证：渲染时长/帧范围'
    order = plugin.Validator.order - 2.0

    def process(self, **kwargs):
        self.error = {}
        if cmds.objExists('lgtRN'):
            jfile = cmds.referenceQuery('lgtRN', filename=1).rsplit('/', 1)[0] + '/__init__.json'
            if os.path.exists(jfile):
                with open(jfile, 'r') as fo:
                    cdict = json.load(fo)
                timeSlider = cdict['setting']['timeSlider']
                startFrame = cmds.getAttr('defaultRenderGlobals.startFrame')
                endFrame = cmds.getAttr('defaultRenderGlobals.endFrame')
                byFrame = cmds.getAttr('defaultRenderGlobals.byFrame')

                cmds.playbackOptions(e=1, maxTime=timeSlider[1])
                if timeSlider[0] != startFrame:
                    self.error['startFrame'] = timeSlider[0]
                if timeSlider[1] != endFrame:
                    self.error['endFrame'] = timeSlider[1]
                if byFrame != 1.0:
                    self.error['byFrame'] = 1.0

                if self.error:
                    raise ValueError("渲染时长设置错误,单击['repair']按钮完成自动修复.")
            else:
                self.optional = True
                raise ValueError('未找到动画组标准读取数据.')
        else:
            self.error['error'] = "请使用['assembly']工具组装镜头,之后再通过提交工具完成文件验证."
            raise ValueError('场内未找到通过组装工具导入的摄像机.')

    def repair(self, args):
        if self.error:
            if 'error' in self.error:
                raise ValueError(self.error['error'])
            else:
                for k, v in self.error.items():
                    cmds.setAttr('defaultRenderGlobals.' + k, v)