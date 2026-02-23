# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateSimMeshExists(plugin.Validator):
    """Check that the polygon model exists in the scene.
    """
    order = plugin.Validator.order - 11.0
    label = '验证：sim总组非必要存在Polygon模型'
    optional = True

    def process(self, **kwargs):
        category = kwargs['category']
        if category == 'chr' or category == 'prp':
            error = []
            if cmds.objExists('simNUL'):
                if cmds.objExists('clothNUL') and cmds.objExists('clothWpNUL'):
                    clothRrMeshes = cmds.filterExpand('clothNUL', ex=1, sm=12)
                    clothWpMeshes = cmds.filterExpand('clothWpNUL', ex=1, sm=12)
                    if clothRrMeshes and clothWpMeshes:
                        if len(clothRrMeshes) != len(clothWpMeshes):
                            self.optional = False
                            error.append('clothNUL与clothWpNUL总组模型个数不对等')
                    else:
                        self.optional = True
                        error.append('clothWpNUL总组存放布料解算体模型 -> 如果任务没有布料环节还可以跳过')

                if cmds.objExists('hairGrmNUL'):
                    meshes = cmds.filterExpand('hairGrmNUL', ex=1, sm=12)
                    if not meshes:
                        error.append('hairGrmNUL总组存放毛发生长体模型 -> 如果任务没有毛发环节还可以跳过')
            else:
                error.append('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

            if error:
                raise RuntimeError('\n'.join(error))