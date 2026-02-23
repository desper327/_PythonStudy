# -*- coding: utf-8 -*-

import re
import os
import sys
import json
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
import subprocess

import envpath
from core.general import Mregister
from core import interface
from core import config
from export.ani import aniExportWindow as UI
import maya.cmds as cmds
import maya.mel as mel

PROJECTS = envpath.ROOTPATH.rsplit('\\', 3)[0] + '/config/projects'
XBMLANGPATH = envpath.ROOTPATH.rsplit('\\', 1)[0] + '/icons'


class Menu(QtWidgets.QMenu):
    SigNeed = QtCore.Signal(dict)
    SigScripts = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(Menu, self).__init__()
        self.parent = parent
        self.SigNeed.connect(self.__parameter__)

    def __parameter__(self, msg):
        self.msg = msg
        self.tpose = self.msg['stpose']

    def clickMenu(self, mode):
        menu = QtWidgets.QMenu(self.parent)
        menu.addAction('选择图标加载引用文件').triggered.connect(partial(self.referenceEdit, 'load'))
        menu.addAction('选择图标卸载引用文件').triggered.connect(partial(self.referenceEdit, 'unload'))
        menu.addAction('选择图标移除引用文件').triggered.connect(partial(self.referenceEdit, 'remove'))
        if mode == 'alembic':
            if self.tpose < 101:
                menu.addSeparator()
                menu.addAction('ADV角色初始姿势 <{}>'.format(self.tpose)).triggered.connect(self.tposeApply)
        elif mode == 'scene':
            menu.addSeparator()
            menu.addAction("选择图标AR切换到 Locator 模式").triggered.connect(partial(self.assemblyEdit, 'Locator'))
            menu.addAction("选择图标AR切换到 ModBbox 模式").triggered.connect(partial(self.assemblyEdit, 'ModBbox'))
            menu.addAction("选择图标AR切换到 ModCache 模式").triggered.connect(partial(self.assemblyEdit, 'ModCache'))
            menu.addAction("选择图标AR切换到 RigFiles 模式").triggered.connect(partial(self.assemblyEdit, 'RigFiles'))
            menu.addAction("选择图标AR切换到 SrfProxy 模式").triggered.connect(partial(self.assemblyEdit, 'SrfProxy'))
            menu.addAction("选择图标AR切换到 SrfFiles 模式").triggered.connect(partial(self.assemblyEdit, 'SrfFiles'))
        menu.exec_(QtGui.QCursor.pos())

    def referenceEdit(self, mode):
        if not self.msg['select']:
            self.SigScripts.emit(['error', '选择头像后右键完成命令操作.'])
        else:
            error = []
            for k, v in self.msg['select'].items():
                cmds.refresh()
                category = v['category']
                if category in ['chr', 'prp', 'old']:
                    rn = v['referenceNode']
                    if mode == 'load':
                        cmds.file(loadReference=rn)
                    elif mode == 'unload':
                        cmds.file(unloadReference=rn)
                    elif mode == 'remove':
                        rfFile = cmds.referenceQuery(rn, filename=1)
                        cmds.file(rfFile, removeReference=1)
                else:
                    error.append(k)
            if error:
                self.SigScripts.emit(['error', 'AR对象 {} 不支持Reference功能,隶属于AR显示切换功能.'.format(error)])

    def assemblyEdit(self, mode):
        if not self.msg['select']:
            self.SigScripts.emit(['error', '选择头像后右键完成命令操作.'])
        else:
            error = []
            for k, v in self.msg['select'].items():
                cmds.refresh()
                category = v['category']
                if category in ['set']:
                    ar = v['outliner']
                    childs = cmds.listRelatives(ar, children=1)
                    if childs:
                        for child in childs:
                            if '_AR' in child:
                                try:
                                    cmds.assembly(child, edit=True, activeLabel=mode)
                                    if mode in ['RigFiles', 'SrfFiles']:
                                        geo = cmds.ls(child.split(':')[0] + ':*:Geometry')
                                        if geo:
                                            cmds.setAttr(geo[0] + '.inheritsTransform', 0)
                                except:
                                    pass
                else:
                    error.append(k)
            if error:
                self.SigScripts.emit(['error', 'RN对象 {} 不支持AssemblyReference功能,隶属于RN切换功能.'.format(error)])

    def tposeApply(self):
        anims = cmds.ls(type=['animCurveTA', 'animCurveTL'])
        if anims:
            v = 0
            for i in anims:
                attr = cmds.connectionInfo(i + '.output', destinationFromSource=1)
                if attr:
                    if len(attr[0].split(':')) == 2:
                        ctrl = attr[0].split(':')[-1].split('.')[0]
                        if ctrl not in ['Main', 'MainExtra']:
                            cmds.setKeyframe(attr[0], time=self.tpose, value=0)
                            v += 1
            if v:
                cmds.file(f=1, save=1)
                self.SigScripts.emit(['result', 'Tpose工作完成,请动画师肉眼检查;如果Tpose有问题请在角色101帧记录动画关键帧.'])
            else:
                self.SigScripts.emit(['error', '场景内未找到任何动画曲线,请在角色101帧记录动画关键帧.'])


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
            # 装载右键
            self.RM = Menu(self.tabWidgetView)
            self.SigSelect.connect(self.RM.SigNeed)
            self.RM.SigScripts.connect(self.scriptsUi)
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
            self.setWindowTitle('Animation Export Tool v{}'.format(envpath.CTOOLKIT))
        else:
            self.resize(480, 780)
            self.setWindowTitle('Animation Export Tool v{} 到期不在提供服务.'.format(envpath.CTOOLKIT))

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
        self.QcbOrigin.clicked.connect(self.originUi)
        self.QcbProject.activated.connect(self.updateEditUi)
        self.QpbStyle.clicked.connect(self.styleUi)
        self.QpbExport.clicked.connect(self.publishApply)
        self.tabWidgetView.currentChanged.connect(self.tabViewUi)
        # Tab/右键
        self.tabWidgetView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tabWidgetView.customContextMenuRequested.connect(self.menuUi)
        # Tab/偏移
        self.tabWidgetEdit.currentChanged.connect(self.tabEditUi)
        self.QpbOffset.clicked.connect(self.offsetApply)

    def assemblyUi(self):
        # 加载插件
        plugins = ['animImportExport.mll', 'gameFbxExporter.mll', 'AbcExport.mll', 'sceneAssembly.mll', 'gpuCache.mll']
        for plugin in plugins:
            try:
                if not cmds.pluginInfo(plugin, q=1, loaded=1):
                    cmds.loadPlugin(plugin)
            except:
                print('//Result: plug-ins {} skip.'.format(plugin))

        # 界面预设
        self.QdsbOriginMin.setEnabled(False)
        self.QcbRange.setVisible(False)
        self.QpbRefresh.setVisible(False)
        self.QpbRepair.setVisible(False)
        self.tabWidgetEdit.removeTab(2)
        self.QcbEvaluation.setCurrentIndex(0)
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

    def menuUi(self, args):
        # 发射选择数据
        chr = self.QlwChr.selectedItems()
        prp = self.QlwPrp.selectedItems()
        set = self.QlwSet.selectedItems()
        items = chr + prp + set
        emitDict = {
            'stpose': self.QdsbSimulation.value(),
            'select': {}
        }
        if items:
            keys = ['alembic', 'scene']
            for i in items:
                key = i.text()
                for n in keys:
                    if self.itemDict[n]:
                        for k, v in self.itemDict[n].items():
                            if key == k:
                                emitDict['select'][k] = v
        self.SigSelect.emit(emitDict)

        # 创建右键菜单
        index = self.tabWidgetView.currentIndex()
        if index == 0:
            self.RM.clickMenu('alembic')
        elif index == 1:
            self.RM.clickMenu('scene')
        self.tabViewUi(self)

    def originUi(self):
        if self.QcbOrigin.isChecked():
            self.labelOrigin.setEnabled(True)
            self.QdsbOriginMax.setEnabled(True)
        else:
            self.labelOrigin.setEnabled(False)
            self.QdsbOriginMax.setEnabled(False)

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
        if self.QdsbSimulation.value() < 101:
            self.QcbTpose.setVisible(True)
        else:
            self.QcbTpose.setVisible(False)
        self.projectDir = self.drive + '/' + self.QcbProject.currentText()
        self.tabViewUi(args)

    def alembicUi(self):
        # {'reference': ['chr', 'prp', 'set']}
        self.QlwSet.clearSelection()
        self.QlwChr.setDragEnabled(False)
        self.QlwChr.setIconSize(QtCore.QSize(92, 92))
        self.QlwPrp.setDragEnabled(False)
        self.QlwPrp.setIconSize(QtCore.QSize(92, 92))

        reference = cmds.file(q=1, reference=1)
        if reference:
            path = self.projectDir + '/assets'
            reference.sort(reverse=False)
            for i in reference:
                cmds.refresh()
                rfn = cmds.referenceQuery(i, rfn=1)
                # 添加主控件
                if path in i:
                    # 字符
                    nsid = re.sub('\D', '', str(rfn).split('_')[-1])
                    task = i.split('/')[4]

                    # 阶段
                    if not cmds.referenceQuery(rfn, isLoaded=1):
                        v = [175, 175, 175]
                        s = 'none'
                        n = 'none'
                        ns = 'none'
                    else:
                        ns = cmds.referenceQuery(rfn, namespace=1)
                        n = ns.replace(':', '') + ':Main'
                        rjson = i.rsplit('/', 3)[0] + '/rig/publish/' + task + '_rig.json'
                        if os.path.exists(rjson):
                            with open(rjson, 'r') as fo:
                                text = fo.read()
                                fdict = json.loads(text)
                            ver = fdict.keys()
                            ver.sort(reverse=True)
                            stage = fdict[ver[0]]['stage']
                            if stage[0] == 'done':
                                if stage[2] in ['hair', 'cloth', 'cfx2']:
                                    v = [150, 85, 150]
                                    s = 'cfx2'
                                else:
                                    v = [75, 150, 75]
                                    s = 'anim'
                            else:
                                v = [35, 150, 200]
                                s = 'base'
                        else:
                            v = [35, 150, 200]
                            s = 'temp'
                        '''
                        1.9.4
                        ns = cmds.referenceQuery(rfn, namespace=1)
                        n = ns.replace(':', '') + ':Main'
                        stage = cmds.referenceQuery(i, ns=1) + ':Group.stage'
                        if cmds.objExists(stage):
                            stage = cmds.getAttr(stage)
                            if stage in ['hair', 'cloth', 'cfx2']:
                                v = [150, 85, 150]
                                s = 'cfx2'
                            elif stage in ['done']:
                                v = [75, 150, 75]
                                s = 'anim'
                            else:
                                v = [35, 150, 200]
                                s = 'base'
                        else:
                            v = [35, 150, 200]
                            s = 'temp'
                        '''

                    # 控件
                    item = QtWidgets.QListWidgetItem(task+nsid)
                    item.setSizeHint(QtCore.QSize(96, 96 + 22))
                    if (path + '/chr/') in i:
                        self.QlwChr.addItem(item)
                        self.itemDict['alembic'][task+nsid] = {
                            'stage': s,
                            'outliner': n,
                            'category': 'chr',
                            # 'instance': item,
                            'namespace': ns,
                            'referenceNode': rfn
                        }
                    elif (path + '/prp/') in i:
                        self.QlwPrp.addItem(item)
                        self.itemDict['alembic'][task+nsid] = {
                            'stage': s,
                            'outliner': n,
                            'category': 'prp',
                            # 'instance': item,
                            'namespace': ns,
                            'referenceNode': rfn
                        }
                    elif (path + '/veh/') in i:
                        self.QlwPrp.addItem(item)
                        self.itemDict['alembic'][task+nsid] = {
                            'stage': s,
                            'outliner': n,
                            'category': 'veh',
                            # 'instance': item,
                            'namespace': ns,
                            'referenceNode': rfn
                        }

                    # 头像, 颜色
                    avatar = i.rsplit('/', 3)[0] + '/avatar.jpg'
                    if not os.path.exists(avatar):
                        avatar = XBMLANGPATH + '/task.jpg'
                    item.setToolTip('\ntask: ' + task + '   \n')
                    item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))
                    item.setIcon(QtGui.QIcon(avatar))

    def sceneUi(self):
        # {'reference': ['set'], 'assembly': ['set']}
        self.QlwChr.clearSelection()
        self.QlwPrp.clearSelection()
        self.QlwSet.setDragEnabled(False)
        self.QlwSet.setIconSize(QtCore.QSize(190, 106))

        reference = cmds.file(q=1, reference=1)
        if reference:
            reference.sort(reverse=False)
            for i in reference:
                if 'X:/PIPILU/Season' in i and '/EP' in i and '/BG/' in i:
                    cmds.refresh()
                    rfn = cmds.referenceQuery(i, rfn=1)
                    if not cmds.referenceQuery(rfn, isLoaded=1):
                        v = [175, 175, 175]
                        s = 'none'
                        n = 'none'
                    else:
                        v = [75, 150, 75]
                        s = 'anim'
                        n = cmds.referenceQuery(rfn, nodes=1)[0]

                    # 空间ID
                    task = i.split('/')[5]
                    nsid = re.sub('\D', '', str(rfn).split('_')[-1])
                    item = QtWidgets.QListWidgetItem(task+nsid)
                    self.QlwSet.addItem(item)
                    self.itemDict['scene'][task + nsid] = {
                        'stage': s,
                        'outliner': n,
                        'category': 'old',
                        # 'instance': item,
                        'namespace': cmds.referenceQuery(rfn, namespace=1),
                        'referenceNode': rfn
                    }

                    item.setSizeHint(QtCore.QSize(192, 108 + 22))
                    avatar = XBMLANGPATH + '/task_16x9.jpg'

                    # 头像颜色
                    item.setToolTip('\ntask: ' + task + '   \n')
                    item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))
                    item.setIcon(QtGui.QIcon(avatar))

        # assembly
        assemblies = cmds.ls(assemblies=1)
        if assemblies:
            proj = self.QcbProject.currentText()
            path = self.drive + '/' + proj + '/assets/set'
            for i in assemblies:
                if cmds.nodeType(i) == 'assemblyReference':
                    filepath = cmds.getAttr(i + '.definition')
                    if path in filepath and '/asm/publish/' in filepath:
                        # 空间ID
                        task = filepath.split('/')[4]
                        nsid = re.sub('\D', '', str(i).split('_')[-1])
                        item = QtWidgets.QListWidgetItem(task+nsid)
                        self.QlwSet.addItem(item)
                        # 场景AR以引用方式创建后场景位置丢失的BUG
                        m = i.replace('AR', 'NS') + ':' + i.replace('AR', 'NS') + ':Main'
                        if not cmds.objExists(m):
                            m = i
                        self.itemDict['scene'][task + nsid] = {
                            'stage': 'anim',
                            'outliner': m,
                            'category': 'set',
                            # 'instance': item
                            'namespace': cmds.assembly(i, q=1, rns=1),
                            'referenceNode': 'none'
                        }
                        item.setSizeHint(QtCore.QSize(192, 108 + 22))
                        avatar = filepath.rsplit('/', 3)[0] + '/avatar.jpg'
                        if not os.path.exists(avatar):
                            avatar = XBMLANGPATH + '/task_16x9.jpg'
                        # 头像颜色
                        item.setToolTip('\ntask: ' + task + '   \n')
                        item.setBackground(QtGui.QBrush(QtGui.QColor(75, 150, 75)))
                        item.setIcon(QtGui.QIcon(avatar))

    def tabViewUi(self, args):
        # 清空数据
        self.QlwChr.clear()
        self.QlwPrp.clear()
        self.QlwSet.clear()
        self.itemDict['camera'] = {}
        self.itemDict['alembic'] = {}
        self.itemDict['scene'] = {}
        # 判断文件
        exn = cmds.file(q=1, exn=1)
        if self.projectDir in exn and '/ani/publish/v' in exn:
        # if self.projectDir in exn and '/ani/publish/v' in exn and '/cache/' not in exn:
            self.alembicUi()
            self.sceneUi()

    def tabEditUi(self, args):
        self.QlwOffset.clear()
        # 判断文件
        if self.offset:
            v = [150, 75, 75]
        else:
            v = [125, 125, 125]
        for k in ['camera', 'alembic', 'scene']:
            if self.itemDict[k]:
                for k1 in sorted(self.itemDict[k], reverse=False):
                    null = self.itemDict[k][k1]['outliner']
                    item = QtWidgets.QListWidgetItem(null)
                    item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))
                    self.QlwOffset.addItem(item)

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

    def offsetQuery(self):
        # 原点距离判断
        if self.QcbOrigin.isChecked():
            if cmds.objExists('sandCenterLOC'):
                self.offset = True
                interface.scriptEditor(self.label, 'error', '请切换到(偏移)菜单完成偏移工作')
                # raise ValueError('error')
                return False
            else:
                if self.itemDict['alembic']:
                    error = []
                    ctrls = []
                    for vDict in self.itemDict['alembic'].values():
                        ctrl = vDict['outliner']
                        if not cmds.objExists(ctrl):
                            error.append(ctrl)
                        else:
                            ctrls.append(ctrl)
                    if error:
                        interface.scriptEditor(self.label, 'warning', '未找到 {} 控制器,禁止导出以及影响场景偏移'.format(error))
                        # raise ValueError('error')
                        return False
                    else:
                        x = []
                        y = []
                        z = []
                        cmds.currentTime(101)
                        for i in ctrls:
                            p = cmds.xform(i, q=1, ws=1, t=1)
                            x.append(p[0])
                            y.append(p[1])
                            z.append(p[2])
                        m = len(ctrls)
                        c = [sum(x)/m, sum(y)/m, sum(z)/m]
                        local = mel.eval('mag(' + str(c).replace('[', '<<').replace(']', '>>') + ');')
                        world = self.QdsbOriginMax.value()
                        if local > world:
                            self.offset = True
                            if not cmds.objExists('sandCenterLOC'):
                                cmds.spaceLocator(n='sandCenterLOC', p=[0, 0, 0])
                            cmds.setAttr('sandCenterLOC.tx', c[0])
                            cmds.setAttr('sandCenterLOC.ty', c[1])
                            cmds.setAttr('sandCenterLOC.tz', c[2])
                            cmds.lockNode('sandCenterLOC', lock=1)
                            interface.scriptEditor(self.label, 'error', '请切换到(偏移)菜单完成偏移工作')
                            # raise ValueError('error')
                            return False
                        else:
                            self.offset = False
                            return True
                else:
                    self.offset = False
                    return True

    def offsetCommand(self, ctrl, offset):
        try:
            cmds.setAttr(ctrl + '.tx', lock=False)
            cmds.setAttr(ctrl + '.ty', lock=False)
            cmds.setAttr(ctrl + '.tz', lock=False)
        except:
            pass
        attrs = cmds.listAttr(ctrl, k=1)
        if attrs:
            for attr in attrs:
                if 'translate' in attr:
                    if attr == 'translateX':
                        v = 0
                    elif attr == 'translateY':
                        v = 1
                    elif attr == 'translateZ':
                        v = 2
                    cb = cmds.listConnections(ctrl + '.' + attr, d=1)
                    if cb:
                        vc = cmds.keyframe(cb[0], q=1, valueChange=1)
                        if vc:
                            for i in range(len(vc)):
                                cmds.keyframe(cb[0], index=(i, i), absolute=1, valueChange=vc[i] - offset[v])
                    else:
                        local = cmds.getAttr(ctrl + '.' + attr)
                        try:
                            cmds.setAttr(ctrl + '.' + attr, local - offset[v])
                        except:
                            pass

    def offsetApply(self):
        if self.offset == True:
            # 摄像机及Main控制器被约束,强行bake关键帧动画
            alls = []
            for i in range(self.QlwOffset.count()):
                alls.append(self.QlwOffset.item(i).text())
            ctrls = []
            error = []
            for i in alls:
                connections = cmds.listConnections(i, d=0)
                if connections:
                    constraints = ['parentConstraint', 'pointConstraint', 'orientConstraint', 'scaleConstraint']
                    for n in list(set(connections)):
                        if cmds.nodeType(n) in ['pairBlend']:
                            error.append(i)
                            break
                        if cmds.nodeType(n) in constraints:
                            ctrls.append(i)
                            break
            if error:
                interface.scriptEditor(self.label, 'error', '请手动解决 {} 控制器既存在关键帧动画又存在约束节点的错误,控制器只允许存在关键帧动画.'.format(error))
                return

            if ctrls:
                attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
                for ctrl in ctrls:
                    try:
                        for attr in attrs:
                            cmds.setAttr(ctrl + '.' + attr, lock=False)
                    except:
                        pass
                minTime = self.QdsbAnimationMin.value()
                maxTime = self.QdsbAnimationMax.value()
                cmds.bakeResults(ctrls,
                                 simulation=1,
                                 t=(minTime, maxTime),
                                 sampleBy=1,
                                 oversamplingRate=1,
                                 disableImplicitControl=1,
                                 preserveOutsideKeys=1,
                                 sparseAnimCurveBake=0,
                                 removeBakedAttributeFromLayer=0,
                                 removeBakedAnimFromLayer=0,
                                 bakeOnOverrideLayer=0,
                                 minimizeRotation=1,
                                 controlPoints=0,
                                 shape=1)
                if cmds.objExists('CamGroup'):
                    cmds.delete('CamGroup')

            # 偏移场景所有对象
            offset = cmds.xform('sandCenterLOC', q=1, ws=1, t=1)
            for i in range(self.QlwOffset.count()):
                cmds.refresh()
                ctrl = self.QlwOffset.item(i).text()
                self.offsetCommand(ctrl, offset)
                self.QlwOffset.item(i).setBackground(QtGui.QColor(75, 150, 75))
            # 删除偏移locator
            self.offset = False
            if cmds.objExists('sandCenterLOC'):
                cmds.lockNode('sandCenterLOC', lock=0)
                cmds.delete('sandCenterLOC')
            interface.scriptEditor(self.label, 'result', '场景偏移完成,请回到(导出)菜单,再次单击执行按钮.')
        else:
            interface.scriptEditor(self.label, 'warning', '请回到(导出)菜单,单击执行按钮.')

    def checkTposeframe(self, tpose):
        sim = True
        if tpose < 101:
            anims = cmds.ls(type=['animCurveTA', 'animCurveTL'])
            if anims:
                t = 0
                s = 0
                for i in anims:
                    attr = cmds.connectionInfo(i + '.output', destinationFromSource=1)
                    if attr:
                        if len(attr[0].split(':')) == 2:
                            ctrl = attr[0].split(':')[-1].split('.')[0]
                            if ctrl not in ['Main', 'MainExtra']:
                                v = cmds.keyframe(attr[0], q=1, tc=1)
                                if tpose in v:
                                    t += 1
                                s += 1
                if t != s:
                    sim = False
        return sim

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
        if '/ani/publish/v' not in exn:
            interface.scriptEditor(self.label, 'note', "通过 {'anipub': 'Animation Publish Tool'} 打开存档菜单下(publish/v###)最高版本通过文件.")
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
        keys = ['alembic', 'scene']
        for key in keys:
            if self.itemDict[key]:
                init.append(key)
                for k, v in self.itemDict[key].items():
                    stage = v['stage']
                    if stage == 'none':
                        load.append(k)
                    elif stage == 'temp':
                        temp.append(k)
                    elif stage == 'base':
                        base.append(k)
                    done[k] = [v['category'], v['outliner'], stage, v['namespace']]

        if not init:
            interface.scriptEditor(self.label, 'note', "通过 {'anipub': 'Animation Publish Tool'} 打开存档菜单下(publish/v###)最高版本通过文件.")
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
        scene = []
        if not done:
            interface.scriptEditor(self.label, 'error', '未找到输出对象,终止执行.')
            return
        else:
            # 缓存对象
            if self.QrbExportAll.isChecked():
                for k, v in done.items():
                    if v[0] in ['chr', 'prp', 'veh']:
                        alembic.append({k: v})
            elif self.QrbExportSel.isChecked():
                items = []
                items.extend(self.QlwChr.selectedItems())
                items.extend(self.QlwPrp.selectedItems())
                for i in items:
                    k = i.text()
                    v = done[k]
                    alembic.append({k: v})
            # 场景对象
            for v in done.values():
                if v[0] in ['set', 'old']:
                    scene.append(v[1])

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
            'simTpose': self.QcbTpose.isChecked(),
            'offset': {
                'check': self.QcbOrigin.isChecked(),
                'distance': self.QdsbOriginMax.value()
            },
            'versionFollow': self.QcbVersion.isChecked(),
            'export': mode
        }

        camera = None
        if cover == False:
            # 解算姿势
            if self.QcbTpose.isChecked():
                if not self.checkTposeframe(self.simMinFrame):
                    interface.scriptEditor(self.label, 'error', '{} 帧未创建角色Tpose,鼠标右键单击(ADV角色初始姿势)按钮.'.format(self.simMinFrame))
                    return

            # 摄像机判断
            camera = cmds.lookThru(q=1)
            if cmds.nodeType(camera) == 'camera':
                camera = cmds.listRelatives(camera, p=1)[0]
            if '_s' in camera and '_c' in camera and '_ani' in camera:
                if cmds.listRelatives(camera, p=1):
                    interface.scriptEditor(self.label, 'error', '摄像机禁止存在组层级;如果组本身没有数值请将摄像机移除组外,反之请自建新的摄像机完成命名及bake关键帧动画.')
                    return
            else:
                interface.scriptEditor(self.label, 'warning', '请切换到(*_s###_c###_ani)命名类型摄像机为当前视窗')
                return

            # 导出偏移前摄像机
            if self.offset == None:
                mel.eval('FBXResetExport;')
                mel.eval('FBXExportBakeComplexAnimation -v true;')
                mel.eval('FBXExportBakeComplexStart -v ' + str(start) + ';')
                mel.eval('FBXExportBakeComplexEnd -v ' + str(end) + ';')
                mel.eval('FBXExportBakeComplexStep -v 1;')
                mel.eval('FBXExportInputConnections - v false')
                mel.eval('FBXExportBakeResampleAnimation - v true;')
                fbxfile = cacheDir + '/' + camera.split('|')[-1].replace('ani', 'cam') + '_unoffset.fbx'
                cmds.select(camera, r=1)
                mel.eval('FBXExport -f "' + fbxfile + '" -s')

            # 原点距离判断
            self.itemDict['camera'][camera] = {'outliner': camera}
            if self.QcbOrigin.isChecked():
                if not self.offsetQuery():
                    return

            # 补救AR导出时丢失动画曲线连接信息
            self.itemDict['connect'] = {}
            if scene:
                anims = ['animCurveTL', 'animCurveTA', 'animCurveTU']
                for i in scene:
                    if cmds.nodeType(i) == 'assemblyReference':
                        objects = cmds.listRelatives(i, ad=1, f=1, type=['transform'])
                        if objects:
                            objects.append(i)
                        else:
                            objects = [i]
                        for anim in anims:
                            attrs = cmds.listConnections(objects, d=0, type=anim)
                            if attrs:
                                for attr in attrs:
                                    k = attr + '.output'
                                    v = cmds.connectionInfo(k, destinationFromSource=True)[0]
                                    self.itemDict['connect'][k] = v

                # 导出AR动画曲线
                groups = cmds.ls('*:*:Group')
                if groups:
                    for i in groups:
                        try:
                            ar = i.split(':')[0]
                            animfile = cacheDir + '/' + proj + '_set_' + ar.split('_')[0] + re.sub('\D', '', ar) + '_ani.anim'
                            cmds.select(i, r=1)
                            cmds.file(animfile,
                                      force=1,
                                      options="precision=17;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range=0:10;options=keys;hierarchy=below;controlPoints=0;shapes=1;helpPictures=0;useChannelBox=0;copyKeyCmd=-animation objects -option keys -hierarchy below -controlPoints 0 -shape 1 ",
                                      typ="animExport",
                                      pr=1,
                                      es=1)
                        except:
                            pass

            # 写入json文件
            jsfile = cacheDir + '/__init__.json'
            with open(jsfile, 'w') as fo:
                fo.write(json.dumps(self.itemDict, indent=4))

        # 初始参数
        self.offset = None

        # 视窗输出
        if self.QrbExClassic.isChecked():
            # 另存文件
            cmds.select(clear=1)
            if cover == False:
                exfile = cacheDir + '/classic.ma'
                cmds.file(rename=exfile)
                cmds.file(f=1, save=1, type='mayaAscii')

                # 导出偏移后摄像机
                fbxfile = cacheDir + '/' + camera.split('|')[-1].replace('ani', 'cam') + '.fbx'
                cmds.select(camera, r=1)
                mel.eval('FBXExport -f "' + fbxfile + '" -s')
            else:
                cmds.file(rename=exn)
                cmds.file(f=1, save=1, type='mayaAscii')

            # 导出缓存
            if alembic:
                for i in alembic:
                    cmds.refresh()
                    k = i.keys()[0]
                    v = i.values()[0]
                    # 优化输出
                    for k0, vDict0 in self.itemDict['alembic'].items():
                        rn = k0 + 'RN'
                        if cmds.objExists(rn):
                            rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                            if k == k0:
                                cmds.setAttr(rootNUL + '.v', 1)
                            else:
                                cmds.setAttr(rootNUL + '.v', 0)

                    # 时间滑条
                    if v[2] == 'anim':
                        abctime = self.itemDict['setting']['animSlider']
                    elif v[2] == 'cfx2':
                        abctime = self.itemDict['setting']['cfx2Slider']
                    # 渲染输出
                    interface.scriptEditor(self.label, 'command', '正在导出 {0}{1}{2} 缓存'.format(k, ':', 'animation'))
                    cmds.refresh()
                    root = v[3] + ':srfNUL'
                    file = cacheDir + '/' + proj + '_' + v[0] + '_' + k + '_ani.abc'
                    self.alembicCmds(abctime, root, file)
                    # 解算缓存
                    if v[2] == 'cfx2':
                        interface.scriptEditor(self.label, 'command', '正在导出 {0}{1}{2} 缓存'.format(k, ':', 'simulation'))
                        cmds.refresh()
                        root = v[3] + ':simNUL'
                        file = cacheDir + '/' + proj + '_' + v[0] + '_' + k + '_sim.abc'
                        self.alembicCmds(abctime, root, file)

                # 全部显示
                for k0, vDict0 in self.itemDict['alembic'].items():
                    rn = k0 + 'RN'
                    if cmds.objExists(rn):
                        rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                        cmds.setAttr(rootNUL + '.v', 1)
                interface.scriptEditor(self.label, 'result', '缓存导出工作完成.')

            # 导出场景
            if scene:
                cmds.refresh()
                asmfile = cacheDir + '/' + proj + '_set_scene_ani.ma'
                if cmds.objExists('editsManager1'):
                    scene.append('editsManager1')
                cmds.select(scene, r=1)
                # cmds.file(asmfile, f=1, typ='mayaAscii', es=1, ch=1, con=1, chn=1, eas=0, sh=1, pr=1)
                cmds.file(asmfile, force=1, options="v=0;", typ="mayaAscii", pr=1, es=1)
                interface.scriptEditor(self.label, 'result', '场景导出工作完成.')

            # 拷贝到服务器
            if self.drive != drive:
                severDir = cacheDir.replace(drive, self.drive)
                cmds.sysFile(severDir, makeDir=True)
                files = cmds.getFileList(folder=cacheDir, filespec='*.*')
                if files:
                    for i in files:
                        cmds.refresh()
                        cmds.sysFile(cacheDir + '/' + i, copy=severDir + '/' + i)
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
            pypath = envpath.MAYAPATH + '/scripts/export/ani/aniPromptMain.py'
            if not os.path.exists(pypath):
                pypath = envpath.MAYAPATH + '/scripts/export/ani/aniPromptMain.pyc'
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