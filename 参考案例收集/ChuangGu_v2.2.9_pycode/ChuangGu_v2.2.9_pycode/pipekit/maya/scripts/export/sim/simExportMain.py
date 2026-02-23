# -*- coding: utf-8 -*-

import os
import re
import sys
import json
from PySide2 import QtWidgets, QtCore, QtGui
import subprocess

import envpath
from core.general import Mregister
from core import interface
from core import config
from export.sim import simExportWindow as UI
import maya.cmds as cmds

PROJECTS = envpath.ROOTPATH.rsplit('\\', 3)[0] + '/config/projects'
XBMLANGPATH = envpath.ROOTPATH.rsplit('\\', 1)[0] + '/icons'


class Main(QtWidgets.QMainWindow, UI.Ui_ExportWin):
    SigSelect = QtCore.Signal(dict)

    def __init__(self, parent=Mregister().getMayaWin()):
        super(Main, self).__init__(parent)

        # 装载界面
        if interface.license():
            self.setupUi(self)
            # 删除界面
            for widget in parent.findChildren(QtWidgets.QMainWindow):
                if widget is not self:
                    if widget.objectName() == self.objectName():
                        widget.close()
            # 定义参数
            self.itemDict = {}
            self.offset = None
            # 预设风格
            self.setStyleSheet('''
                QMenu{
                    font-size: 10pt; 
                }
                QMenu::item {
                    color: rgb(185,185,185);
                }
                QMenu::item:selected{
                    background-color:rgb(50,50,50);
                }
                QLabel,QDoubleSpinBox{
                    border-radius: 2px;
                }
                QLabel:disabled,QCheckBox:disabled,QDoubleSpinBox:disabled{
                    color: rgb(125, 125, 125);
                }
                QDoubleSpinBox::up-button,QDoubleSpinBox::down-button
                {
                    width: 0px;
                }
                QLabel,QGroupBox,QCheckBox,QComboBox,QSpinBox,QDoubleSpinBox,QSlider{
                    color: rgb(175, 175, 175);
                }
                QGroupBox {
                    border-style: solid;
                }
                QPushButton{
                    border-radius: 2px;
                    color: rgb(180, 180, 180);
                    background-color: rgb(100,100,100);
                }
                QPushButton:hover{
                    color: rgb(200, 200, 200);
                    background-color: rgb(125,125,125);
                    font:bold 12px
                }
                QPushButton:pressed{
                    color: rgb(150, 100, 150);
                    background-color: rgb(50,50,50);
                    font:bold 12px
                }
                QToolBox:tab{
                    color: rgb(175, 175, 175);
                    background-color: rgb(60,60,60);
                }
                QToolBox::tab:selected{
                    background-color: rgb(75,55,75);
                    color: rgb(125, 100, 125);
                    border-radius: 5px;
                }
                QListWidget{
                    outline: 0px;
                    background-color: rgb(75, 75, 75);
                }
                QListWidget::item{
                    color: rgb(50,50,50);
                }
                QListWidget::item:hover{
                    background-color: rgb(50,50,50);
                    border-radius: 2px;
                    color: rgb(150, 100, 150)
                }
                QListWidget::item:selected{
                    color: rgb(200,200,75);
                    border: 2px solid rgb(200,200,75);
                    border-radius: 4px;
                }
            ''')
            self.assemblyUi()
            self.connectUi()
            self.resize(1400, 780)
            self.label.setText(interface.copyright())
            self.setWindowTitle('Simulation Export Tool v{}'.format(envpath.CTOOLKIT))
        else:
            self.resize(480, 780)
            self.setWindowTitle('Simulation Export Tool v{} 到期不在提供服务.'.format(envpath.CTOOLKIT))

    def __parameter__(self):
        proj = self.QcbProject.currentText()
        jfile = PROJECTS + '/' + proj + '.json'

        projectDcit = config.project(jfile)['project']
        # 初始参数
        self.drive = projectDcit['drive']
        self.fps = projectDcit['playbackSpeed']
        self.simMinFrame = projectDcit['simulationFrame']
        self.aniMinFrame = projectDcit['startFrame']
        self.handleFrame = projectDcit['handleFrame']
        self.resolutions = projectDcit['resolutions']

    def scriptsUi(self, msg):
        interface.scriptEditor(self.label, msg[0], msg[1])

    def connectUi(self):
        # Tab/导出
        self.QcbEvaluation.activated.connect(self.evaluationMode)
        self.QcbProject.activated.connect(self.updateEditUi)
        self.QpbStyle.clicked.connect(self.styleUi)
        self.QpbExport.clicked.connect(self.publishApply)
        self.tabWidgetView.currentChanged.connect(self.tabViewUi)

    def assemblyUi(self):
        # 加载插件
        plugins = ['AbcExport.mll', 'sceneAssembly.mll', 'gpuCache.mll']
        for plugin in plugins:
            try:
                if not cmds.pluginInfo(plugin, q=1, loaded=1):
                    cmds.loadPlugin(plugin)
            except:
                print('//Result: plug-ins {} skip.'.format(plugin))

        # 界面预设
        self.QcbEvaluation.setCurrentIndex(2)
        # 初始执行
        self.evaluationMode(self)
        self.projectUi()
        self.updateEditUi(self)

    def styleUi(self):
        stage = self.QpbStyle.text()
        if stage == '[-]':
            self.tabWidgetView.setVisible(False)
            self.frameNote.setVisible(False)
            self.resize(300, 780)
            self.QpbStyle.setText('[+]')
            self.QrbExportAll.setChecked(True)
        else:
            self.tabWidgetView.setVisible(True)
            self.frameNote.setVisible(True)
            self.resize(1400, 780)
            self.QpbStyle.setText('[-]')

    def projectUi(self):
        projects = cmds.getFileList(fld=PROJECTS, fs='*.json')
        if projects:
            projects.sort(reverse=False)
            for proj in projects:
                self.QcbProject.addItem(proj.split('.')[0])

    def updateEditUi(self, args):
        self.__parameter__()
        # 驱动器号
        self.QcbDrive.clear()
        drive = [self.drive, 'F:', 'E:', 'D:']
        self.QcbDrive.addItems(drive)
        # 设置起始帧
        cmds.currentUnit(time=self.fps)
        self.QdsbAnimationMin.setValue(self.aniMinFrame)
        self.QdsbAnimationMax.setValue(cmds.playbackOptions(q=1, maxTime=1))
        self.QdsbHandleMin.setValue(self.handleFrame[0])
        self.QdsbHandleMax.setValue(self.handleFrame[1])
        self.QdsbSimulation.setValue(self.simMinFrame)
        self.projectDir = self.drive + '/' + self.QcbProject.currentText()
        self.tabViewUi(args)

    def alembicUi(self):
        # {'reference': ['chr', 'prp', 'set']}
        self.QlwSim.setDragEnabled(False)
        self.QlwSim.setIconSize(QtCore.QSize(92, 92))
        self.QlwTmp.setDragEnabled(False)
        self.QlwTmp.setIconSize(QtCore.QSize(92, 92))

        reference = cmds.file(q=1, reference=1)
        if reference:
            reference.sort(reverse=False)
            for i in reference:
                rfn = cmds.referenceQuery(i, rfn=1)
                nsid = re.sub('\D', '', str(rfn).split('_')[-1])
                task = i.split('/')[4] + nsid
                if 'sim' in task:
                    task = 'camera'
                item = QtWidgets.QListWidgetItem(task)
                item.setSizeHint(QtCore.QSize(96, 96 + 22))
                item.setToolTip('Task: ' + task)
                if '/assets/' in i and '/cfx/publish/' in i:
                    # 头像
                    avatar = i.rsplit('/', 3)[0] + '/avatar.jpg'
                    if not os.path.exists(avatar):
                        avatar = XBMLANGPATH + '/task.jpg'

                    if not cmds.referenceQuery(i, isLoaded=1):
                        v = [175, 175, 175]
                        s = 'none'
                        self.itemDict['alembic'][task] = {
                            'category': i.split('/')[3],
                            'stage': s,
                            'namespace': 'none'
                        }
                    else:
                        jfile = i.rsplit('/', 1)[0] + '/' + i.split('/')[4] + '_cfx.json'
                        if os.path.exists(jfile):
                            with open(jfile, 'r') as fo:
                                text = fo.read()
                                fdict = json.loads(text)
                            ver = fdict.keys()
                            ver.sort(reverse=True)
                            stage = fdict[ver[0]]['stage']
                            if stage[2] == 'hair':
                                v = [0, 150, 150]
                                s = 'hair'
                            elif stage[2] == 'cloth':
                                v = [214, 128, 109]
                                s = 'cloth'
                            elif stage[2] == 'cfx2':
                                v = [150, 75, 150]
                                s = 'cfx2'
                        else:
                            v = [150, 75, 150]
                            s = 'temp'
                        namespace = cmds.referenceQuery(i, namespace=1)
                        self.itemDict['alembic'][task] = {
                            'category': i.split('/')[3],
                            'stage': s,
                            'namespace': namespace
                        }
                    self.QlwSim.addItem(item)
                else:
                    if not cmds.referenceQuery(i, isLoaded=1):
                        v = [175, 175, 175]
                    else:
                        v = [75, 150, 75]
                    self.QlwTmp.addItem(item)
                    avatar = XBMLANGPATH + '/task.jpg'
                item.setIcon(QtGui.QIcon(avatar))
                item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))

    def tabViewUi(self, args):
        # 清空数据
        self.QlwSim.clear()
        self.QlwTmp.clear()
        self.itemDict['alembic'] = {}
        # 判断文件
        exn = cmds.file(q=1, exn=1)
        if self.projectDir in exn and '/sim/publish/v' in exn:
        # if self.projectDir in exn and '/sim/publish/v' in exn and '/cache/' not in exn:
            self.alembicUi()

    def evaluationMode(self, args):
        item = self.QcbEvaluation.currentText()
        if item == 'DG':
            mode = 'off'
        else:
            mode = item.lower()
        self.evaluation = mode

        old = cmds.evaluationManager(q=1, mode=1)
        if old[0] != mode:
            cmds.evaluationManager(mode=mode)
            interface.scriptEditor(self.label, 'result', 'Evaluation mode [' + item + ']')

    def alembicParams(self):
        cmd = ' -step ' + str(self.QdsbStep.value())
        if self.QcbNormals.isChecked():
            cmd += ' -noNormals'
        if self.QcbStrip.isChecked():
            cmd += ' -stripNamespaces'
        if self.QcbUV.isChecked():
            cmd += ' -uvWrite'
        if self.QcbColorSets.isChecked():
            cmd += ' -writeColorSets'
        if self.QcbFaceSets.isChecked():
            cmd += ' -writeFaceSets'
        if self.QcbWorld.isChecked():
            cmd += ' -worldSpace'
        if self.QcbVisibility.isChecked():
            cmd += ' -writeVisibility'
        if self.QcbCreases.isChecked():
            cmd += ' -autoSubd'
        if self.QcbUvSets.isChecked():
            cmd += ' -writeUVSets'
        cmd += ' -dataFormat ogawa'
        return cmd

    def alembicCmds(self, time, root, file):
        cmd = '-frameRange ' + str(time[0]) + ' ' + str(time[1])
        cmd += self.alembicParams()
        cmd += ' -root ' + root
        cmd += ' -file ' + file
        cmds.AbcExport(j=cmd)

    def publishApply(self):
        # 驱动器判断
        if not os.path.exists(self.drive):
            interface.scriptEditor(self.label, 'error', '服务器驱动器 {} 不存在,请及时映射磁盘.')
            return
        else:
            drive = self.QcbDrive.currentText()
            if not os.path.exists(drive):
                interface.scriptEditor(self.label, 'error', '本地驱动器 {} 不存在,请选择本期其他驱动器.')
                return

        # 文件路径判断
        cover = False
        exn = cmds.file(q=1, exn=1)
        if '/sim/publish/v' not in exn:
            interface.scriptEditor(self.label, 'note', "通过 {'simpub': 'Simulation Publish Tool'} 打开存档菜单下(publish/v###)最高版本通过文件.")
            return
        else:
            if '/cache/' in exn:
                if self.QrbExportSel.isChecked():
                    cover = True
                cacheDir = exn.rsplit('/', 1)[0].replace(self.drive, drive)
            else:
                cacheDir = exn.rsplit('/', 1)[0].replace(self.drive, drive) + '/cache'
            cmds.sysFile(cacheDir, makeDir=True)

        # 全局判断
        init = []
        load = []
        temp = []
        base = []
        done = {}
        if self.itemDict['alembic']:
            init.append('alembic')
            for k, v in self.itemDict['alembic'].items():
                stage = v['stage']
                if stage == 'none':
                    load.append(k)
                elif stage == 'temp':
                    temp.append(k)
                elif stage == 'base':
                    base.append(k)
                done[k] = [v['category'], stage, v['namespace']]

        if not init:
            interface.scriptEditor(self.label, 'note', "通过 {'simpub': 'Simulation Publish Tool'} 打开存档菜单下(publish/v###)最高版本通过文件.")
            return
        elif load:
            interface.scriptEditor(self.label, 'warning', '未加载引用文件 {},全局受到影响执行被迫终止.'.format(load))
            return
        elif temp:
            interface.scriptEditor(self.label, 'error', '错误文件 {} 请及时更新绑定文件,向下执行被迫终止'.format(temp))
            return
        elif base:
            interface.scriptEditor(self.label, 'warning', '绿色或紫色项允许输出缓存,蓝色项 {} 找制片或绑定师更新绑定文件.'.format(base))
            return

        # 执行入口
        alembic = []
        if not done:
            interface.scriptEditor(self.label, 'error', '未找到输出对象,终止执行.')
            return
        else:
            # 缓存对象
            if self.QrbExportAll.isChecked():
                for k, v in done.items():
                    if v[0] in ['chr', 'prp']:
                        alembic.append({k: v})
            elif self.QrbExportSel.isChecked():
                items = self.QlwSim.selectedItems()
                for i in items:
                    k = i.text()
                    v = done[k]
                    alembic.append({k: v})
        if not alembic:
            interface.scriptEditor(self.label, 'error', '未找到输出对象,终止执行.')
            return

        # 新增字段
        start = self.QdsbAnimationMin.value()
        end = self.QdsbAnimationMax.value()
        self.itemDict['ctoolkit'] = envpath.CTOOLKIT
        self.itemDict['application'] = 'Maya ' + str(cmds.about(api=1))[:4] + '.' + str(cmds.about(api=1))[5:6]
        animation = [self.QdsbAnimationMin.value(), self.QdsbAnimationMax.value()]
        handle = [self.QdsbHandleMin.value(), self.QdsbHandleMax.value()]
        simulation = self.QdsbSimulation.value()
        proj = self.QcbProject.currentText()
        if self.QrbExClassic.isChecked():
            mode = 'classic'
        elif self.QrbExPrompt.isChecked():
            mode = 'prompt'
        elif self.QrbExClient.isChecked():
            mode = 'client'
        self.itemDict['setting'] = {
            'drive': [self.drive, drive],
            'project': proj,
            'dirpath': cacheDir,
            'animSlider': [animation[0] + handle[0], animation[1] + handle[1]],
            'cfx2Slider': [simulation, animation[1] + handle[1]],
            'timeSlider': [start, end],
            'resolution': self.resolutions,
            'playbackSpeed': self.fps,
            'evaluation': self.evaluation,
            'abcParams': self.alembicParams(),
            'versionFollow': self.QcbVersion.isChecked(),
            'export': mode
        }

        # 写入json文件
        jsfile = cacheDir + '/__init__.json'
        with open(jsfile, 'w') as fo:
            fo.write(json.dumps(self.itemDict, indent=4))

        # 视窗输出
        if self.QrbExClassic.isChecked():
            # 另存文件
            cmds.select(clear=1)
            if cover == False:
                exfile = cacheDir + '/classic.ma'
                cmds.file(rename=exfile)
                cmds.file(f=1, save=1, type='mayaAscii')
            else:
                cmds.file(rename=exn)
                cmds.file(f=1, save=1, type='mayaAscii')

            # 导出缓存
            if alembic:
                abctime = self.itemDict['setting']['animSlider']

                for i in alembic:
                    cmds.refresh()
                    k = i.keys()[0]
                    v = i.values()[0]

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
                                        for n in nucleus:
                                            cmds.setAttr(n + '.enable', 1)
                                            cmds.setAttr(n + '.startFrame', 50)
                                    else:
                                        for n in nucleus:
                                            cmds.setAttr(n + '.enable', 0)
                                            cmds.setAttr(n + '.startFrame', 999)

                    subdir = cacheDir + '/' + v[0] + '_' + k
                    # 毛发缓存/hairCurveNUL
                    if v[1] in ['hair', 'cfx2']:
                        root = v[2] + ':hairCurveNUL'
                        grps = cmds.listRelatives(root, c=1)
                        if grps:
                            cmds.sysFile(subdir, makeDir=True)
                            for grp in grps:
                                cmds.refresh()
                                interface.scriptEditor(self.label, 'command', '正在导出 {0}{1}{2} 缓存'.format(grp, ':', 'hair'))
                                crvfile = subdir + '/' + grp.split(':')[-1] + '.abc'
                                self.alembicCmds(abctime, grp, crvfile)
                    # 渲染模型/srfNUL
                    if v[1] in ['cloth', 'cfx2']:
                        cmds.refresh()
                        cmds.sysFile(subdir, makeDir=True)
                        root = v[2] + ':srfNUL'
                        interface.scriptEditor(self.label, 'command', '正在导出 {0}{1}{2} 缓存'.format(k, ':', 'srfNUL'))
                        anifile = subdir + '/' + proj + '_' + v[0] + '_' + k + '_ani.abc'
                        self.alembicCmds(abctime, root, anifile)

                    # 解算模型/simNUL
                    if v[1] in ['hair', 'cfx2']:
                        cmds.refresh()
                        cmds.sysFile(subdir, makeDir=True)
                        root = v[2] + ':simNUL'
                        interface.scriptEditor(self.label, 'command', '正在导出 {0}{1}{2} 缓存'.format(k, ':', 'simNUL'))
                        simfile = subdir + '/' + proj + '_' + v[0] + '_' + k + '_sim.abc'
                        self.alembicCmds(abctime, root, simfile)

                # 全部显示
                for k0, vDict0 in self.itemDict['alembic'].items():
                    rn = vDict0['category'] + '_' + k0 + 'RN'
                    if cmds.objExists(rn):
                        rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                        cmds.setAttr(rootNUL + '.v', 1)
                interface.scriptEditor(self.label, 'result', '缓存导出工作完成.')

            # 拷贝到服务器
            if self.drive != drive:
                severDir = cacheDir.replace(drive, self.drive)
                files = cmds.getFileList(folder=cacheDir, filespec='*.*')
                if files:
                    for file in files:
                        cmds.refresh()
                        cmds.sysFile(cacheDir + '/' + file, copy=severDir + '/' + file)
                        interface.scriptEditor(self.label, 'result', '正在拷贝 {} 到服务器.'.format(file))

                dirs = cmds.getFileList(folder=cacheDir, filespec='*.')
                if dirs:
                    for dir in dirs:
                        cacheSubDir = cacheDir + '/' + dir
                        files = cmds.getFileList(folder=cacheSubDir, filespec='*.*')
                        if files:
                            severSubDir = severDir + '/' + dir
                            cmds.sysFile(severSubDir, makeDir=True)
                            for i in files:
                                cmds.refresh()
                                cmds.sysFile(cacheSubDir + '/' + i, copy=severSubDir + '/' + i)
                                interface.scriptEditor(self.label, 'result', '正在拷贝 {} 到服务器.'.format(i))
                os.startfile(severDir.rsplit('/', 1)[0])
            else:
                os.startfile(cacheDir.rsplit('/', 1)[0])

            # 返回结果
            cmds.refresh()
            interface.scriptEditor(self.label, 'result', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作.\n'
                                                         '将publish/v###文件夹下所有文件拖拽到工作/通过文件.\n'
                                                         '单击参考/镜头缩略图框的avatar.jpg完成上传(一次即可).')
        # 后台输出
        elif self.QrbExPrompt.isChecked():
            if self.QrbExportSel.isChecked():
                interface.scriptEditor(self.label, 'warning', '使用后台输出模式时选择模式必须为(所有).')
                return
            # 保存文件
            exfile = cacheDir + '/prompt.ma'
            cmds.file(rename=exfile)
            cmds.file(f=1, save=1, type='mayaAscii')
            # 返回打印
            interface.scriptEditor(self.label, 'result', '后台输出模式启动,请等待数据输出完成.\n'
                                                         '将publish/v###文件夹下所有文件拖拽到工作/通过文件.\n'
                                                         '单击参考/镜头缩略图框的avatar.jpg完成上传(一次即可).')
            # 启动后台
            mayapy = sys.argv[0].replace('maya', 'mayapy')
            pypath = envpath.MAYAPATH + '/scripts/export/sim/simPromptMain.py'
            if not os.path.exists(pypath):
                pypath = envpath.MAYAPATH + '/scripts/export/sim/simPromptMain.pyc'
            subprocess.Popen("{exepath} {scripts} {filepath}".format(
                    exepath=mayapy,
                    scripts=pypath,
                    filepath=exfile),
                shell=False)
        # 到客户端
        elif self.QrbExClient.isChecked():
            interface.scriptEditor(self.label, 'warning', '客户端输出模式预计在2022年07月左右提供.')
            return
            # 保存后台文件
            exfile = cacheDir + '/client.ma'
            cmds.file(rename=exfile)
            cmds.file(f=1, save=1, type='mayaAscii')


def main():
    win = Main()
    win.show()