# -*- coding: utf-8 -*-

import os
import sys
import json
import maya.cmds as cmds
import maya.mel as mel


class Export(object):
    def __init__(self):
        self.mafile = sys.argv[-1]
        self.jsfile = self.mafile.rsplit('/', 1)[0] + '/__init__.json'

        # 加载插件
        plugins = ['gameFbxExporter.mll', 'AbcExport.mll', 'sceneAssembly.mll', 'gpuCache.mll', 'redshift4maya.mll']
        for plugin in plugins:
            try:
                if not cmds.pluginInfo(plugin, q=1, loaded=1):
                    cmds.loadPlugin(plugin)
            except:
                print('//Result: plug-ins {} skip.'.format(plugin))

        # 读取数据
        with open(self.jsfile, 'r') as fo:
            text = fo.read()
            self.itemDict = json.loads(text)

        # 定义参数
        self.setting = self.itemDict['setting']
        self.dirpath = self.setting['dirpath']
        self.project = self.setting['project']

    def alembicCmds(self, time, root, file):
        cmd = '-frameRange ' + str(time[0]) + ' ' + str(time[1])
        cmd += self.setting['abcParams']
        cmd += ' -root ' + root
        cmd += ' -file ' + file
        cmds.AbcExport(j=cmd)

    def exportCamera(self):
        camera = self.itemDict['camera'].keys()[0]
        # 导出偏移前摄像机
        mel.eval('FBXResetExport;')
        mel.eval('FBXExportBakeComplexAnimation -v true;')
        mel.eval('FBXExportBakeComplexStart -v ' + str(self.setting['timeSlider'][0]) + ';')
        mel.eval('FBXExportBakeComplexEnd -v ' + str(self.setting['timeSlider'][1]) + ';')
        mel.eval('FBXExportBakeComplexStep -v 1;')
        mel.eval('FBXExportInputConnections - v false')
        mel.eval('FBXExportBakeResampleAnimation - v true;')
        fbxfile = self.setting['dirpath'] + '/' + camera.replace('ani', 'cam') + '.fbx'
        cmds.select(camera, r=1)
        mel.eval('FBXExport -f "' + fbxfile + '" -s')
        print('//Result: export.camera')

    def exportAlembic(self):
        for k, v in self.itemDict['alembic'].items():
            cmds.refresh()
            # 优化输出
            for k0, vDict0 in self.itemDict['alembic'].items():
                rn = k0 + 'RN'
                if cmds.objExists(rn):
                    rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                    if k == k0:
                        cmds.setAttr(rootNUL + '.v', 1)
                    else:
                        cmds.setAttr(rootNUL + '.v', 0)
            
            category = v['category']
            stage = v['stage']
            namespace = v['namespace']
            if stage == 'anim':
                abctime = self.setting['animSlider']
            elif stage == 'cfx2':
                abctime = self.setting['cfx2Slider']

            # 渲染缓存
            print('//Result: export.start.ani {0} {1} ...'.format(k, abctime))
            root = namespace + ':srfNUL'
            file = self.dirpath + '/' + self.project + '_' + category + '_' + k + '_ani.abc'
            self.alembicCmds(abctime, root, file)
            print('//Result: export.ended.ani {0} {1}\n'.format(k, abctime))
            # 解算缓存
            if stage == 'cfx2':
                print('//Result: export.start.sim {0} {1} ...'.format(k, abctime))
                root = namespace + ':simNUL'
                file = self.dirpath + '/' + self.project + '_' + category + '_' + k + '_sim.abc'
                self.alembicCmds(abctime, root, file)
                print('//Result: export.ended.sim {0} {1}\n'.format(k, abctime))

        # 全部显示
        for k0, vDict0 in self.itemDict['alembic'].items():
            rn = k0 + 'RN'
            if cmds.objExists(rn):
                rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                cmds.setAttr(rootNUL + '.v', 1)
        print('//Result: export.alembic')

    def exportScene(self):
        nulls = []
        for vDict in self.itemDict['scene'].values():
            nulls.append(vDict['outliner'])
        if nulls:
            asmfile = self.dirpath + '/' + self.project + '_set_scene_ani.ma'
            cmds.select(nulls, r=1)
            # cmds.file(asmfile, f=1, typ='mayaAscii', es=1, ch=1, con=1, chn=1, eas=0, sh=1, pr=1)
            cmds.file(asmfile, force=1, options="v=0;", typ="mayaAscii", pr=1, es=1)
            print('//Result: export.scene')

    def apply(self):
        # 打开文件
        cmds.file(self.mafile, f=1, options="v=0;", esn=0, ignoreVersion=1, typ="mayaAscii", o=1)
        # 参数预设
        cmds.currentUnit(time=self.setting['playbackSpeed'])
        cmds.evaluationManager(mode=self.setting['evaluation'])
        print('//Result: {}'.format(self.setting['evaluation']))
        # 执行导出
        self.exportCamera()
        self.exportAlembic()
        self.exportScene()
        # 文件拷贝
        drive = self.setting['drive']
        if drive[0] != drive[1]:
            severDir = self.dirpath.replace(drive[1], drive[0])
            cmds.sysFile(severDir, makeDir=True)
            files = cmds.getFileList(folder=self.dirpath, filespec='*.*')
            if files:
                for i in files:
                    cmds.refresh()
                    cmds.sysFile(self.dirpath + '/' + i, copy=severDir + '/' + i)
                    print('//Result: copying {} to sever.\n'.format(i))
            os.startfile(severDir.rsplit('/', 1)[0])
        else:
            os.startfile(self.dirpath.rsplit('/', 1)[0])