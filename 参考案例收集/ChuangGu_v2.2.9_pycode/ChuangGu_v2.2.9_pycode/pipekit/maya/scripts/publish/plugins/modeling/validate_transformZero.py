# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateTransformZero(plugin.Validator):
    """Transforms can't have any values
    To solve this issue, try freezing the transforms. So long
    as the transforms, rotation and scale values are zero,
    you're all good.
    """
    _identity = [1.0, 0.0, 0.0, 0.0, 
                 0.0, 1.0, 0.0, 0.0, 
                 0.0, 0.0, 1.0, 0.0, 
                 0.0, 0.0, 0.0, 1.0] 
    _tolerance = 1e-30
    optional = True
    label = '验证：通道参数归零'
    actions = ['select']

    @classmethod
    def get_invalid(cls):
        transforms = cmds.ls(type="transform")
        invalid = []
        for transform in transforms:
            if cmds.listRelatives(transform, type='camera'):
                continue
            if cmds.nodeType(transform) == 'place3dTexture':
                continue 
            mat = cmds.xform(transform, q=1, matrix=True, objectSpace=True)
            if not all(abs(x-y) < cls._tolerance
                       for x, y in zip(cls._identity, mat)):
                invalid.append(transform)
        return invalid

    def process(self, **kwargs):
        invalid = self.get_invalid()
        if invalid:
            raise ValueError("需要冻结参数的节点: {0}".format(invalid))
        
    def select(self):
        cmds.select(self.get_invalid())