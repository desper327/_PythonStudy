# -*- coding: utf-8 -*-

from publish import plugin
import maya.cmds as cmds


class ExtractTemplatePose(plugin.MayaExtractor):
    label = '提取：绑定的姿势'

    def process(self, **kwargs):
        self.commands = []
        shapes = cmds.ls(type=['nurbsCurve'])
        if not shapes:
            pass
        else:
            curves = []
            for shape in shapes:
                obj = cmds.listRelatives(shape, p=1)[0]
                if 'ctrlBox' in obj:
                    pass
                else:
                    if obj not in curves:
                        curves.append(obj)
                        attrs = cmds.listAttr(obj, unlocked=True, keyable=True)
                        if attrs:
                            for attr in attrs:
                                sfd = cmds.connectionInfo(obj + '.' + attr, sourceFromDestination=True)
                                if not sfd:
                                    if 'translate' in attr or 'rotate' in attr or 'scale' in attr:
                                        v = cmds.getAttr(obj + '.' + attr)
                                        if 'translate' in attr or 'rotate' in attr:
                                            if v != 0.0:
                                                self.commands.append('cmds.setAttr(\'' + obj + '.' + attr + '\', 0)')
                                        if 'scale' in attr:
                                            if v != 1.0:
                                                self.commands.append('cmds.setAttr(\'' + obj + '.' + attr + '\', 1.0)')

        if self.commands:
            raise ValueError('绑定不是初始姿势.')

    def repair(self, args):
        if self.commands:
            for command in self.commands:
                eval(command)