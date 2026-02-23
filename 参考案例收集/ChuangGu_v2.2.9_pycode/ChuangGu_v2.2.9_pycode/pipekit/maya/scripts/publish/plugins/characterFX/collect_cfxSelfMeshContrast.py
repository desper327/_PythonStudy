# -*- coding: utf-8 -*-

from publish import plugin
import maya.cmds as cmds


class CollectCfxSelfMeshContrast(plugin.MayaCollector):
    '''ntegrate the extracted '''
    order = plugin.MayaCollector.order + 2.0
    label = '收集：ClothMeshNUL与ClothNUL层级对比'
    optional = True
    actions = ['select']

    def process(self, **kwargs):
        # srfNUL
        if not cmds.objExists('clothMeshNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

        self.hdict = {
            "missed": {
                "objects": []
            },
            "index": {
                "objects": []
            },
            "count": {
                "objects": []
            }
        }

        # simNUL
        fx2Cloths = cmds.filterExpand('clothMeshNUL', ex=1, sm=12)
        if fx2Cloths:
            srfCloths= cmds.filterExpand('clothNUL', ex=1, sm=12)
            if not srfCloths:
                self.hdict['missed']['objects'].append('clothNUL')
            else:
                if len(fx2Cloths) != len(srfCloths):
                    self.hdict['index']['objects'].extend(['clothNUL', 'clothMeshNUL'])
                else:
                    for i in range(len(fx2Cloths)):
                        fx2Shape = cmds.listRelatives(fx2Cloths[i], shapes=1, path=1, ni=1)
                        fx2Count = cmds.polyEvaluate(fx2Shape[0], f=1)
                        srfShape = cmds.listRelatives(srfCloths[i], shapes=1, path=1, ni=1)
                        srfCount = cmds.polyEvaluate(srfShape[0], f=1)
                        if fx2Count != srfCount:
                            self.hdict['count']['objects'].extend([fx2Cloths[i], srfCloths[i]])

        if self.hdict['missed']['objects']:
            raise ValueError("clothNUL总组下丢失布料模型.")
        elif self.hdict['index']['objects']:
            raise ValueError("对应组 {} 下子集布料模型总体个数不一致.".format(self.hdict['index']['objects']))
        elif self.hdict['count']['objects']:
            raise ValueError("对应组 {} 下子集布料模型单体面数不一致.".format(self.hdict['count']['objects']))

    def select(self):
        if self.hdict['missed']['objects']:
            cmds.select(self.hdict['missed']['objects'], r=1)
        elif self.hdict['index']['objects']:
            cmds.select(self.hdict['index']['objects'], r=1)
        elif self.hdict['count']['objects']:
            cmds.select(self.hdict['count']['objects'], r=1)