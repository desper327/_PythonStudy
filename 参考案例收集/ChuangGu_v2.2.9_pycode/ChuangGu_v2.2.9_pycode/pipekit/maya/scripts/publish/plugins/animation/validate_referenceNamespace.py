# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateReferenceNamespace(plugin.Validator):
    ''' Check playback speed/frame rate.'''
    label = '验证：引用文件名称空间'

    def process(self, **kwargs):
        project = kwargs['project']
        assetsDir = kwargs['assetsDir']
        chrDir = assetsDir + '/chr/'
        prpDir = assetsDir + '/prp/'
        setDir = assetsDir + '/set/'

        # 获取['chr', 'prp']参考信息
        self.error0 = {}
        self.error1 = []
        reference = cmds.file(q=1, reference=1)
        if reference:
            '''
            # 1.7.3
            rfn = []
            reference.sort(reverse=False)
            for i in reference:
                rn = cmds.referenceQuery(i, rfn=1)
                if chrDir in i or prpDir in i:
                    if '/rig/publish/' in i:
                        rfn.append(rn)
                else:
                    if project == 'PPLU':
                        if 'X:/PIPILU/Season' in i:
                            if '/EP' not in i:
                                rfn.append(rn)
                            else:
                                if '/BG/' not in i:
                                    rfn.append(rn)
                        else:
                            rfn.append(rn)
                    else:
                        rfn.append(rn)
            if rfn:
                for rn in rfn:
                    if len(rn.split('_')) > 1:
                        self.error0.append(rn)
            '''
            # 1.8.0
            reference.sort(reverse=False)
            for i in reference:
                rn = cmds.referenceQuery(i, rfn=1)
                if chrDir in i or prpDir in i:
                    if '/rig/publish/' in i:
                        rnname = i.split('/')[4] + 'RN'
                        if rnname not in rn:
                            self.error0[rn] = rnname
        # ['set']
        assemblies = cmds.ls(assemblies=1)
        for ar in assemblies:
            if cmds.nodeType(ar) == 'assemblyReference':
                if len(ar.split('_')) == 3 and '_set_AR' in ar:
                    pass
                else:
                    self.error1.append(ar)

        if self.error0:
            text = ['*RN', '*RN#']
            raise ValueError('{0} 的名称空间应为 {1} 此类型命名格式.'.format(self.error0.keys(), text))
        elif self.error1:
            text = ['*_set_AR', '*_set_AR#']
            raise ValueError('{0} 的名称空间应为 {1} 此类型命名格式.'.format(self.error1, text))


    def repair(self, args):
        if self.error0:
            for k, v in self.error0.items():
                cmds.lockNode(k, lock=0)
                nrn = cmds.rename(k, v)
                cmds.lockNode(nrn, lock=1)
        if self.error1:
            for ar in self.error1:
                cmds.rename(ar, ar.split('_')[0] + '_set_AR')