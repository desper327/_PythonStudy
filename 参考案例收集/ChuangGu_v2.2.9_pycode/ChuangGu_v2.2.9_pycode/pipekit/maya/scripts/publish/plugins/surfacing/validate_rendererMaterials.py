# -*- coding: utf-8 -*-

import time
from publish import plugin
import maya.cmds as cmds


class ValidateRendererMaterials(plugin.Validator):
    ''' Check there are no mesh items with default "Lambert1" '''
    label = '验证：渲染器自身材质球'
    actions = ['select']

    def process(self, **kwargs):
        category = kwargs['category']
        instance = kwargs['instance']
        render = kwargs['render']
        if 'Redshift' in render:
            matType = 'Redshift'
        elif 'Arnold' in render:
            matType = 'ai'
        else:
            matType = ''

        emptyMats = []
        groupMats = []
        errorMats = []
        self.error = []
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复.')
        else:
            meshes = cmds.filterExpand('srfNUL', ex=1, sm=12)
            if not meshes:
                raise ValueError("Geometry总组下未找到任何模型,请将模型存放至 ['srfNUL'] 对应组内.")
            else:
                instance.label.setVisible(True)
                instance.label.setText('[验证：渲染器自身材质球]')
                instance.version.setVisible(False)
                instance.progressBar.setVisible(True)
                instance.progressBar.setStyleSheet('''
                    QProgressBar::chunk { 
                        background-color: rgb(100,100,100); 
                    }
                ''')

                materials = cmds.ls(materials=1)
                SG = []
                n = 0
                m = 100.0 / len(materials)
                # 得到SG节点,模型是否选面添加材质球
                for mat in materials:
                    time.sleep(0.05)
                    n += 1
                    v = n * m
                    if matType in cmds.nodeType(mat):
                        SE = cmds.listConnections(mat, type='shadingEngine')
                        if SE:
                            SG.append(SE)
                            groupIds = cmds.listConnections(SE, type='groupId')
                            if groupIds:
                                groupMats.extend(groupIds)
                    instance.progressBar.setValue(v/2.0)

                # 模型是否添加渲染器材质球
                sgMeshs = []
                for i in SG:
                    time.sleep(0.05)
                    n += 1
                    v = n * m
                    objs = cmds.listConnections(i, type='mesh')
                    if objs:
                        sgMeshs.extend(objs)
                    instance.progressBar.setValue(v/2.0)
                miss = list(set(meshes) - set(sgMeshs))
                if miss:
                    errorMats.extend(miss)
                '''
                m = 100.0 / len(meshes)
                for mesh in meshes:
                    n += 1
                    v = n * m
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
                        groupIds = cmds.listConnections(shape, type='groupId')
                        if groupIds:
                            groupMats.append(mesh)
                        else:
                            shadingEngines = list(set(shadingEngines))
                            materials = cmds.ls(cmds.listConnections(shadingEngines), materials=1)
                            for material in materials:
                                matNT = cmds.nodeType(material)
                                if matNT in ['displacementShader']:
                                    pass
                                else:
                                    if matType not in matNT:
                                        errorMats.append(mesh)
                    instance.progressBar.setValue(v)
                '''
                time.sleep(0.5)
                instance.label.setVisible(True)
                instance.version.setVisible(True)
                instance.progressBar.setVisible(False)

            if emptyMats:
                self.error = emptyMats
                raise RuntimeError('模型丢失材质球: {}.'.format(self.error))
            elif errorMats:
                if category in ['set']:
                    self.optional = True
                self.error = list(set(errorMats))
                raise RuntimeError('模型未添加 {0} 渲染器材质球: {1}.'.format(matType, self.error))
            elif groupMats:
                if category in ['set']:
                    self.optional = True
                self.error = list(set(groupMats))
                raise RuntimeError("建议不要选择面添加材质球.\n"
                                   "['set']资产类型允许跳过.\n"
                                   "['chr', 'prp', 'env']资产类型暂定不允许跳过.")

    def select(self):
        if self.error:
            cmds.select(self.error)