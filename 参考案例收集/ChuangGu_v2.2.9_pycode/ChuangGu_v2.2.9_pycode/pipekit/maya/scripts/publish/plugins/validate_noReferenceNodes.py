# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoReferenceNodes(plugin.Validator):
    ''' Validate that there are no reference nodes in the scene. '''
    
    label = '验证：没有引用节点'
    order = plugin.Validator.order - 1.5
    ignoreType = ['shots', 'asm']

    def process(self, **kwargs):
        ''' Process all the transform nodes in the instance. '''
        rns = cmds.ls(type='reference')
        if rns:
            raise ValueError("存在 {} 个引用文件.".format(len(rns)))

        cmds.namespace(set=':')
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        namespaces.remove('shared')
        namespaces.remove('UI')
        if namespaces:
            raise ValueError("存在 {} 个空间字符.".format(len(namespaces)))

    def repair(self, args):
        ''' Remove references. '''
        rns = cmds.ls(type='reference')
        for rn in rns:
            try:
                cmds.file(removeReference=True, referenceNode=rn)
            except RuntimeError:
                pass

        fosters = cmds.ls(type='fosterParent')
        if fosters:
            cmds.delete(fosters)

        cmds.namespace(set=':')
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        namespaces.remove('shared')
        namespaces.remove('UI')
        for ns in namespaces:
            cmds.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)

        for rn in rns:
            if cmds.objExists(rn):
                cmds.lockNode(rn, lock=False)
                cmds.delete(rn)