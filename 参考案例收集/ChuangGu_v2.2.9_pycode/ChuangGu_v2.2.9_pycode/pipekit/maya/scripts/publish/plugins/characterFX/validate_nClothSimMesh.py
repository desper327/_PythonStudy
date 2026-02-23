# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectNClothSimMesh(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order - 0.5
    label = '验证：nCloth输入节点'
    actions = ['select']

    def process(self, **kwargs):
        # nCloth
        if not cmds.objExists('clothWpNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')
        else:
            self.error = []
            meshes = cmds.filterExpand('clothWpNUL', ex=1, sm=12)
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
                    nodes = cmds.listHistory(mesh)
                    if nodes:
                        p = []
                        for node in nodes:
                            if cmds.nodeType(node) in ['nCloth']:
                                p.append(1)
                                break
                        if not p:
                            self.error.append(mesh)
                    else:
                        self.error.append(mesh)
                    cmds.setAttr(shape + '.v', v)

            if self.error:
                raise ValueError("衣服解算体模型未添加nCloth节点.\n"
                                 "单击['select']按钮选择错误对象.")

    def select(self):
        if self.error:
            cmds.select(self.error, r=1)