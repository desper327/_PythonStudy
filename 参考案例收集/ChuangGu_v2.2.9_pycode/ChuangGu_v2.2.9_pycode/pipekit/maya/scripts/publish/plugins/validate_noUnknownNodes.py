# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoUnknownNodes(plugin.Validator):
    ''' Checks that there are no unknown nodes. '''
    order = plugin.Validator.order + 2.5
    label = '验证：没有未知节点'

    def process(self, **kwargs):
        """Process all the nodes in the instance"""
        unknown = cmds.ls(type=["unknown", "unknownDag"])
        if unknown:
            raise ValueError("找到未知节点: {}".format(unknown))
        
    def repair(self, args):
        unknown_nodes = cmds.ls(type=["unknown", "unknownDag"])
        if unknown_nodes:
            for node in unknown_nodes:
                cmds.lockNode(node, lock=False)
                cmds.delete(node)