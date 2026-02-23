# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateDeformersEnvelope(plugin.Validator):
    label = '验证：变形节点开关正常打开'
    actions = ['select']
    optional = True

    @classmethod
    def getInvalid(cls):
        deformers = []
        meshes = cmds.filterExpand('Geometry', ex=1, sm=12)
        if meshes:
            for mesh in meshes:
                if cmds.nodeType(mesh) == 'mesh':
                    mesh = cmds.listRelatives(mesh, p=1)[0]
                hists = cmds.listHistory(mesh, pdo=1, il=1)
                nodes = cmds.ls(hists, type=['skinCluster', 'blendShape', 'wrap'])
                for node in nodes:
                    if not cmds.getAttr(node + '.envelope'):
                        if not cmds.listConnections(node + '.envelope', source=True, destination=False):
                            deformers.append(node)
        return deformers

    def process(self, **kwargs):
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')
        else:
            deformers = self.getInvalid()
            if deformers:
                raise Exception('变形节点开关关闭: {}'.format(deformers))

    def repair(self, args):
        deformers = self.getInvalid()
        if deformers:
            for deformer in deformers:
                cmds.setAttr(deformer + '.envelope', 1)

    def select(self):
        deformers = self.getInvalid()
        if deformers:
            cmds.select(deformers)