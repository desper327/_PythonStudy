# -*- coding: utf-8 -*-

import os
import sys
import json
import maya.cmds as cmds


class Export(object):
    def __init__(self):
        self.mafile = sys.argv[-1]
        self.jsfile = self.mafile.rsplit('/', 1)[0] + '/__init__.json'

        # 加载插件
        plugins = ['AbcExport.mll', 'sceneAssembly.mll', 'gpuCache.mll', 'redshift4maya.mll']
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

    def exportAlembic(self):
        abctime = self.setting['animSlider']
        for k, v in self.itemDict['alembic'].items():
            cmds.refresh()
            # 优化输出
            for k0, vDict0 in self.itemDict['alembic'].items():
                rn = vDict0['category'] + '_' + k0 + 'RN'
                if cmds.objExists(rn):
                    rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                    if k == k0:
                        cmds.setAttr(rootNUL + '.v', 1)
                    else:
                        cmds.setAttr(rootNUL + '.v', 0)

                    fx2NUL = vDict0['category'] + '_' + k0 + ':fx2NUL'
                    if cmds.objExists(fx2NUL):
                        nucleus = cmds.listRelatives(fx2NUL, ad=1, type=['nucleus'])
                        if nucleus:
                            if k == k0:
                                for i in nucleus:
                                    cmds.setAttr(i + '.enable', 1)
                                    cmds.setAttr(i + '.startFrame', 50)
                            else:
                                for i in nucleus:
                                    cmds.setAttr(i + '.enable', 0)
                                    cmds.setAttr(i + '.startFrame', 999)

            category = v['category']
            stage = v['stage']
            namespace = v['namespace']

            subdir = self.dirpath + '/' + category + '_' + k
            # 毛发缓存
            if stage in ['hair', 'cfx2']:
                roots = cmds.listRelatives(namespace + ':hairCurveNUL', c=1)
                if roots:
                    cmds.sysFile(subdir, makeDir=True)
                    for root in roots:
                        print('//Result: start.sim.hair {0} {1} ...'.format(root, abctime))
                        crvfile = subdir + '/' + root.split(':')[-1] + '.abc'
                        self.alembicCmds(abctime, root, crvfile)
                        print('//Result: ended.sim.hair {0} {1}'.format(root, abctime))

            # 布料缓存
            if stage in ['cloth', 'cfx2']:
                print('//Result: start.sim.cloth {0} {1} ...'.format(k, abctime))
                cmds.sysFile(subdir, makeDir=True)
                root = namespace + ':srfNUL'
                simfile = subdir + '/' + self.project + '_' + category + '_' + k + '_ani.abc'
                self.alembicCmds(abctime, root, simfile)
                print('//Result: ended.sim.cloth {0} {1}\n'.format(k, abctime))

        # 全部显示
        for k0, vDict0 in self.itemDict['alembic'].items():
            rn = vDict0['category'] + '_' + k0 + 'RN'
            if cmds.objExists(rn):
                rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                cmds.setAttr(rootNUL + '.v', 1)
        print('//Result: export.alembic')

    def apply(self):
        # 打开文件
        cmds.file(self.mafile, f=1, options="v=0;", esn=0, ignoreVersion=1, typ="mayaAscii", o=1)
        # 参数预设
        cmds.currentUnit(time=self.setting['playbackSpeed'])
        cmds.evaluationManager(mode=self.setting['evaluation'])
        print('//Result: {}'.format(self.setting['evaluation']))
        # 执行导出
        self.exportAlembic()
        # 文件拷贝
        drive = self.setting['drive']
        if drive[0] != drive[1]:
            severDir = self.dirpath.replace(drive[1], drive[0])
            files = cmds.getFileList(folder=self.dirpath, filespec='*.*')
            if files:
                for file in files:
                    cmds.refresh()
                    cmds.sysFile(self.dirpath + '/' + file, copy=severDir + '/' + file)
                    print('//Result: copy2server {0}\n'.format(file))

            dirs = cmds.getFileList(folder=self.dirpath, filespec='*.')
            if dirs:
                for dir in dirs:
                    cacheSubDir = self.dirpath + '/' + dir
                    files = cmds.getFileList(folder=cacheSubDir, filespec='*.*')
                    if files:
                        severSubDir = severDir + '/' + dir
                        cmds.sysFile(severSubDir, makeDir=True)
                        for i in files:
                            cmds.refresh()
                            cmds.sysFile(cacheSubDir + '/' + i, copy=severSubDir + '/' + i)
                            print('//Result: copy2server {0} {1}\n'.format(dir, i))
            os.startfile(severDir.rsplit('/', 1)[0])
        else:
            os.startfile(self.dirpath.rsplit('/', 1)[0])