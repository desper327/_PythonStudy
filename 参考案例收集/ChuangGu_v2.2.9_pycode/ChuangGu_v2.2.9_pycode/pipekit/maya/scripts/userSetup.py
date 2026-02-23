# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.utils as utils
from wsControl import toolkitMain
from startup import removes


def presets():
    # 修改Maya左下角图标
    cmds.help(popupMode=True)
    cmds.iconTextButton('mayaWebButton', e=1, image1="mayaWeb.png", c=toolkitMain.createChunToolkit)
    # 加载皮皮鲁工具集
    toolkitMain.createChunToolkit()
    # 加载恶意脚本查询
    # removes.startup(SceneOpened=['unknown', 'malicious', 'change'], SceneSaved=[])
    removes.startup(SceneOpened=['unknown', 'malicious', 'change'], SceneSaved=[])

utils.executeDeferred(presets)