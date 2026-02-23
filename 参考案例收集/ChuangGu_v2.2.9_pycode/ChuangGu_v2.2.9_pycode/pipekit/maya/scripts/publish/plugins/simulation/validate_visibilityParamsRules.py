# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateVisibilityParamsRules(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.3
    label = '验证：显示层参数规则'
    ignoreType = ['sim']

    def process(self, **kwargs):
        self.error = {
            'unload': [],
            'outliner': {}
        }
        reference = cmds.file(q=1, reference=1)
        if reference:
            for i in reference:
                rfn = cmds.referenceQuery(i, rfn=1)
                if not cmds.referenceQuery(rfn, isLoaded=1):
                    self.error['unload'].append(rfn)
                else:
                    rootNUL = cmds.referenceQuery(rfn, nodes=1)[0]
                    if not cmds.getAttr(rootNUL + '.v'):
                        self.error['outliner'][rootNUL + '.v'] = 1
                    else:
                        nsid = rootNUL.split(':')[0]
                        if ':srfNUL' in rootNUL:
                            nulls = ['defaultNUL', 'clothNUL', 'noRenderNUL']
                            for n in nulls:
                                null = nsid + ':' + n
                                if not cmds.getAttr(null + '.v'):
                                    self.error['outliner'][null + '.v'] = 1
                        elif ':cfxNUL' in rootNUL:
                            nulls = ['srfNUL', 'simNUL', 'fx2NUL',
                                     'noRenderNUL', 'hairCurveNUL']
                            for n in nulls:
                                null = nsid + ':' + n
                                if not cmds.getAttr(null + '.v'):
                                    self.error['outliner'][null + '.v'] = 1

                            if not cmds.getAttr(nsid + ':clothNUL.v'):
                                self.error['outliner'][nsid + ':clothNUL.v'] = 1
                            if cmds.getAttr(nsid + ':clothWpNUL.v'):
                                self.error['outliner'][nsid + ':clothWpNUL.v'] = 0
                            if cmds.getAttr(nsid + ':clothMeshNUL.v'):
                                self.error['outliner'][nsid + ':clothMeshNUL.v'] = 0
                            if cmds.filterExpand(nsid + ':noRenderNUL', ex=1, sm=12):
                                if cmds.getAttr(nsid + ':hairGrmNUL.v'):
                                    self.error['outliner'][nsid + ':hairGrmNUL.v'] = 0
                            else:
                                if not cmds.getAttr(nsid + ':hairGrmNUL.v'):
                                    self.error['outliner'][nsid + ':hairGrmNUL.v'] = 1

        if self.error['unload']:
            raise ValueError("单击['验证：引用文件正常加载']项,再次单击['repair']按钮完成自动修复.")

        if self.error['outliner']:
            if cmds.objExists('persp.mode'):
                mode = cmds.getAttr('persp.mode')
                if mode in ['replace', 'combine']:
                    self.optional = True
                else:
                    self.optional = False
            raise ValueError("预设显示层参数错误,单击['repair']按钮自动完成修复.")

    def repair(self, args):
        if self.error['outliner']:
            for k, v in self.error['outliner'].items():
                cmds.setAttr(k, v)