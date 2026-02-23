# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectExistsReference(plugin.MayaCollector):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.MayaCollector.order + 0.5
    label = '收集：场景内至少存在一个引用资产'

    def process(self, **kwargs):
        exists = []
        # ['chr', 'prp']
        reference = cmds.file(q=1, reference=1)
        if reference:
            exists.append(1)

        # ['set']
        assemblies = cmds.ls(assemblies=1)
        for i in assemblies:
            if cmds.nodeType(i) == 'assemblyReference':
                exists.append(1)

        if not exists:
            raise ValueError("场景内至少存在一个 ['chr', 'prp', 'set'] 类型的引用资产文件\n"
                             "请在右侧 [Chun Toolkit/Animation/PIPETOOLS] 菜单下单击(assets)工具创建引用资产")