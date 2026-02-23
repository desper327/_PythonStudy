# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateMeshColoured(plugin.Validator):
    """Checks whether any meshes have lambert1 applied.
    """
    label = '验证：模型添加默认lambert1材质球'
    actions = ['select']

    def process(self, **kwargs):
        self.error = []
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复.')
        else:
            meshes = cmds.filterExpand('Geometry', ex=1, sm=12)
            if not meshes:
                null = ['aniNUL', 'srfNUL', 'simNUL']
                raise ValueError('Geometry总组下未找到任何模型,请将模型存放至 {} 对应组内.'.format(null))

            lambert = cmds.listConnections('initialShadingGroup.dagSetMembers', source=True, destination=False)
            if not lambert:
                self.error = meshes
            elif len(meshes) != len(lambert):
                for mesh in meshes:
                    if mesh not in lambert:
                        self.error.append(mesh)

            if self.error:
                raise RuntimeError('未赋予lambert1默认材质球的模型: {}'.format(meshes))
        
    def select(self):
        cmds.select(self.error)