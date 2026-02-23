# -*- coding: utf-8 -*-

import re
import os
import json
from PySide2 import QtCore
import maya.cmds as cmds
import maya.mel as mel
import envpath


class SubmitShots(QtCore.QObject):
    SigScriptEditor = QtCore.Signal(str, str)

    def __init__(self, **kwargs):
        super(SubmitShots, self).__init__()

        # 传参
        self.instance = kwargs['instance']
        self.category = kwargs['category']
        self.abbr = kwargs['abbr']
        self.format = kwargs['format']
        dirpath = kwargs['dirpath']
        self.submit = kwargs['submit']
        self.taskDir = dirpath.rsplit('/', 1)[0]
        if self.submit == 'dailies':
            if 'series' in dirpath:
                self.dirpath = dirpath.replace('series', 'dailies').replace('shots', 'series')
            elif 'film' in dirpath:
                self.dirpath = dirpath.replace('film', 'dailies').replace('shots', 'film')
        elif self.submit == 'publish':
                self.dirpath = dirpath + '/publish'
        self.task = kwargs['task']
        self.comment = kwargs['comment']
        self.project = kwargs['project']

        # 获取版本号及版本路径
        dirs = cmds.getFileList(folder=self.dirpath, filespec='v*.')
        if not dirs:
            self.ver = 'v001'
            self.verDir = self.dirpath + '/' + self.ver
            self.oldVerDir = None
        else:
            dirs.sort(reverse=False)
            count = int(re.sub('\D', '', dirs[-1])) + 1
            self.ver = 'v' + str(count).zfill(3)
            self.verDir = self.dirpath + '/' + self.ver
            self.oldVerDir = self.dirpath + '/' + dirs[-1]

        if not cmds.objExists('persp.version'):
            cmds.addAttr('persp', ln='version', dt='string')
        cmds.setAttr('persp.version', self.ver, type='string')

    def versionData(self):
        '''
        jfile: */v001/task_mod.json
        {
            "v001": {
                "stage": ["done", "tangchun", "2020/04/04 10:00:00"],
                "comment": "",
                "application": "Maya 2020",
                "assets":{
                    "chr":{
                        "task":{
                            "file": none, "nsid: [0, 1]"
                        }
                    },
                    "prp":{
                        "task":{
                            "file": none, "nsid: [0, 1]"
                        }
                    }
                    "set":{
                        "task":{
                            "file": none, "nsid: [0, 1]"
                        }
                    }
                },
                "shots":{
                    "camera": ""
                }

            }
        }
        '''

        # 定义json字典
        camera = cmds.lookThru(q=True)
        fps = cmds.currentUnit(q=1, time=1)
        if fps == 'film':
            fps = '24fps'
        elif fps == 'pal':
            fps = '25fps'
        elif fps == 'ntscf':
            fps = '60fps'
        tdict = {
            'application': 'Maya ' + str(cmds.about(api=1))[:4] + '.' + str(cmds.about(api=1))[5:6],
            'comment': self.comment,
            "ctoolkit": envpath.CTOOLKIT,
            'stage': ['done', None, os.environ['USERNAME'].lower(), cmds.date()],
            "assets": {
                "chr": {},
                "prp": {},
                "set": {},
                'old': {}
            },
            "shots": {
                "camera": {
                    "lookThru": camera
                },
                "resolution": [cmds.getAttr('defaultResolution.width'), cmds.getAttr('defaultResolution.height')],
                "timeSlider": [cmds.playbackOptions(q=1, minTime=1), cmds.playbackOptions(q=1, maxTime=1)],
                "playbackSpeed": fps,
                "evaluation": cmds.evaluationManager(q=1, mode=1)[0]
            },
        }

        # 摄像机默认参数
        options = {
            'displayFilmGate': 0,
            'displayResolution': 0,
            'displayGateMask': 0,
            'displayGateMaskOpacity': 0.70,
            'displayGateMaskColor': [0.5, 0.5, 0.5],
            'displayFieldChart': 0,
            'displaySafeAction': 0,
            'displaySafeTitle': 0,
            'displayFilmPivot': 0,
            'displayFilmOrigin': 0,
            'overscan': 1.0
        }
        for k, v in options.items():
            v = cmds.getAttr(camera + '.' + k)
            if type(v) == list:
                tdict['shots']['camera'][k] = v[0]
            else:
                tdict['shots']['camera'][k] = v

        # 获取['chr', 'prp']参考信息
        reference = cmds.file(q=1, reference=1)
        if reference:
            if self.abbr in ['lay', 'blk', 'ani']:
                istring = '/rig/publish/'
            elif self.abbr in ['sim']:
                istring = '/cfx/publish/'
            elif self.abbr in ['lgt']:
                istring = '/srf/publish/'

            reference.sort(reverse=False)
            for i in reference:
                rfn = cmds.referenceQuery(i, rfn=1)
                nsid = re.sub('\D', '', str(rfn).split('_')[-1])
                if not nsid:
                    nsid = 0
                else:
                    nsid = int(nsid)
                i = i.split('{')[0]
                array = i.split('/')
                if '/assets/chr/' in i or '/assets/prp/' in i:
                    if istring in i:
                        task = array[4]
                        category = array[3]
                        if task not in tdict['assets'][category]:
                            tdict['assets'][category][task] = {
                                "nsid": [],
                                "file": i
                            }
                        tdict['assets'][category][task]['nsid'].append(nsid)
                else:
                    if self.abbr in ['lay', 'blk', 'ani']:
                        task = array[5]
                        if task not in tdict['assets']['old']:
                            tdict['assets']['old'][task] = {
                                "nsid": [],
                                "file": i
                            }
                        tdict['assets']['old'][task]['nsid'].append(nsid)

        # 获取['set']参考信息
        assemblies = cmds.ls(assemblies=1)
        for i in assemblies:
            if '_set_AR' in i:
                task = i.split('_')[0]
                if task not in tdict['assets']['set']:
                    tdict['assets']['set'][task] = {
                        "nsid": [],
                        "file": cmds.getAttr(i + '.definition')
                    }

                nsid = re.sub('\D', '', str(i.split('_')[-1]))
                if not nsid:
                    nsid = 0
                else:
                    nsid = int(nsid)
                tdict['assets']['set'][task]['nsid'].append(nsid)
        # 定义版本字典
        pdict = {}
        pdict[self.ver] = tdict
        return pdict

    def writeData(self, jsonname):
        fdict = {}
        if self.oldVerDir:
            oldfile = self.oldVerDir + '/' + jsonname
            if os.path.exists(oldfile):
                with open(oldfile, 'r') as fo:
                    text = fo.read()
                    tdict = json.loads(text)
                ver = tdict.keys()
                ver.sort(reverse=True)
                fdict[ver[0]] = tdict[ver[0]]

        vdict = self.versionData()
        fdict[vdict.keys()[0]] = vdict.values()[0]
        newfile = self.verDir + '/' + jsonname
        with open(newfile, 'w') as fo:
            fo.write(json.dumps(fdict, indent=4))

    def dailies(self):
        # 无选择物体进行拍屏
        cmds.select(clear=1)

        # 删除初始HUD
        if cmds.headsUpDisplay(listHeadsUpDisplays=True):
            for i in cmds.headsUpDisplay(listHeadsUpDisplays=True):
                cmds.headsUpDisplay(i, remove=True)

        # 生成头像
        # 摄像机默认参数
        camera = cmds.lookThru(q=True)
        options = {
            'displayFilmGate': 0,
            'displayResolution': 0,
            'displayGateMask': 0,
            'displayGateMaskOpacity': 0.70,
            'displayGateMaskColor': [0.5, 0.5, 0.5],
            'displayFieldChart': 0,
            'displaySafeAction': 0,
            'displaySafeTitle': 0,
            'displayFilmPivot': 0,
            'displayFilmOrigin': 0,
            'overscan': 1.0
        }
        # 恢复摄像机初始设置
        for k, v in options.items():
            if not cmds.getAttr(camera + '.' + k, l=1):
                v1 = cmds.getAttr(camera + '.' + k)
                if type(v1) == list:
                    cmds.setAttr(camera + '.' + k, v[0], v[1], v[2])
                    options[k] = v1[0]
                else:
                    cmds.setAttr(camera + '.' + k, v)
                    options[k] = v1
        modelPanel = cmds.getPanel(withFocus=True)
        cmds.modelEditor(modelPanel, e=1, allObjects=0)
        cmds.modelEditor(modelPanel, e=1, polymeshes=1)
        cmds.modelEditor(modelPanel, e=1, pluginObjects=['gpuCacheDisplayFilter', 1])
        images = self.taskDir + '/avatar.jpg'
        cmds.playblast(
            format='image',
            cf=images,
            viewer=1,
            frame=101,
            showOrnaments=1,
            percent=100,
            compression='jpg',
            quality=100,
            widthHeight=[320, 180]
        )

        # 拍屏参数
        # 菜单切换触发HUD
        index = self.instance.tabWidget.count()
        self.instance.tabWidget.setCurrentIndex(index-3)
        view = self.instance.QcbView.isChecked()
        ornaments = self.instance.QcbOrnaments.isChecked()
        offscreen = self.instance.QcbOffscreen.isChecked()
        mformat = self.instance.QcbFormat.currentText()
        encoding = self.instance.QcbEncoding.currentText()
        quality = self.instance.QsbQuality.value()
        scale = self.instance.QsbScale.value()
        w = self.instance.QsbWidth.value()
        h = self.instance.QsbHeight.value()

        # 摄像机默认参数
        camera = cmds.lookThru(q=True)
        options = {
            'displayFilmGate': 0,
            'displayResolution': 0,
            'displayGateMask': 0,
            'displayGateMaskOpacity': 0.70,
            'displayGateMaskColor': [0.5, 0.5, 0.5],
            'displayFieldChart': 0,
            'displaySafeAction': 1,
            'displaySafeTitle': 0,
            'displayFilmPivot': 0,
            'displayFilmOrigin': 0,
            'overscan': 1.0
        }
        # 恢复摄像机初始设置
        for k, v in options.items():
            if not cmds.getAttr(camera + '.' + k, l=1):
                v1 = cmds.getAttr(camera + '.' + k)
                if type(v1) == list:
                    cmds.setAttr(camera + '.' + k, v[0], v[1], v[2])
                    options[k] = v1[0]
                else:
                    cmds.setAttr(camera + '.' + k, v)
                    options[k] = v1

        # movies,音频
        if self.abbr in ['sim']:
            cmds.modelEditor(modelPanel, e=1, nurbsCurves=1)
        s = []
        sounds = cmds.ls(type='audio')
        if sounds:
            slider = mel.eval('$tmpVar=$gPlayBackSlider')
            audio = cmds.timeControl(slider, q=1, sound=1)
            if audio:
                s.append(audio)

        movies = self.verDir + '/' + self.task + '_' + self.abbr + '.mov'
        if s:
            cmds.playblast(
                format=mformat,
                sound=s[0],
                filename=movies,
                forceOverwrite=1,
                sequenceTime=0,
                clearCache=1,
                viewer=view,
                showOrnaments=ornaments,
                offScreen=offscreen,
                fp=4,
                percent=scale,
                compression=encoding,
                quality=quality,
                widthHeight=[w, h]
            )
        else:
            cmds.playblast(
                format=mformat,
                filename=movies,
                forceOverwrite=1,
                sequenceTime=0,
                clearCache=1,
                viewer=view,
                showOrnaments=ornaments,
                offScreen=offscreen,
                fp=4,
                percent=scale,
                compression=encoding,
                quality=quality,
                widthHeight=[w, h]
            )

        # 恢复摄像机用户设置
        for k, v in options.items():
            if not cmds.getAttr(camera + '.' + k, l=1):
                if type(v) == tuple:
                    cmds.setAttr(camera + '.' + k, v[0], v[1], v[2])
                else:
                    cmds.setAttr(camera + '.' + k, v)
        # 切回提交菜单
        cmds.refresh()
        self.instance.tabWidget.setCurrentIndex(index-2)
        cmds.modelEditor(modelPanel, e=1, nurbsCurves=1)

    def publish(self):
        if 'qt' not in cmds.playblast(q=1, format=1):
            self.SigScriptEditor.emit('error', '安装Windows 64位版本的QuickTime(7.7.9), 重启Maya后完成文件提交工作')
            raise RuntimeError('QuickTime 7.7.9')

        # 创建文件夹
        cmds.sysFile(self.verDir, makeDir=True)

        # 创建json文件
        jsonfile = self.task + '_' + self.abbr + '.json'
        self.writeData(jsonfile)

        # 镜头拍屏
        if self.abbr in ['lay', 'blk', 'ani', 'efx', 'sim']:
            # 镜头拍屏
            self.dailies()
        os.startfile(self.verDir)

        # 分支规则
        mfile = self.verDir + '/' + self.task + '_' + self.abbr + self.format[0]
        if self.submit == 'dailies':
            # 工程文件
            exn = cmds.file(q=1, exn=1)
            cmds.sysFile(exn, copy=mfile)
            # 进程提示
            if self.abbr in ['lay', 'blk', 'ani', 'efx', 'sim']:
                self.SigScriptEditor.emit('dailies', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作\n'
                                                     '将dailies/v###文件夹下*.mov文件拖拽到工作/效果审核')
            elif self.abbr in ['lgt']:
                self.SigScriptEditor.emit('dailies', '任务文件保存完成,艺术家自行完成单帧渲染及预合的工作\n'
                                                     '将最终单帧合成后的*.jpg图片文件拖拽到工作/效果审核')
        elif self.submit == 'publish':
            # 工程文件
            cmds.file(rename=mfile)
            cmds.file(f=1, save=1, type=self.format[1])
            # 进程提示
            if self.abbr in ['lay', 'blk']:
                self.SigScriptEditor.emit('publish', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作\n'
                                                     '将publish/v###文件夹下所有文件拖拽到工作/通过文件')
            elif self.abbr in ['ani', 'efx', 'sim']:
                self.SigScriptEditor.emit('publish', '任务文件保存完成,请在当前视窗打开橙色缓存工具完成后续工作')
            elif self.abbr in ['lgt']:
                # 创建渲染文件夹
                cmds.sysFile(self.verDir + '/images', makeDir=True)
                # 进程提示
                self.SigScriptEditor.emit('publish', '任务文件保存完成,艺术家自行完成灯光渲染的工作(交付时提交即可)\n'
                                                     '要求图片格式为EXR序列,输出路径为publish/v###/images文件夹\n'
                                                     '将publish/v###文件夹下所有文件拖拽到工作/通过文件')