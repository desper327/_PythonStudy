# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateMeshHasUVs(plugin.Validator):
    '''
    Checks whether mesh has UVs.
    Number of UVs must be at least number of Vertices
    '''
    label = '验证：模型拥有UVs'
    optional = True
    actions = ['select']

    def process(self, **kwargs):
        self.invalid = []

        for node in cmds.ls(type='mesh'):
            uv = cmds.polyEvaluate(node, uv=True)
    
            if uv == 0:
                self.invalid.append(node)
                continue

            vertex = cmds.polyEvaluate(node, vertex=True)
            if uv < vertex:
                self.invalid.append(node)
                continue

        if self.invalid:
            raise RuntimeError("模型没有有效的UVs: {0}".format(self.invalid))

    def select(self):
        cmds.select(self.invalid)