# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateReferenceIsLoaded(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：引用文件正常加载'
    actions = ['select']
    ignoreType = ['assets']

    def process(self, **kwargs):
        # ['chr', 'prp']
        self.error = []
        reference = cmds.file(q=1, reference=1)
        if reference:
            reference.sort(reverse=False)
            for i in reference:
                rfn = cmds.referenceQuery(i, rfn=1)
                if not cmds.referenceQuery(rfn, isLoaded=1):
                    self.error.append(rfn)

        if self.error:
            raise ValueError('引用资产未加载 {} ,如果是场景内无用角色请手动移除'.format(self.error))

    def select(self):
        if self.error:
            cmds.select(self.error, r=1)

    def repair(self, args):
        if self.error:
            for rn in self.error:
                cmds.file(loadReference=rn)