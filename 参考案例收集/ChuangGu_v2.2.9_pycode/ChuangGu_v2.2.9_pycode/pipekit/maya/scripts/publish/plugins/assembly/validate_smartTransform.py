# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class validateSmartTransform(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 1.0
    label = '收集：关联复制生效'

    def process(self, **kwargs):
        meshs = cmds.ls(type=['mesh'])
        self.error = []
        if meshs:
            for i in meshs:
                if not cmds.listHistory(i, pdo=1):
                    self.error.append(i)

        if self.error:
            raise RuntimeError("场景内局部关联复制文件失效,单击[repair]按钮完成修复.")

    def repair(self, args):
        if self.error:
            error = []
            for i in self.error:
                pxyShape = i.split('_')[0] + '_env_pxyShape'
                if cmds.objExists(pxyShape):
                    objs = cmds.listRelatives(i, p=1, f=1)
                    cmds.delete(i)
                    cmds.parent(pxyShape, objs[0], add=1, shape=1)
                else:
                    error.append(i)

            if error:
                raise ValueError("关联复制文件未找到母体文件,复制文件命名要求 ['*_env_pxy#'].")
            else:
                cmds.select(clear=1)