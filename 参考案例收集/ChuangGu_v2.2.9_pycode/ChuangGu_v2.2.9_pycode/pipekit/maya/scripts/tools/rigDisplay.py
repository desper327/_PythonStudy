# -*- coding: utf-8 -*-

import maya.cmds as cmds


class Rigging(object):
    def intermediateObjects(self, mode=True):
        # 节点
        intermediate = cmds.ls(shapes=True, intermediateObjects=False, long=True)
        if intermediate:
            future = cmds.listHistory(intermediate, future=True)
            for i in future:
                cmds.setAttr(i + '.isHistoricallyInteresting', mode)

    def joints(self, mode=True):
        # 骨骼
        if mode == True:
            v = 0
        elif mode == False:
            v = 2
        joints = cmds.ls(type=['joint'], l=1)
        for jnt in joints:
            cmds.setAttr(jnt + '.drawStyle', v)