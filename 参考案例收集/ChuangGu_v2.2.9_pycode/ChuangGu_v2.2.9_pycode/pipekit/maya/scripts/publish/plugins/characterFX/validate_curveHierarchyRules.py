# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateCurveHierarchyRules(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order + 0.3
    label = '验证：曲线层级规则'

    def process(self, **kwargs):
        if not cmds.objExists('hairFxNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

        self.hdict = {
            "rename": {
                "hierarchy": "hairNodeNUL",
                "objects": []
            },
            "exists": {
                "hierarchy": "hairCurveNUL",
                "objects": []
            },
            "alembic": {
                "hierarchy": "hairCurveNUL",
                "objects": []
            }
        }

        # hairNodeNUL/子集个数判断
        nodes = cmds.ls(type=['xgmPalette'], l=1)
        if nodes:
            crvs = cmds.listRelatives('hairCurveNUL', c=1)
            if crvs:
                for crv in crvs:
                    if crv.split('_')[-1] == 'OutputCurves':
                        dec = crv.replace('_OutputCurves', '_xgen_DES')
                        if not cmds.objExists(dec):
                            self.hdict['exists']['objects'].append(crv)
                        else:
                            crvShapes = cmds.listRelatives(crv, ad=1, type=['nurbsCurve'])
                            if not crvShapes:
                                self.hdict['alembic']['objects'].append(crv)
                    else:
                        self.hdict['rename']['objects'].append(crv)


        if self.hdict['rename']['objects']:
            raise ValueError("曲线输出组命名错误.\n"
                             "请到 ['hairCurveNUL'] 总组下对子集对象命名,请手动完成.\n"
                             "命名规则：{'DES': '部位名称_xgen_DES', 'GRP': '部位名称_OutputCurves'}.")

        if self.hdict['exists']['objects']:
            raise ValueError("Description文件丢失.\n"
                             "请到 ['xgmPalette'] 子集DES对象匹配命名.\n"
                             "命名规则：{'DES': '部位名称_xgen_DES', 'GRP': '部位名称_OutputCurves'}.")

        if self.hdict['alembic']['objects']:
            raise ValueError("曲线输出组下丢失曲线.\n"
                             "请到 {} 总组下手动完成删除或修改.".format(self.hdict['alembic']['objects']))