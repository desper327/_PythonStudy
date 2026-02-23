# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectOutlinerParallel(plugin.MayaCollector):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.MayaCollector.order
    label = '收集：大纲物体平行'

    def process(self, **kwargs):
        self.error = {
            'stage': None,
            'ar': [],
            'ds': [],
            'ns': []
        }

        # ar
        ars = cmds.ls(type=['assemblyReference'], l=1)
        for i in ars:
            array = i.split('|')
            if len(array) > 2:
                self.error['ar'].append(i)

        # ds
        all = cmds.ls(type=['mesh'], l=1)
        if all:
            for i in all:
                mesh = cmds.listRelatives(i, p=1, f=1)
                if len(i.split('|')) == 3:
                    if '_env_pxy' in i:
                        self.error['ds'].append(mesh[0])
                    else:
                        self.error['ns'].append(mesh[0])
                else:
                    if '_env_pxy' not in i:
                        self.error['ns'].append(mesh[0])

        if self.error['ar']:
            self.error['stage'] = 'ar'
            raise RuntimeError('AR节点平行存在大纲内,单击 [repair] 按钮完成自动修复.')
        elif self.error['ds']:
            self.error['stage'] = 'ds'
            raise RuntimeError('关联复制文件 {} 应存放在[*_env_DS]总组下,单击 [repair] 按钮完成自动修复.'.format(self.error['ds']))
        elif self.error['ns']:
            self.error['stage'] = 'ns'
            raise RuntimeError('模型文件命名错误,单击 [repair] 按钮完成自动删除.')

    def repair(self, args):
        if self.error['stage'] == 'ar':
            for i in self.error['ar']:
                cmds.parent(i, w=1)
        elif self.error['stage'] == 'ds':
            for i in self.error['ds']:
                ds = i.rsplit('_', 1)[0] + '_DS'
                cmds.parent(i, ds)
        elif self.error['stage'] == 'ns':
            cmds.delete(self.error['ns'])