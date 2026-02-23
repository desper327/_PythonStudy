# -*- coding: utf-8 -*-

import datetime
import maya.cmds as cmds
from PySide2 import QtGui
import envpath


def copyright():
    path = envpath.ROOTPATH
    if 'Y:\\Devkit\\Pipilu_v' in path:
        name = 'PiPiLu'
    elif 'J:\\Devkit\\Pipilu_v' in path:
        name = 'PiPiLu'
    elif '\\ChuangGu_v' in path:
        name = 'ChuangGu'
    else:
        name = 'ChunDevkit'
    year = datetime.datetime.now().year
    text = 'Copyright 2021-{0} {1},Inc.All rights reserved.'.format(year, name)
    return text


def license():
    path = envpath.ROOTPATH
    if 'Y:\\Devkit\\Pipilu_v' in path:
        defdate = 20240229
    elif 'J:\\Devkit\\Pipilu_v' in path:
        defdate = 20230930
    elif '\\ChuangGu_v' in path:
        defdate = 20231001
    else:
        defdate = 20231001
    nowdate = int(cmds.date(d=1).replace('/', ''))
    if defdate > nowdate:
        return True
    else:
        return False


def scriptEditor(instance, mode, text):
    font = QtGui.QFont()
    font.setPointSize(10)
    instance.setFont(font)
    instance.setText(mode.capitalize() + ': ' + text)
    if mode == 'result':
        instance.setStyleSheet('color: rgb(75, 175, 75)')
    elif mode == 'warning':
        instance.setStyleSheet('color: rgb(175, 175, 75)')
    elif mode == 'error':
        instance.setStyleSheet('color: rgb(175, 75, 75)')
    elif mode in ['command', 'repair', 'ignore']:
        instance.setStyleSheet('color: rgb(150, 75, 150)')
    elif mode in ['submit', 'dailies', 'publish']:
        instance.setStyleSheet('color: rgb(75, 150, 75)')
    else:
        instance.setStyleSheet('color: rgb(150, 150, 150)')