# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateShapeDefaultNames(plugin.Validator):
    """ Validates that Shape names are using Maya's default format """
    order = plugin.Validator.order + 1.0
    label = '验证：形状节点命名正确'
    actions = ['select']
    ignoreType = ['set']

    def process(self, **kwargs):
        """Process all the shape nodes in the instance"""
        self.error = []
        self.shapes = []
        if cmds.objExists('srfNUL'):
            meshes = cmds.filterExpand('Geometry', ex=1, sm=12)
            if meshes:
                for imesh in meshes:
                    shapes = cmds.listRelatives(imesh, shapes=1, f=1)
                    if len(shapes) > 1:
                        self.error1.append(imesh)
                    else:
                        shapes = cmds.listRelatives(imesh, shapes=1, f=1, ni=1)
                        if str(shapes[0]).split('|')[-1] != (str(imesh).split('|')[-1] + 'Shape'):
                            self.shapes.append(shapes[0])
            else:
                raise RuntimeError('Geometry总组下未找到模型.')

            if self.error:
                raise RuntimeError('形状节点下存在Orig节点,先完成 <模型没有中间形状> 的修复工作.')
            elif self.shapes:
                raise RuntimeError('形状节点命名错误,请到大纲查阅.')
        else:
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

    def repair(self, args):
        if self.shapes:
            for shape in self.shapes:
                obj = cmds.listRelatives(shape, p=1)
                cmds.rename(shape, obj[0] + 'Shape')

    def select(self):
        if self.shapes:
            cmds.select(self.shapes, r=1)