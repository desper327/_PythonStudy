# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoEmptyBlendshapes(plugin.Validator):
    label = '验证：没有空的blendshapes'
    optional = True
    actions = ['select']

    def process(self, **kwargs):
        if getEmptyBlendshapeNodes():
            raise Exception('{} blendShape发现没有目标体节点.'.format())

    def select(self):
        cmds.select(getEmptyBlendshapeNodes())
            
            
def getEmptyBlendshapeNodes():
    bsNodes = []
    bs = cmds.ls(type='blendShape')
    for each in bs:
        if cmds.getAttr(each+'.w', size=True) == 0:
            bsNodes.append(each)
    return bsNodes