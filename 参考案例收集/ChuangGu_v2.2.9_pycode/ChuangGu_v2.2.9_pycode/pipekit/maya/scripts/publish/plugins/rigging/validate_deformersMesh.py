# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateDeformersMesh(plugin.Validator):
    label = '验证：模型持有蒙皮或融合或包裹或晶格的输入节点'
    actions = ['select']
    optional = True

    @classmethod
    def getInvalid(cls):
        deformers = []
        meshes = cmds.filterExpand('Geometry', ex=1, sm=12)
        if meshes:
            for mesh in meshes:
                if cmds.nodeType(mesh) == 'mesh':
                    shape = mesh
                    mesh = cmds.listRelatives(mesh, p=1)[0]
                else:
                    shape = cmds.listRelatives(mesh, shapes=1, path=1, ni=1)[0]
                v = cmds.getAttr(shape + '.v')
                if v == 0:
                    cmds.setAttr(shape + '.v', 1)
                nodes = cmds.listHistory(mesh, pdo=1)
                if nodes:
                    p = []
                    for node in nodes:
                        if cmds.nodeType(node) in ['skinCluster', 'blendShape', 'wrap', 'ffd']:
                            p.append(1)
                            break
                    if not p:
                        deformers.append(mesh)
                else:
                    deformers.append(mesh)
                cmds.setAttr(shape + '.v', v)
        return deformers

    def process(self, **kwargs):
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')
        else:
            deformers = self.getInvalid()
            if deformers:
                raise Exception('模型缺失输入节点: {}'.format(deformers))

    def select(self):
        deformers = self.getInvalid()
        if deformers:
            cmds.select(deformers)