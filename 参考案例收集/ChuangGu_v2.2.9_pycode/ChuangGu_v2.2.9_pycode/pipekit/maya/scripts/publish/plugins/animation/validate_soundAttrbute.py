# -*- coding: utf-8 -*-

import os
import maya.cmds as cmds
import maya.mel as mel
from publish import plugin


class ValidateSoundAttrbute(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：音频文件地址及属性'
    actions = ['select', 'opendir']

    def process(self, **kwargs):
        self.sound = None
        self.epDir = None
        startFrame = kwargs['startFrame']
        taskDir = kwargs['taskDir']
        project = kwargs['project']
        business = kwargs['business']

        audios = cmds.ls(type='audio')
        if audios:
            sfile = cmds.getAttr(audios[0] + '.filename')
            if os.path.exists(sfile):
                gPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
                audio = cmds.timeControl(gPlayBackSlider, q=1, sound=1)
                if audio:
                    self.sound = audio
                    offset = cmds.getAttr(audio + '.offset')
                    if offset != startFrame:
                        self.optional = True
                        raise ValueError('场景内音频文件的offset属性建议等于 {} ,但允许跳过.\n'
                                         '单击select按钮后, ctrl+a 打开属性面板'.format(startFrame))
                else:
                    raise ValueError('场景内音频文件未正产使用.')
            else:
                raise ValueError('场景内音频文件丢失.\n'
                                 '请到CGTW对应任务下的[工作/声音文件]框及时下载音频文件')
        else:
            if business == 'film':
                self.epDir = taskDir.rsplit('/', 1)[0].replace('shots', 'sound')
            else:
                self.epDir = taskDir.rsplit('/', 2)[0].replace('shots', 'sound')
            wavfile = self.epDir + '/' + project + '_' + taskDir.split('/', 4)[4].replace('/', '_') + '.wav'
            if not os.path.exists(wavfile):
                self.optional = True
                raise ValueError('场景内未找到音频文件.\n'
                                 '如果CGTW对应任务下的[工作/声音文件]框存在音频文件请及时下载,文件不存在则可以跳过')
            else:
                raise ValueError('服务器已经存在音频文件但场景内未找到音频文件.\n'
                                 '单击opendir按钮打开音频所在文件夹,请手动拖拽到Maya时间条上.')

    def select(self):
        if self.sound:
            cmds.select(self.sound, r=1)

    def opendir(self):
        if self.epDir:
            os.startfile(self.epDir)