# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNucleusParamsRules(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.4
    label = '验证：解算器参数规则'

    def process(self, **kwargs):
        self.hdict = {
            "connect": {
                "hierarchy": "hairNodeNUL",
                "objects": {}
            },
            "enable": {
                "hierarchy": "hairCurveNUL",
                "objects": []
            },
            "startFrame": {
                "hierarchy": "hairCurveNUL",
                "objects": []
            }
        }

        # hairNodeNUL/子集个数判断
        nucleus = cmds.ls(type=['nucleus'], l=1)
        if nucleus:
            for i in nucleus:
                k = cmds.connectionInfo(i + '.enable', sourceFromDestination=1)
                if k:
                    self.hdict['connect']['objects'][k] = i + '.enable'
                else:
                    if cmds.getAttr(i + '.enable'):
                        self.hdict['enable']['objects'].append(i)
                    elif cmds.getAttr(i + '.startFrame') != 999.0:
                        self.hdict['startFrame']['objects'].append(i)

        if self.hdict['connect']['objects']:
            raise ValueError("解算器开关禁止关联.\n"
                             "单击['repair']按钮自动完成错误修复(c).")

        if self.hdict['enable']['objects']:
            raise ValueError("解算器开关参数错误.\n"
                             "单击['repair']按钮自动完成错误修复(0).")

        if self.hdict['startFrame']['objects']:
            raise ValueError("解算器起始帧参数错误.\n"
                             "单击['repair']按钮自动完成错误修复(999).")

    def repair(self, args):
        if self.hdict['connect']['objects']:
            for k, v in self.hdict['connect']['objects'].items():
                cmds.disconnectAttr(k, v)
        elif self.hdict['enable']['objects']:
            for i in self.hdict['enable']['objects']:
                cmds.setAttr(i + '.enable', 0)
        elif self.hdict['startFrame']['objects']:
            for i in self.hdict['startFrame']['objects']:
                cmds.setAttr(i + '.startFrame', 999)