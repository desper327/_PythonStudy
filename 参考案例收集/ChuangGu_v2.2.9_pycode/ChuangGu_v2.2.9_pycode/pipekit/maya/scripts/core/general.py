# -*- coding: utf-8 -*-

import maya.OpenMayaUI as omui
import shiboken2
from PySide2 import QtWidgets


class Mregister(object):
    def getMayaWin(self):
        pointer = omui.MQtUtil.mainWindow()
        return shiboken2.wrapInstance(long(pointer), QtWidgets.QWidget)