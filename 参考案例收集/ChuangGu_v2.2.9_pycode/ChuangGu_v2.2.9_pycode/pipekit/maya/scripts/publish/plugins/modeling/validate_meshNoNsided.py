# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
from publish import plugin


class ValidateMeshNoNside(plugin.Validator):
    """Validate meshes don't have triangles
    """
    label = '验证：模型没有多边面'
    actions = ['select']
    optional = True
    ignoreType = ['env', 'set']

    def getInvalid(self):
        meshes = cmds.ls(type='mesh')
        cmds.select(meshes)
        cmds.polySelectConstraint(mode=3, type=0x0008, size=3)
        cmds.polySelectConstraint(disable=True)
        return cmds.ls(sl=True, fl=True)
    
    def process(self, **kwargs):
        invalid = self.getInvalid()
        cmds.select(clear=1)
        if invalid:
            raise ValueError('找到 {} 个多边面.'.format(len(invalid)))

    def select(self):
        mel.eval('changeSelectMode -component')
        cmds.selectType(smp=False, sme=True, smf=False, smu=False, pv=False, pe=True, pf=False, puv=False)
        cmds.select(self.getInvalid())