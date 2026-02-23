# -*- coding: utf-8 -*-

from stat import S_IWUSR, S_IREAD
from functools import partial
import maya.mel as mel
import maya.cmds as cmds
# import pymel.core as pm
import os
import json


def startup(**kwargs):
    plugins = ['unknown', 'malicious', 'change']
    scenes = ['SceneOpened', 'SceneSaved']
    rDict = {}
    for scene in kwargs.keys():
        if scene in scenes:
            rDict[scene]={}
            if kwargs[scene]:
                for plug in kwargs[scene]:
                    if plug in plugins:
                        rDict[scene][plug]=True
                        instance = eval('M'+plug+'()')
                        cmds.scriptJob(event=[scene, partial(instance.default)],protected=True)
                    else:
                        rDict[scene][plug] = False
    print('removes[2.0.0]:'+json.dumps(rDict, indent=4))


class Munknown(object):
    def default(self):
        self.unknownNode()
        self.unknownPlugin()

    def unknownNode(self):
        unknown = cmds.ls(type=["unknown", "unknownDag"])
        if unknown:
            cmds.lockNode(unknown, l=0)
            cmds.delete(unknown)

    def unknownPlugin(self):
        unknownPlugin = cmds.unknownPlugin(q=1, l=1)
        if unknownPlugin:
            for iunknownPlugin in unknownPlugin:
                if cmds.pluginInfo(iunknownPlugin, q=1, loaded=1):
                    cmds.unloadPlugin(iunknownPlugin, f=1)
                cmds.unknownPlugin(iunknownPlugin, r=1)
            print(u'remove unused unknown nodes and plugin...')


class Mmalicious(object):
    def __init__(self):
        self.forces = ['leukocyte.antivirus()', 'autoUpdatoAttrEnd()', 'look()', 'sysytenasdasdfsadfsdaf_dsfsdfaasd']
        self.malicious = ['MayaMelUIConfigurationFile', 'sysytenasdasdfsadfsdaf_dsfsdfaasd', 'script', 'breed_gene', 'vaccine_gene']

    def default(self):
        self.china()

    def china(self):
        mel.eval('global proc autoUpdatoAttrEnd(){}')
        mel.eval('global proc look(){}')
        mel.eval('global int $autoUpdateAttrEd_aoto_int=1;')

        department = [0]
        data = []

        # 获取工作脚本
        scriptJobs = cmds.scriptJob(listJobs=1)
        for iscriptJob in scriptJobs:
            for iforce in self.forces:
                if iforce in iscriptJob:
                    # 终止工作脚本进程
                    index = int(iscriptJob.split(':')[0])
                    cmds.scriptJob(kill=index, force=1)

        # 获取脚本
        scripts = cmds.ls(type='script')
        if scripts:
            # 打开或参考状态
            if cmds.file(q=1, reference=1):
                department.append(1)

            # 删除/复写恶意脚本
            for script in scripts:
                for maliciou in self.malicious:
                    lscript = script.split(':')[-1]
                    if maliciou in lscript:
                        # 镜头
                        if cmds.referenceQuery(script, isNodeReferenced=1) == 1:
                            cmds.scriptNode(script, e=1, beforeScript='')
                            data.append('reference: ' + cmds.referenceQuery(script, filename=1).split('{')[0] + '\n')
                        # 资产
                        else:
                            if maliciou == 'script':
                                before = cmds.getAttr(script + '.before')
                                if '////****************************************////' in before or before == '':
                                    data.append('remove: ' + script)
                                    cmds.delete(script)
                            else:
                                data.append('remove: ' + script)
                                cmds.delete(script)

        # 移除感染的userSetup.mel
        scriptsDir = cmds.internalVar(uad=True)+'scripts'
        userSetupMel=scriptsDir+'/userSetup.mel'
        if os.path.exists(userSetupMel):
            with open(userSetupMel, 'r') as fo:
                text = fo.read()

            if all([len(text) >= 4118,
                    '// Maya Mel UI Configuration File.Maya Mel UI Configuration File..\n// \n//\n//  This script is machine generated.  Edit at your own risk' in text,
                    'string $chengxu' in text]):
                os.chmod(userSetupMel, S_IWUSR | S_IREAD)
                os.remove(userSetupMel)
                data.append('deleted: '+userSetupMel)

        # 移除感染的userSetup.py
        userSetupPy=scriptsDir+'/userSetup.py'
        if os.path.exists(userSetupPy):
            with open(userSetupMel, 'r') as fo:
                text = fo.read()

            if 'leukocyte.occupation()' in text:
                os.chmod(userSetupPy, S_IWUSR | S_IREAD)
                os.remove(userSetupPy)
                data.append('deleted: ' + userSetupPy)
                files = ['vaccine.py', 'vaccine.pyc']

                # 删除vaccine文件
                for ifile in files:
                    vaccine = scriptsDir + '/'+ifile
                    if os.path.exists(vaccine):
                        os.chmod(vaccine, S_IWUSR | S_IREAD)
                        os.remove(vaccine)
                        data.append('deleted: ' + vaccine)

        # 部门提示
        if sum(department):
            data = list(set(data))
            if data:
                # 镜头部门
                data.append(u'\n提示:\n'
                            u'当前打开的文件已经移除恶意脚本\n'
                            u'参考文件内部存在恶意脚本即使不删除也不会造成当前文件让Maya死机的情况\n'
                            u'方案:\n'
                            u'如果想移除参考文件内部的恶意脚本\n'
                            u'按照弹窗文件地址逐一打开,再次保存即可\n'
                            u'\nTip:\n'
                            u'The currently open file has removed the malicious script\n'
                            u'The presence of a malicious script inside the reference file does not cause the current file to crash Maya even if it is not deleted\n'
                            u'Solution:\n'
                            u'If you want to remove malicious scripts from inside the reference file\n'
                            u'Open the file one by one according to the address of the pop-up window, and save it again\n')
                cmds.confirmDialog(title=u'Warning finds malicious script',
                                   message='\n'.join(data),
                                   button=[u'Continue to work'], defaultButton=u'Continue to work')
        else:
            if data:
                # 资产部门
                data.append(u'\n提示:\n'
                            u'当前打开的文件已经移除恶意脚本\n'
                            u'\nTip:\n'
                            u'The currently open file has removed the malicious script\n')
                cmds.confirmDialog(title=u'Warning finds malicious script',
                                   message='\n'.join(data),
                                   button=[u'Continue to work'], defaultButton=u'Continue to work')


class Mchange(object):
    def default(self):
        self.onModelChange3dc()
        self.functionSelComAt()
        self.lockUnpublished()

    def onModelChange3dc(self):
        script = cmds.ls(type=['script'])
        if script:
            for i in script:
                fixing = False
                expression_str = cmds.getAttr(i + '.before')
                expression_lines = []
                for line in expression_str.split('\n'):
                    if '-editorChanged "onModelChange3dc"' in line:
                        fixing = True
                        continue
                    expression_lines.append(line)
                fixed_expression = '\n'.join(expression_lines)
                if fixing:
                    cmds.setAttr(i + '.before', fixed_expression, type='string')

    def functionSelComAt(self):
        for editor in cmds.lsUI(editors=True):
            if not cmds.outlinerEditor(editor, query=True, exists=True):
                continue
            cmd = cmds.outlinerEditor(editor, query=True, selectCommand=True)
            if not cmd or not cmd.startswith('<function selCom at '):
                continue
            cmds.outlinerEditor(editor, edit=True, selectCommand='print("")')

    def lockUnpublished(self):
        objs = ['initialShadingGroup', 'initialParticleSE']
        for obj in objs:
            v = cmds.lockNode(obj, q=1, lu=True)
            if v[0]:
                cmds.lockNode(obj, lu=False)