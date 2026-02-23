# -*- coding: utf-8 -*-

import os
import json
import logging
import maya.cmds as cmds
import maya.mel as mel
from core import interface

LOG = logging.getLogger("materials")


def materialsJson(mode=None):
    # 服务日期
    if not interface.license():
        LOG.warning(u'到期不在提供服务.')
        return

    # file
    mjson = cmds.internalVar(uad=True) + 'scripts/materials.json'
    mfile = cmds.internalVar(uad=True) + 'scripts/materials.ma'

    # mode
    if mode == 'export':
        materials = cmds.ls(materials=1)
        mdict = {}
        for material in materials:
            cmds.hyperShade(objects=material)
            objs = cmds.ls(sl=1)
            if objs:
                mdict[material] = objs
        if mdict:
            # write mat json file
            with open(mjson, 'w') as fo:
                fo.write(json.dumps(mdict, indent=4))

            # export shanding file
            mat = []
            for k in mdict:
                mat.append(k)
            cmds.select(mat, r=1)
            cmds.file(mfile, op="v=0;p=17;f=0", typ="mayaAscii", pr=1, es=1, f=1)
            LOG.info(u'成功导出材质球与模型关联信息')
        else:
            LOG.warning(u'未找到可以输出的模型数据')
    elif mode == 'import':
        meshs = cmds.ls(type=['mesh'])
        if not meshs:
            LOG.warning(u"场景内未发现模型,请打开同任务不同组的文件再进行材质球导入")
            return

        if os.path.exists(mjson) and os.path.exists(mfile):
            # open json text
            with open(mjson, 'r') as fo:
                text = fo.read()
                mdict = json.loads(text)

            # delete objExists material
            for k, v in mdict.items():
                if cmds.objExists(k):
                    try:
                        cmds.delete(k)
                    except:
                        pass
            # import material file
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')
            cmds.file(mfile,
                      i=1,
                      type="mayaAscii",
                      ignoreVersion=1,
                      ra=1,
                      mergeNamespacesOnClash=1,
                      namespace=":",
                      options="v=0;",
                      pr=1,
                      importTimeRange="combine")

            # add material json
            temp = []
            data = []
            for k, v in mdict.items():
                temp.append(1)
                try:
                    cmds.select(v)
                    cmds.hyperShade(assign=k)
                except:
                    data.append(1)
                    LOG.warning(u'传递失败' + str(v))
            # print
            if sum(temp) == sum(data):
                # delete imported material
                for k, v in mdict.items():
                    if cmds.objExists(k):
                        cmds.delete(k)
                mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')
                LOG.warning(u'导入材质球与模型关联信息全部失败')
            else:
                if sum(data):
                    LOG.warning(u'导入材质球与模型关联信息部分失败,请查阅上述详细警告信息')
                else:
                    LOG.info(u'成功导入全部材质球与模型关联信息')
        else:
            LOG.warning(u"请先打开 ['srf'] 组的文件再导出材质球关联信息")