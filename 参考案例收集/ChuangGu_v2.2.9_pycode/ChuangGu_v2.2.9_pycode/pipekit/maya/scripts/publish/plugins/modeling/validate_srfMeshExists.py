# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateSrfMeshExists(plugin.Validator):
    """Check that the polygon model exists in the scene.
    """
    order = plugin.Validator.order - 11.5
    label = '验证：srf总组务必有Polygon模型'

    def process(self, **kwargs):
        if cmds.objExists('srfNUL'):
            meshes = cmds.filterExpand('srfNUL', ex=1, sm=12)
            if not meshes:
                raise RuntimeError('Geometry|srfNUL总组下未找到Polygon模型.')
        else:
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')