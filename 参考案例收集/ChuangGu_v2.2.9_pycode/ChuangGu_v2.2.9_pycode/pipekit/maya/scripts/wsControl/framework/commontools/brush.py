RELATIVE = 0
SUFFIX = None
ICON = 'SHAPESBrush.svg'
TOOLTIP = 'SHAPESBrush'

import maya.cmds as cmds
import maya.mel as mel


def main():
    if not cmds.pluginInfo('SHAPESBrush.mll', q=1, loaded=1):
        cmds.loadPlugin('SHAPESBrush.mll')
    mel.eval('SHAPESBrushToolCtx')