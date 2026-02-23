# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoIntermediateShapes(plugin.Validator):
    '''Checks for objects with intermediate shapes.'''
    order = plugin.Validator.order + 0.5
    label = '验证：模型没有中间形状'

    @classmethod    
    def _getInvalid(*kwargs):
        intermediate_objects = cmds.ls(shapes=True, intermediateObjects=True, long=True)
        return intermediate_objects
     
    def process(self, **kwargs):
        """Process all the intermediateObject nodes in the instance"""
        intermediate_objects = self._getInvalid()
        if intermediate_objects:
            raise ValueError("发现中间对象: {0}".format(intermediate_objects))

    def repair(self, args):
        """Delete all intermediateObjects"""
        intermediate_objects = self._getInvalid()
        if intermediate_objects:
            future = cmds.listHistory(intermediate_objects, future=True)
            cmds.delete(future, ch=True)
            cmds.delete(intermediate_objects)