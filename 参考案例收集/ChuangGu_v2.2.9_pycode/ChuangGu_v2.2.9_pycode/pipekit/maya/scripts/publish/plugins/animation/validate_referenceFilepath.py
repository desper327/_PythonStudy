# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateReferenceFilepath(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：引用文件正确路径'
    actions = ['select']

    def process(self, **kwargs):
        project = kwargs['project']
        assetsDir = kwargs['assetsDir']
        chrDir = assetsDir + '/chr/'
        prpDir = assetsDir + '/prp/'
        vehDir = assetsDir + '/veh/'
        setDir = assetsDir + '/set/'

        # ['chr', 'prp']
        self.error = []
        error0 = []
        error1 = []
        reference = cmds.file(q=1, reference=1)
        if reference:
            reference.sort(reverse=False)
            for i in reference:
                i = i.replace('\\', '/')
                rfn = cmds.referenceQuery(i, rfn=1)
                if chrDir in i or prpDir in i or vehDir in i:
                    if '/rig/publish/' not in i:
                        error1.append(rfn)
                else:
                    if project == 'PPLU':
                        if 'X:/PIPILU/Season' in i:
                            if '/EP' not in i:
                                error0.append(rfn)
                            else:
                                if '/BG/' not in i:
                                    error0.append(rfn)
                        else:
                            error0.append(rfn)
                    else:
                        error0.append(rfn)

        # ['set']
        assemblies = cmds.ls(assemblies=1)
        for i in assemblies:
            if cmds.nodeType(i) == 'assemblyReference':
                filepath = cmds.getAttr(i + '.definition')
                if setDir in filepath:
                    if '/asm/publish/' not in filepath:
                        error1.append(i)
                else:
                    error0.append(i)

        if error0:
            self.error = error0
            raise ValueError('资产 {0} 不隶属于 {1} 项目.'.format(error0, project))
        elif error1:
            self.error = error1
            raise ValueError('资产版本路径错误 {}.'.format(error1))

    def select(self):
        if self.error:
            cmds.select(self.error, r=1)