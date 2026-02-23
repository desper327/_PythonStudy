# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
from publish import plugin


class ValidateSceneSaved(plugin.Validator):
    ''' Checks that the scene is saved. '''
    
    order = plugin.Validator.order + 5.0
    label = '验证：场景变动保存'

    def process(self, **kwargs):
        if cmds.file(q=True, modified=True):
            raise Exception('场景有未保存的更改.')

    def repair(self, args):
        if not cmds.file(sceneName=True, query=True):
            mel.eval('SaveSceneAs')
        else:
            cmds.file(save=True)