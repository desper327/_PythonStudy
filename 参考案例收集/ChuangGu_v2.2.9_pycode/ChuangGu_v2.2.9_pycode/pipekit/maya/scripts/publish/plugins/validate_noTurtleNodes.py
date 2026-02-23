# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoTurtleNodes(plugin.Validator):
    ''' Checks that the turtle plug-in is disabled. '''
    order = plugin.Validator.order + 2.0
    label = '验证：没有海龟渲染器节点'

    def process(self, **kwargs):
        if not cmds.pluginInfo('Turtle.mll', loaded=True, q=True):
            return

        types = cmds.pluginInfo('Turtle.mll', dependNode=True, q=True)
        nodes = cmds.ls(type=types, long=True)

        if nodes:
            raise RuntimeError('Turtle插件已感染此场景.' )
        cmds.unloadPlugin('Turtle.mll')


    def repair(self, args):
        types = cmds.pluginInfo('Turtle.mll', dependNode=True, q=True)
        nodes = cmds.ls(type=types, long=True)
        if nodes:
            cmds.lockNode(nodes, lock=False)
            cmds.delete(nodes)
            cmds.flushUndo()
        cmds.unloadPlugin('Turtle.mll')