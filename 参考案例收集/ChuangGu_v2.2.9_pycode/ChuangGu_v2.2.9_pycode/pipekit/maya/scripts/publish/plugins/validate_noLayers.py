# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoLayers(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 1.5
    label = '验证：场景中没有图层'
    ignoreType = ['shots']
    
    def getDisplayLayers(self):
        layers = cmds.ls(type='displayLayer')
        for layer in layers:
            if 'defaultLayer' in layer:
                layers.remove(layer)
        layers = [x for x in layers if not cmds.referenceQuery(x, isNodeReferenced=True)]
        return layers
    
    def getRenderLayers(self):
        layers = cmds.ls(type='renderLayer')
        for layer in layers:
            if 'defaultRenderLayer' in layer:
                layers.remove(layer)
        layers = [x for x in layers if not cmds.referenceQuery(x, isNodeReferenced=True)]
        layers = [x for x in layers if 'defaultRenderLayer' not in x]
        return layers
    
    def process(self, **kwargs):
        layers = self.getDisplayLayers()
        rlayers = self.getRenderLayers()
        
        if layers or rlayers:
            raise RuntimeError('在场景中发现的显示或渲染层.')

    def repair(self, args):
        layers = self.getDisplayLayers()
        if layers:
            cmds.delete(layers)
            
        rlayers = self.getRenderLayers()
        if rlayers:
            cmds.delete(layers)