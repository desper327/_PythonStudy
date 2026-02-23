# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectNoFrameHierarchy(plugin.MayaCollector):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.MayaCollector.order
    label = '收集：大纲层级框架'
    ignoreType = ['shots', 'asm']

    def process(self, **kwargs):
        self.category = kwargs['category']
        self.abbr = kwargs['department']
        nulls = []
        if self.category in ['chr', 'prp', 'veh']:
            nulls.extend(['srfNUL', 'defaultNUL', 'clothNUL', 'noRenderNUL'])
            if self.abbr == 'srf':
                nulls.append('Geometry')
            else:
                nulls.extend(['simNUL', 'hairGrmNUL', 'clothWpNUL'])
                if self.abbr in ['mod', 'rig']:
                    nulls.append('Geometry')
                    nulls.append('aniNUL')
                    if self.abbr == 'rig':
                        nulls.append('Group')
                        nulls.extend(['Main', 'MainExtra'])
                        if self.category == 'chr':
                            nulls.append('FaceGroup')
                        nulls.append('OtherGroup')
                elif self.abbr == 'cfx':
                    nulls.append('cfxNUL')
                    nulls.append('fx2NUL')
                    nulls.extend(['hairFxNUL', 'hairNodeNUL', 'hairRiggingNUL', 'hairSystemNUL', 'hairFollicleNUL', 'hairCurveNUL'])
                    nulls.extend(['clothFxNUL', 'clothMeshNUL', 'clothNodeNUL', 'clothConstraintNUL', 'clothColliderNUL', 'clothBaseNUL'])
        else:
            # ['set', 'env']
            nulls.extend(['Geometry', 'aniNUL', 'srfNUL', 'simNUL'])
            if self.category == 'set':
                if self.abbr in ['rig', 'srf']:
                    nulls.extend(['Group', 'Main', 'MainExtra', 'OtherGroup'])
        self.nulls = nulls

        # 输出结果
        error0 = []
        error1 = []

        for null in nulls:
            if len(cmds.ls('*|'+null)) > 1:
                error0.append(null)
            else:
                if not cmds.objExists(null):
                    error1.append(null)
        # raise RuntimeError('大纲内平行组,请手动删除多余平行组层级')
        if error0:
            raise RuntimeError('层级框架重名,请手动删除多余层级')
        elif len(error1) > 0:
            raise RuntimeError('缺少层级框架,单击 [repair] 按钮完成自动修复')

    def repair(self, args):
        geometry = cmds.ls('Geometry*')
        if len(geometry) > 1:
            raise ValueError('大纲内存在多个 {} ,无法自动完成修复功能,请手动删除重复物体.'.format(geometry))

        for null in self.nulls:
            if not cmds.objExists(null):
                cmds.group(em=1, n=null)
            else:
                if cmds.listRelatives(null, p=1, f=1):
                    cmds.parent(null, w=1)

        if self.category in ['chr', 'prp', 'veh']:
            cmds.parent('defaultNUL', 'clothNUL', 'noRenderNUL', 'srfNUL')
            if self.abbr == 'srf':
                cmds.parent('srfNUL', 'Geometry')
            else:
                cmds.parent('hairGrmNUL', 'clothWpNUL', 'simNUL')
                if self.abbr in ['mod', 'rig']:
                    cmds.parent('aniNUL', 'srfNUL', 'simNUL', 'Geometry')
                    if self.abbr == 'rig':
                        cmds.parent('MainExtra', 'Main')
                        if self.category == 'chr':
                            cmds.parent('Main', 'Geometry', 'FaceGroup', 'OtherGroup', 'Group')
                        else:
                            cmds.parent('Main', 'Geometry', 'OtherGroup', 'Group')
                elif self.abbr == 'cfx':
                    cmds.parent('hairFxNUL', 'clothFxNUL', 'fx2NUL')
                    cmds.parent('hairNodeNUL', 'hairRiggingNUL', 'hairSystemNUL', 'hairFollicleNUL', 'hairCurveNUL', 'hairFxNUL')
                    cmds.parent('clothMeshNUL', 'clothNodeNUL', 'clothConstraintNUL', 'clothColliderNUL', 'clothBaseNUL', 'clothFxNUL')
                    cmds.parent('srfNUL', 'simNUL', 'fx2NUL', 'cfxNUL')
        else:
            # ['set', 'env']
            cmds.parent('aniNUL', 'srfNUL', 'simNUL', 'Geometry')
            if self.category == 'set':
                if self.abbr in ['rig', 'srf']:
                    cmds.parent('MainExtra', 'Main')
                    cmds.parent('Main', 'Geometry', 'OtherGroup', 'Group')

        for null in self.nulls:
            if null == 'Geometry':
                continue
            else:
                if not cmds.listConnections(null):
                    cmds.connectAttr('Geometry.intermediateObject', null+'.intermediateObject', f=1)