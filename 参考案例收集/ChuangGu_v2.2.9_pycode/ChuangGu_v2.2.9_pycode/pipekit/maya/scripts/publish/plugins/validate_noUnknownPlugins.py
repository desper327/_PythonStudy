# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoUnknownPlugins(plugin.Validator):
    ''' Checks that there are no unknown plug-ins. '''
    order = plugin.Validator.order + 3.0
    label = '验证：没有未知插件'

    def process(self, **kwargs):
        """Process all the nodes in the instance"""
        unknown_plugins = cmds.unknownPlugin(query=True, list=True)
        
        if unknown_plugins:
            if 'stereoCamera' in unknown_plugins:
                unknown_plugins.remove('stereoCamera')
        
        if unknown_plugins:
            raise ValueError("找到未知插件: {}".format(unknown_plugins))
    
    def repair(self, args):
        unknown_plugins = cmds.unknownPlugin(query=True, list=True)
        if unknown_plugins:
            for unknown in unknown_plugins:
                if cmds.pluginInfo(unknown, q=1, loaded=1):
                    cmds.unloadPlugin(unknown, f=1)
                cmds.unknownPlugin(unknown, remove=True)