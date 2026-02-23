# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectRenderUsing(plugin.Collector):
    ''' Checks that there are no display layers in the current scene. '''
    label = '收集：渲染器应用'

    def process(self, **kwargs):
        self.render = kwargs['render'][0].lower()
        if cmds.getAttr("defaultRenderGlobals.currentRenderer") != self.render:
            raise ValueError('项目渲染器应为 {} '.format(self.render))

    def repair(self, args):
        if self.render == 'redshift':
            try:
                if not cmds.pluginInfo('redshift4maya.mll', q=1, loaded=1):
                    cmds.loadPlugin('redshift4maya.mll')
                cmds.setAttr("defaultRenderGlobals.currentRenderer", self.render, type="string")
            except:
                raise ValueError('请安装或加载 {} 渲染器'.format(self.render))
        elif self.render == 'arnold':
            cmds.setAttr("defaultRenderGlobals.currentRenderer", self.render, type="string")