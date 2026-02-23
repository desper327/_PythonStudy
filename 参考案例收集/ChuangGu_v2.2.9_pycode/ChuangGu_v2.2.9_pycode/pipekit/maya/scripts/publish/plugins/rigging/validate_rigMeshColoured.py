# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateRigMeshColoured(plugin.Validator):
    """Checks whether any meshes have ['blinn', 'lambert', 'phong'] applied.
    """
    label = "验证：添加Maya内置纯色/单色材质球"
    actions = ['select']

    def process(self, **kwargs):
        self.error = []
        error0 = []
        error1 = []
        error2 = []
        emptyMats = []
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复.')
        else:
            # 获取所选物体的材质
            meshes = cmds.filterExpand('Geometry', ex=1, sm=12)
            if meshes:
                defaults = ['blinn', 'lambert', 'phong']
                for mesh in meshes:
                    cmds.refresh()
                    if cmds.nodeType(mesh) == 'mesh':
                        shape = mesh
                        mesh = cmds.listRelatives(mesh, p=1)[0]
                    else:
                        shape = cmds.listRelatives(mesh, shapes=1, path=1, ni=1)[0]
                    shadingEngines = cmds.listConnections(shape, type='shadingEngine')
                    if not shadingEngines:
                        emptyMats.append(mesh)
                    else:
                        shadingEngines = list(set(shadingEngines))
                        materials = cmds.ls(cmds.listConnections(shadingEngines), materials=1)
                        for material in materials:
                            if cmds.nodeType(material) in defaults:
                                if material == 'lambert1':
                                    error1.append(mesh)
                                else:
                                    fileNode = cmds.listConnections(material + '.color', type='file')
                                    if fileNode:
                                        error2.extend(fileNode)
                            else:
                                error0.append(mesh)
            if emptyMats:
                self.error = emptyMats
                raise RuntimeError('模型丢失材质球: {}.'.format(emptyMats))
            elif error0:
                self.error = error0
                raise RuntimeError("模型只能赋予['blinn', 'lambert', 'phong']类型材质球: {}".format(error0))
            elif error1:
                self.error = error1
                raise RuntimeError("模型禁止赋予['lambert1']默认材质球: {}".format(error1))
            elif error2:
                self.error = error2
                raise RuntimeError('禁止材质球下添加file贴图节点: {}'.format(error2))

    def select(self):
        if self.error:
            cmds.select(self.error, r=1)