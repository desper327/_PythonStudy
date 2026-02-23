# -*- coding: utf-8 -*-

import logging
import os
import re
import inspect
from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
import maya.mel as mel

from core import config, interface, framework
from publish.gui import publishWindow as UI
from publish.gui.pluguiWidget import PluguiWidget
from publish.gui.helpuiWidget import HelpuiWidget
from startup import removes
import envpath

PROJECTS = envpath.ROOTPATH.rsplit('\\', 3)[0] + '/config/projects'
PLUGROOT = envpath.ROOTPATH + '/publish/plugins'
XBMLANGPATH = envpath.ROOTPATH.rsplit('\\', 1)[0] + '/icons'
LOG = logging.getLogger("publish")


class Menu(QtWidgets.QMenu):
    SigParams = QtCore.Signal(dict)
    SigScripts = QtCore.Signal(list)
    SigCommand = QtCore.Signal()

    def __init__(self, parent=None):
        super(Menu, self).__init__()
        self.parent = parent
        self.SigParams.connect(self.__parameter__)

    def __parameter__(self, msg):
        self.business = msg['business']
        self.abbrDir = msg['abbrDir']

    def clickMenu(self):
        menu = QtWidgets.QMenu(self.parent)
        menu.addAction("打开 work 文件夹...").triggered.connect(partial(self.openDir, 'open', 'work'))
        menu.addSeparator()
        if self.business == 'assets':
            menu.addAction("打开 submit 文件夹...").triggered.connect(partial(self.openDir, 'open', 'submit'))
        else:
            menu.addAction("打开 dailies 文件夹...").triggered.connect(partial(self.openDir, 'open', 'dailies'))
            menu.addAction("拷贝 dailies 文件夹最高版本到 publish 文件夹下...").triggered.connect(partial(self.openDir, 'copy', 'dailies'))
        menu.addSeparator()
        menu.addAction("打开 publish 文件夹...").triggered.connect(partial(self.openDir, 'open', 'publish'))
        menu.exec_(QtGui.QCursor.pos())

    def openDir(self, mode, stage):
        # 路径转换
        if stage == 'dailies':
            kind = self.abbrDir.split('/')[2]
            pathdir = self.abbrDir.replace(kind, 'dailies').replace('shots', kind)
        else:
            pathdir = self.abbrDir + '/' + stage

        if mode == 'open':
            # 打开文件夹
            if not os.path.exists(pathdir):
                self.SigScripts.emit(['warning', '{} 路径不存在'.format(pathdir)])
            else:
                os.startfile(pathdir)
                self.SigScripts.emit(['command', '文件夹成功打开'])
        elif mode == 'copy':
            if stage == 'submit':
                pubDir = self.abbrDir + '/publish'
            elif stage == 'dailies':
                pubDir = self.abbrDir + '/publish/v001'
                files = cmds.getFileList(folder=pubDir, filespec='*_*.json')
                if files:
                    self.SigScripts.emit(['warning', '发布版本存在,打开publish下文件完成后续操作'])
                else:
                    vers = cmds.getFileList(folder=pathdir, filespec='v*.')
                    if not vers:
                        self.SigScripts.emit(['error', '拷贝数据失败,dailies数据不存在'])
                    else:
                        vers.sort(reverse=True)
                        verDir = pathdir + '/' + vers[0]
                        files = cmds.getFileList(folder=verDir, filespec='*_*.*')
                        if files:
                            cmds.sysFile(pubDir, makeDir=True)
                            for i in files:
                                cmds.sysFile(verDir + '/' + i, copy=pubDir + '/' + i)
                        self.SigCommand.emit()
                        self.SigScripts.emit(['result', 'dailies转化publish版本成功'])


class Publish(MayaQWidgetDockableMixin, QtWidgets.QWidget, UI.Ui_Form):
    def __init__(self, abbr=None, tooltip=None):
        '''
        :param abbr: 部门简写
        :param tooltip: 工具提示
        '''
        super(Publish, self).__init__()

        # Delete existing UI
        try:
            cmds.deleteUI('PublishWorkspaceControl')
        except RuntimeError:
            pass

        # 静态参数
        self.abbr = abbr
        self.format = framework.fileFormat(self.abbr)
        self.kind = framework.department(self.abbr)[0]
        self.modules = framework.department(self.abbr)[1]
        if self.modules in ['layout', 'blocking']:
            self.modules = 'animation'

        # 动态参数
        self.itemLoading = False
        self.plugLoading = False

        # 装载界面
        if interface.license():
            self.setupUi(self)
            self.assemblyUi()
            self.connectUi()
            # self.optionVar(True)
            # self.publishEditUi()

            # 预设界面
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
                QGroupBox {
                    background-color: rgb(100,100,100);
                    border-radius: 5px;
                }
                QLabel{
                    border-radius: 2px;
                }
                QProgressBar { 
                    border-radius: 5px;
                    text-align: right;
                }
                QProgressBar::chunk { 
                    border-radius: 5px;
                }
                QLabel,QGroupBox,QCheckBox,QComboBox,QSpinBox,QSlider{
                    color: rgb(175, 175, 175);
                }
                QTextEdit{
                    border-radius: 2px;
                    border:1px solid rgb(50,50,50);
                    background-color: rgb(50,75,50);
                }
                QLineEdit{
                    border-radius: 2px;
                    border:1px solid rgb(50,50,50);
                    background-color: rgb(50,75,50);
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
            ''')
            self.QlwEnv.setStyleSheet('''
                QListWidget{
                    outline: 0px;
                    background-color: rgb(75,75,75);
                }
                QListWidget::item{
                    color: rgb(50,50,50);
                }
                QListWidget::item:hover{
                    color: rgb(200, 200, 200);
                    background-color: rgb(50,50,50);
                }
                QListWidget::item:selected{
                    background-color: rgb(175,125,175);
                    border-radius: 2px;
                }
            ''')

            self.label.setText(interface.copyright())
            self.version.setText('版本: ' + envpath.CTOOLKIT)

            # 存档右键菜单
            self.RM = Menu(self.tabArchive)
            self.RM.SigScripts.connect(self.scriptsUi)
            self.RM.SigCommand.connect(partial(self.archiveFiles, self))
            self.tabArchive.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.tabArchive.customContextMenuRequested.connect(self.menuUi)

        # 显示界面
        self.setObjectName('Publish')
        self.show(dockable=True)
        # self.show()
        if interface.license():
            self.optionVar(True)
            self.publishEditUi()

        # 刷新标题
        self.setWindowTitle(tooltip)

    def __parameter__(self):
        proj = self.QcbProject.currentText()
        jfile = PROJECTS + '/' + proj + '.json'

        projectDcit = config.project(jfile)['project']
        mayaDcit = config.project(jfile)['maya']

        # 初始参数
        self.dailies = True
        self.project = proj
        self.drive = projectDcit['drive']
        self.fps = projectDcit['playbackSpeed']
        self.resolutions = projectDcit['resolutions']
        self.startFrame = projectDcit['startFrame']
        self.mayaRender = mayaDcit['render']

    def assemblyUi(self):
        # 加载任务
        self.projectUi(self)
        # 隐藏进度条
        self.progressBar.setVisible(False)
        # 隐藏菜单栏
        self.gbSubmit.setVisible(False)
        if self.kind == 'assets':
            self.QcbBusiness.addItem('assets')
            if self.abbr == 'asm':
                self.tabWidget.removeTab(0)
                self.tabWidget.removeTab(2)
            elif self.abbr == 'mod':
                self.tabWidget.removeTab(0)
                self.tabWidget.removeTab(1)
                self.tabWidget.removeTab(1)
            else:
                self.tabWidget.removeTab(2)
                self.tabWidget.removeTab(2)
                self.QpbUpstream.setText('导入')
        elif self.kind == 'shots':
            self.QcbBusiness.addItems(['series', 'film'])
            self.tabWidget.removeTab(2)
            if self.abbr in ['sim', 'efx', 'lgt']:
                self.tabWidget.removeTab(0)
                if self.abbr in ['lgt']:
                    self.tabWidget.removeTab(1)
            else:
                if self.abbr in ['lay']:
                    self.QpbUpstream.setText('导入')
                else:
                    self.QpbUpstream.setText('打开')
            if self.abbr in ['lay', 'blk', 'ani', 'sim']:
                self.HUD = MayaHud()
        # ToolTip
        self.QlwTask.setToolTip('\n'
                                '说明\n'
                                '绿色：本地存在通过版本\n'
                                '如果有修改建议优先打开此文件另存工程文件后进行修改\n\n'
                                '黄色：本地存在提交版本\n'
                                '如果有修改建议次选打开此文件另存工程文件后进行修改\n\n'
                                '翠兰：本地工作文件\n\n'
                                '白色：本地空任务\n'
                                '\n')

    def connectUi(self):
        # gui
        self.QpbRefresh.clicked.connect(self.refreshUi)
        # Task
        self.QcbBusiness.activated.connect(self.businessUi)
        self.QcbProject.activated.connect(self.businessUi)
        if self.kind == 'shots':
            self.QcbBusiness.activated.connect(partial(self.extend2Ui, True))
            self.QcbProject.activated.connect(partial(self.extend2Ui, True))
        self.QcbBusiness.activated.connect(self.categoryUi)
        self.QcbBusiness.activated.connect(self.taskUi)
        self.QcbProject.activated.connect(self.categoryUi)
        self.QcbProject.activated.connect(self.taskUi)

        self.QcbExtend1.activated.connect(partial(self.extend2Ui, True))
        self.QcbExtend1.activated.connect(self.categoryUi)
        self.QcbExtend1.activated.connect(self.taskUi)
        self.QcbExtend2.activated.connect(partial(self.extend2Ui, False))
        self.QcbExtend2.activated.connect(self.categoryUi)
        self.QcbExtend2.activated.connect(self.taskUi)

        self.QcbCategory.activated.connect(self.taskUi)
        self.QlwTask.itemClicked.connect(self.archiveFiles)
        # Tab
        self.tabWidget.currentChanged.connect(self.tabChangedUi)
        # Tab.Upstream
        self.QpbUpstream.clicked.connect(partial(self.archiveApply, 'import'))
        # Tab.Archive
        self.QpbOpen.clicked.connect(partial(self.archiveApply, 'open'))
        self.QpbSave.clicked.connect(partial(self.archiveApply, 'save'))
        self.QpbWork.clicked.connect(partial(self.archiveApply, 'work'))
        # Tab.Submit
        self.QpbSubmit.clicked.connect(partial(self.submit, 'all'))
        # ->
        self.QcbProject.activated.connect(self.refreshUi)
        if self.abbr == 'asm':
            self.QcbProject.activated.connect(self.updateEnvUi)
        elif self.abbr in ['lay', 'blk', 'ani', 'sim']:
            self.QcbProject.activated.connect(self.updateDailiesUi)
        self.QcbCategory.activated.connect(self.refreshUi)
        # Tab.Env
        self.QleSearch.textEdited.connect(self.asmSearchUi)
        self.QlwEnv.itemDoubleClicked.connect(self.asmReference)

    def scriptsUi(self, msg):
        interface.scriptEditor(self.label, msg[0], msg[1])

    def menuUi(self, args):
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'warning', '选择任务对象后再次鼠标右键')
        else:
            emitDict = {
                'business': self.kind,
                'abbrDir': self.departmentDir
            }
            self.RM.SigParams.emit(emitDict)
            self.RM.clickMenu()

    def projectUi(self, args):
        # print 'projectUi'
        self.QcbProject.clear()
        jfiles = cmds.getFileList(folder=PROJECTS, filespec='*.json')
        if jfiles:
            jfiles.sort(reverse=False)
            for jfile in jfiles:
                proj = jfile.split('.')[0]
                if len(proj) == 4:
                    self.QcbProject.addItem(proj)
            # self.businessUi(args)

    def businessUi(self, args):
        # print 'businessUi'
        # 初始参数
        self.__parameter__()
        # 资产: assets
        self.business = self.QcbBusiness.currentText()
        if self.business == 'assets':
            self.frameBusiness2Shots.setHidden(True)
            self.workDir = self.drive + '/' + self.project + '/assets'
            # self.categoryUi(args)
        else:
            # 剧集: series
            if self.business == 'series':
                self.frameBusiness2Shots.setHidden(False)
                self.QcbExtend2.setHidden(False)
                self.QcbExtend1.setMaximumSize(QtCore.QSize(60, 16777215))
                self.shotsDir = self.drive + '/' + self.project + '/series/shots'
                self.extend1Ui()
                # self.extend2Ui(True)
                # self.categoryUi(args)
            # 电影: film
            elif self.business == 'film':
                self.frameBusiness2Shots.setHidden(False)
                self.QcbExtend2.setHidden(True)
                self.QcbExtend1.setMaximumSize(QtCore.QSize(128, 16777215))
                self.shotsDir = self.drive + '/' + self.project + '/film/shots'
                self.extend1Ui()
                # self.categoryUi(args)

    def extend1Ui(self):
        # print 'extend1Ui'
        # print('季 & 部')
        self.workDir = None
        self.QcbExtend1.clear()
        sfDirs = cmds.getFileList(folder=self.shotsDir, filespec='*.')
        if sfDirs:
            sfDirs.sort(reverse=True)
            self.QcbExtend1.addItems(sfDirs)
        else:
            self.QcbExtend1.addItem('None')
        self.workDir = self.shotsDir + '/' + self.QcbExtend1.currentText()

    def extend2Ui(self, *args):
        # print 'extend2Ui'
        # print('剧集/集')
        ext1Dir = self.shotsDir + '/' + self.QcbExtend1.currentText()
        if self.business == 'series':
            if args[0] == True:
                self.QcbExtend2.clear()
                epDirs = cmds.getFileList(folder=ext1Dir, filespec='ep*.')
                if epDirs:
                    epDirs.sort(reverse=True)
                    self.QcbExtend2.addItems(epDirs)
                else:
                    self.QcbExtend2.addItem('None')
            self.workDir = ext1Dir + '/' + self.QcbExtend2.currentText()
        elif self.business == 'film':
            self.workDir = ext1Dir

    def categoryUi(self, args):
        # print 'categoryUi'
        self.QcbCategory.clear()
        # 资产或镜头特定字符判断
        dirs = cmds.getFileList(folder=self.workDir, filespec='*.')
        if dirs:
            if self.business == 'assets':
                if self.abbr == 'asm':
                    category = ['set']
                elif self.abbr == 'rig':
                    category = ['chr', 'prp', 'veh', 'set']
                elif self.abbr == 'cfx':
                    category = ['chr', 'prp']
                else:
                    category = ['chr', 'prp', 'veh', 'env', 'set']

                dirs.sort(reverse=False)
                for dir in dirs:
                    if dir in category:
                        self.QcbCategory.addItem(dir)
            else:
                dirs.sort(reverse=True)
                for dir in dirs:
                    if dir[0] == 's' and dir[-3:].isdigit():
                        self.QcbCategory.addItem(dir)
        # self.taskUi(args)

    def taskUi(self, args):
        # print 'taskUi'
        self.QlwTask.clear()
        self.QlwUpstream.clear()
        self.QlwArchive.clear()
        if not self.QcbCategory.count():
            return

        # core: ['assets', 'series', 'film']
        category = self.QcbCategory.currentText()
        if self.business == 'assets':
            self.template = category
        elif self.business == 'series':
            self.template = '_'.join([self.QcbExtend1.currentText(), self.QcbExtend2.currentText(), category])
        elif self.business == 'film':
            self.template = '_'.join([self.QcbExtend1.currentText(), category])

        self.category = category
        self.categoryDir = self.workDir + '/' + category

        self.itemsDict = {}
        tasks = cmds.getFileList(folder=self.categoryDir, filespec='*.')
        if tasks:
            if self.kind == 'assets':
                tasks.sort(reverse=False)
                attrs = ['publish', 'submit', 'work']
                for task in tasks:
                    cmds.refresh()
                    item = QtWidgets.QListWidgetItem(task)
                    self.QlwTask.addItem(item)

                    templates = ['_'.join([task, self.abbr + self.format[0]]),
                                 'v*.',
                                 '_'.join([self.project, self.template, task, self.abbr, 'v*'+self.format[0]])]
                    for attr in attrs:
                        dirpath = os.path.join(self.categoryDir, task, self.abbr, attr)
                        if attr == attrs[0]:
                            files = cmds.getFileList(folder=dirpath, filespec=templates[0])
                            if files:
                                item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
                                self.itemsDict[task] = ('publish', templates)
                                break
                        elif attr == attrs[1]:
                            dirs = cmds.getFileList(folder=dirpath, filespec=templates[1])
                            if dirs:
                                item.setForeground(QtGui.QBrush(QtGui.QColor(175, 175, 75)))
                                self.itemsDict[task] = ('submit', templates)
                                break
                        elif attr == attrs[2]:
                            files = cmds.getFileList(folder=dirpath, filespec=templates[2])
                            if files:
                                item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 175)))
                                self.itemsDict[task] = ('work', templates)
                    # 空文件
                    if task not in self.itemsDict:
                        self.itemsDict[task] = (None, templates)
            else:
                tasks.sort(reverse=True)
                attrs = ['publish', 'dailies', 'work']
                for task in tasks:
                    cmds.refresh()
                    if task[0] == 'c' and task[1:5].isdigit():
                        item = QtWidgets.QListWidgetItem(task)
                        self.QlwTask.addItem(item)

                        templates = ['_'.join([task, self.abbr + self.format[0]]),
                                     'v*.',
                                     '_'.join([self.project, self.template, task, self.abbr, 'v*'+self.format[0]])]
                        for attr in attrs:
                            if attr == attrs[0]:
                                dirpath = os.path.join(self.categoryDir, task, self.abbr, attr)
                                dirs = cmds.getFileList(folder=dirpath, filespec=templates[1])
                                if dirs:
                                    item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
                                    self.itemsDict[task] = ('publish', templates)
                                    break
                            elif attr == attrs[1]:
                                if 'series' in self.categoryDir:
                                    tmppath = self.categoryDir.replace('series', 'dailies').replace('shots', 'series')
                                elif 'film' in self.categoryDir:
                                    tmppath = self.categoryDir.replace('film', 'dailies').replace('shots', 'film')
                                dirpath = os.path.join(tmppath, task, self.abbr)
                                dirs = cmds.getFileList(folder=dirpath, filespec=templates[1])
                                if dirs:
                                    item.setForeground(QtGui.QBrush(QtGui.QColor(175, 175, 75)))
                                    self.itemsDict[task] = ('dailies', templates)
                                    break
                            elif attr == attrs[2]:
                                dirpath = os.path.join(self.categoryDir, task, self.abbr, attr)
                                files = cmds.getFileList(folder=dirpath, filespec=templates[2])
                                if files:
                                    item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 175)))
                                    self.itemsDict[task] = ('work', templates)
                        # 空文件
                        if task not in self.itemsDict:
                            self.itemsDict[task] = (None, templates)

    def updateEnvUi(self, *args):
        if self.tabObjectName == 'tabEnv':
            # 切换项目清空items
            self.QlwEnv.clear()

            # 更新机制
            items = {}
            for i in range(self.QlwEnv.count()):
                obj = self.QlwEnv.item(i)
                items[obj.text()] = obj

            # 控件预设参数
            self.QlwEnv.setDragEnabled(False)

            self.envDir = self.drive + '/' + self.project + '/assets/env'
            tasks = cmds.getFileList(folder=self.envDir, filespec='*.')
            if tasks:
                tasks.sort(reverse=False)
                for task in tasks:
                    cmds.refresh()
                    if task not in items.keys():
                        item = QtWidgets.QListWidgetItem(task)
                        self.QlwEnv.addItem(item)
                        item.setSizeHint(QtCore.QSize(96, 96 + 22))
                        item.setToolTip('\ntask: ' + task + '   \n')
                    else:
                        item = items[task]

                    miss = []
                    asmfile = self.envDir + '/' + task + '/asm/publish/' + task + '.mb'
                    srffile = self.envDir + '/' + task + '/srf/publish/' + task + '_srf_pxy.mb'
                    if os.path.exists(asmfile) and os.path.exists(srffile):
                        rgb = [75, 175, 75]
                    else:
                        rgb = [125, 125, 125]
                        miss.append(1)

                    # 头像
                    avatar = self.envDir + '/' + task + '/avatar.jpg'
                    if not os.path.exists(avatar):
                        if miss:
                            avatar = XBMLANGPATH + '/task404.jpg'
                        else:
                            avatar = XBMLANGPATH + '/task.jpg'

                    # 颜色
                    item.setBackground(QtGui.QBrush(QtGui.QColor(rgb[0], rgb[1], rgb[2])))
                    item.setIcon(QtGui.QIcon(avatar))

    def asmSearchUi(self, args):
        search = self.QleSearch.text().lower()
        for i in range(self.QlwEnv.count()):
            cmds.refresh()
            if search != '':
                item = self.QlwEnv.item(i).text().lower()
                if search in item:
                    self.QlwEnv.item(i).setHidden(False)
                else:
                    self.QlwEnv.item(i).setHidden(True)
            else:
                self.QlwEnv.item(i).setHidden(False)

    def asmReference(self, agrs):
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'warning', '请选择任务对象')
            return
        else:
            exist = []
            error = []
            setAR = self.task + '_set_AR'
            setARs = cmds.ls(self.task + '_set_AR*')
            for i in setARs:
                if i == setAR:
                    exist.append(i)
                else:
                    error.append(i)

            if not exist:
                interface.scriptEditor(self.label, 'warning', '请切回存档菜单选择存档文件后单击[打开]按钮')
                return
            elif error:
                interface.scriptEditor(self.label, 'warning', "场景内只能存在一个['{}_set_AR']文件,请手动删除多余的[*_set_AR*]文件".format(self.task))
                return
            elif '/work/' not in cmds.file(q=1, exn=1):
                interface.scriptEditor(self.label, 'warning', '请单击存档菜单下的[工程新版]按钮')
                return

        task = self.QlwEnv.currentItem().text()

        pxyfile = self.envDir + '/' + task + '/srf/publish/' + task + '_srf_pxy.mb'
        if os.path.exists(pxyfile):
            DS = task + '_env_DS'
            pxy = task + '_env_pxy'
            if not cmds.objExists(DS):
                cmds.group(em=1, name=DS)
            if not cmds.objExists(pxy):
                cmds.file(pxyfile,
                          i=1,
                          type="mayaBinary",
                          ignoreVersion=True,
                          ra=True,
                          mergeNamespacesOnClash=True,
                          namespace=":",
                          options="v=0;",
                          pr=1,
                          importFrameRate=True,
                          importTimeRange="override")
                cmds.rename(task + '_proxy', pxy)
                cmds.parent(pxy, DS)
            else:
                dpxy = cmds.instance(pxy, smartTransform=True)
                cmds.setAttr(dpxy[0] + '.v', 1)
                cmds.select(dpxy[0], r=1)
        else:
            interface.scriptEditor(self.label, 'warning', '丢失: ' + pxyfile)

    def updateDailiesUi(self, *args):
        if self.tabObjectName == 'tabDailies':
            # 判断Maya是否安装Quicktime
            if 'qt' not in cmds.playblast(q=1, format=1):
                self.QcbFormat.addItem('none')
            else:
                self.QcbFormat.clear()
                self.QcbEncoding.clear()
                self.QcbFormat.addItem('qt')
                self.QcbEncoding.addItem('H.264')
                pdict = {
                    'project': self.project,
                    'scale': self.QsbScale.value(),
                    'instance': self
                }
                self.HUD.SigDict.emit(pdict)
                if self.dailies:
                    # Tab/Playblast
                    self.QcbDisplayViewport20.clicked.connect(partial(self.HUD.changed, 'viewport20'))
                    self.QcbOcclusion.clicked.connect(partial(self.HUD.changed, 'ssao'))
                    self.QcbBlur.clicked.connect(partial(self.HUD.changed, 'motionBlur'))
                    self.QcbSafeAction.clicked.connect(partial(self.HUD.changed, 'safeAction'))
                    self.QcbDisplayHUD.clicked.connect(partial(self.HUD.changed, 'hud'))
                    self.QcbDisplayShade.clicked.connect(partial(self.HUD.changed, 'shade'))
                    self.QcbDisplayWireframe.clicked.connect(partial(self.HUD.changed, 'wireframe'))
                    self.QcbDisplayCurves.clicked.connect(partial(self.HUD.changed, 'curves'))
                    self.QcbDisplayGrid.clicked.connect(partial(self.HUD.changed, 'grid'))
                    self.HUD.changed('viewport20')
                    self.HUD.changed('ssao')
                    self.HUD.changed('motionBlur')
                    self.HUD.changed('safeAction')
                    #
                    self.HUD.changed('shade')
                    self.HUD.changed('wireframe')
                    self.HUD.changed('curves')
                    self.HUD.changed('grid')
                    self.dailies = False

                # 预设参数
                self.QpbDailies.setVisible(False)
                self.QsbStart.setValue(self.startFrame)
                self.QsbEnd.setValue(cmds.playbackOptions(q=1, maxTime=1))
                self.QsbWidth.setValue(self.resolutions[0])
                self.QsbHeight.setValue(self.resolutions[1])
                self.QcbPlaybackSpeed.setCurrentText(self.fps)
                cmds.currentUnit(time=self.fps)
                cmds.playbackOptions(e=1, minTime=self.startFrame)
                cmds.setAttr('defaultResolution.width', self.resolutions[0])
                cmds.setAttr('defaultResolution.height', self.resolutions[1])
                self.QcbDisplayHUD.setChecked(True)
                self.HUD.changed('hud')

    def optionVar(self, *args):
        self.tabObjectName = self.tabWidget.currentWidget().objectName()
        if self.tabObjectName == 'tabArchive':
            exn = cmds.file(q=1, exn=1)
            if '/assets/' in exn or '/series/' in exn or '/film/' in exn:
                array = exn.split('/')
                if len(array) < 8:
                    pass
                else:
                    project = array[1]
                    if '/assets/' in exn:
                        category = array[3]
                        task = array[4]
                        process = array[6]
                        if process in ['work', 'publish', 'images']:
                            mfile = '/'.join(array[-2:])
                        elif process == 'submit':
                            mfile = '/'.join(array[-3:])
                        if args[0] == True:
                            self.QcbProject.setCurrentText(project)
                            self.businessUi(args)
                            self.categoryUi(args)
                            self.QcbCategory.setCurrentText(category)
                            self.taskUi(args)
                    elif '/series/' in exn or '/film/' in exn:
                        if '/series/' in exn:
                            business = 'series'
                            category = array[6]
                            task = array[7]
                        elif '/film/' in exn:
                            business = 'film'
                            category = array[5]
                            task = array[6]

                        if '/work/' in exn:
                            mfile = '/'.join(array[-2:])
                        elif '/publish/' in exn:
                            if '/cache/' in exn:
                                mfile = '/'.join(array[-4:])
                            else:
                                mfile = '/'.join(array[-3:])
                        elif '/dailies/' in exn:
                            mfile = 'dailies/' + '/'.join(array[-2:])
                        if args[0] == True:
                            self.QcbBusiness.setCurrentText(business)
                            self.QcbProject.setCurrentText(project)
                            self.businessUi(args)
                            self.QcbExtend1.setCurrentText(array[4])
                            if business == 'series':
                                # 集项切换
                                self.extend2Ui(True)
                                self.QcbExtend2.setCurrentText(array[5])
                            self.extend2Ui(False)
                            self.categoryUi(args)
                            self.QcbCategory.setCurrentText(category)
                            self.taskUi(args)
                    if self.QlwTask.count():
                        '''
                        item = self.QlwTask.findItems(task, QtCore.Qt.MatchRegExp)[0]
                        self.QlwTask.setCurrentItem(item)
                        self.QlwTask.scrollToItem(item)
                        '''
                        for i in range(self.QlwTask.count()):
                            item = self.QlwTask.item(i)
                            if item.text() == task:
                                self.QlwTask.setCurrentRow(i)
                                self.QlwTask.scrollToItem(item)
                                break

                        self.archiveFiles(args)
                        if self.QlwArchive.count():
                            for i in range(self.QlwArchive.count()):
                                item = self.QlwArchive.item(i)
                                if item.text() == mfile:
                                    self.QlwArchive.setCurrentRow(i)
                                    self.QlwArchive.scrollToItem(item)
                                    break
            else:
                if self.itemLoading == False:
                    self.businessUi(args)
                    if self.business == 'series':
                        self.extend2Ui(True)
                    self.categoryUi(args)
                    self.taskUi(args)
                    self.itemLoading = True

    def tabChangedUi(self, args):
        self.tabObjectName = self.tabWidget.currentWidget().objectName()
        if self.tabObjectName == 'tabUpstream':
            interface.scriptEditor(self.label, 'command', '上游菜单')
            self.archiveFiles(args)
        elif self.tabObjectName == 'tabArchive':
            interface.scriptEditor(self.label, 'command', '存档菜单')
            self.optionVar(False)
        elif self.tabObjectName == 'tabEnv':
            interface.scriptEditor(self.label, 'command', '环境菜单')
            self.updateEnvUi()
        elif self.tabObjectName == 'tabSubmit':
            interface.scriptEditor(self.label, 'command', '提交菜单')
            if self.plugLoading == False:
                self.publishUi()
                self.plugLoading = True
            self.publishEditUi()
        elif self.tabObjectName == 'tabDailies':
            interface.scriptEditor(self.label, 'command', '日报菜单')
            self.updateDailiesUi()
        elif self.tabObjectName == 'tabNotes':
            interface.scriptEditor(self.label, 'command', '注释菜单')

    def archiveFiles(self, args):
        # print 'archiveUi'
        self.QlwUpstream.clear()
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'Notes', '请选择任务对象')
            return
        else:
            interface.scriptEditor(self.label, 'command', '已选择任务对象')

        self.task = self.QlwTask.currentItem().text()
        self.taskDir = self.categoryDir + '/' + self.task
        self.departmentDir = self.taskDir + '/' + self.abbr

        if self.tabObjectName == 'tabUpstream':
            if self.abbr in ['rig', 'srf', 'cfx']:
                filename = self.task+'_mod.mb'
                modFile = self.taskDir + '/mod/publish/' + filename
                if os.path.exists(modFile):
                    item = QtWidgets.QListWidgetItem('mod/publish/' + filename)
                    self.QlwUpstream.addItem(item)
                    item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
                if self.category in ['chr', 'prp'] and self.abbr == 'rig':
                    filename = self.task + '_sim.abc'
                    simFile = self.taskDir + '/cfx/publish/' + filename
                    if os.path.exists(simFile):
                        item = QtWidgets.QListWidgetItem('cfx/publish/' + filename)
                        self.QlwUpstream.addItem(item)
                        item.setForeground(QtGui.QBrush(QtGui.QColor(175, 75, 175)))
                elif self.category == 'set' and self.abbr == 'srf':
                    filename = self.task + '_rig.mb'
                    rigFile = self.taskDir + '/rig/publish/' + filename
                    if os.path.exists(rigFile):
                        item = QtWidgets.QListWidgetItem('rig/publish/' + filename)
                        self.QlwUpstream.addItem(item)
                        item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
            elif self.abbr in ['lay']:
                camera = envpath.MAYAPATH + '/examples/layout/camera_ue4.mb'
                item = QtWidgets.QListWidgetItem('examples/layout/camera_ue4.mb')
                self.QlwUpstream.addItem(item)
                if os.path.exists(camera):
                    item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
                else:
                    item.setForeground(QtGui.QBrush(QtGui.QColor(175, 75, 75)))
            elif self.abbr in ['blk', 'ani']:
                if self.abbr == 'blk':
                    up = ['lay']
                elif self.abbr == 'ani':
                    up = ['lay', 'blk']
                for i in up:
                    pubDir = self.taskDir + '/' + i + '/publish'
                    dirs = cmds.getFileList(folder=pubDir, filespec='v*.')
                    if dirs:
                        dirs.sort(reverse=True)
                        mfile = pubDir + '/' + dirs[0] + '/' + self.task + '_' + i + '.ma'
                        if os.path.exists(mfile):
                            item = QtWidgets.QListWidgetItem(i + '/publish/' + dirs[0] + '/' + self.task + '_' + i + '.ma')
                            self.QlwUpstream.addItem(item)
                            item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
        elif self.tabObjectName == 'tabArchive':
            self.QlwArchive.clear()
            if self.kind == 'assets':
                # 列表框添加 [publish, submit, work] 文件
                attrs = ['publish', 'submit', 'work']
                lists = self.itemsDict[self.task][1]
                for i in range(len(attrs)):
                    cmds.refresh()
                    dirpath = os.path.join(self.departmentDir, attrs[i])
                    if attrs[i] == attrs[1]:
                        dirs = cmds.getFileList(folder=dirpath, filespec='v*.')
                        if dirs:
                            dirs.sort(reverse=True)
                            for dir in dirs:
                                file = dirpath + '/' + dir + '/' + lists[0]
                                if os.path.exists(file):
                                    item = QtWidgets.QListWidgetItem(attrs[i] + '/' + dir + '/' + lists[0])
                                    self.QlwArchive.addItem(item)
                                    item.setForeground(QtGui.QBrush(QtGui.QColor(175, 175, 75)))
                    else:
                        files = cmds.getFileList(folder=dirpath, filespec=lists[i])
                        if files:
                            files.sort(reverse=True)
                            for file in files:
                                item = QtWidgets.QListWidgetItem(attrs[i] + '/' + file)
                                self.QlwArchive.addItem(item)
                                if attrs[i] == attrs[0]:
                                    item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
                                elif attrs[i] == attrs[2]:
                                    item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 175)))
            else:
                # 列表框添加 [publish, submit, work] 文件
                files = ['client.ma', 'prompt.ma', 'classic.ma']
                attrs = ['publish', 'dailies', 'work']
                lists = self.itemsDict[self.task][1]
                for i in range(len(attrs)):
                    cmds.refresh()
                    if attrs[i] == 'work':
                        dirpath = os.path.join(self.departmentDir, attrs[i])
                        files = cmds.getFileList(folder=dirpath, filespec=lists[2])
                        if files:
                            files.sort(reverse=True)
                            for file in files:
                                item = QtWidgets.QListWidgetItem(attrs[i] + '/' + file)
                                self.QlwArchive.addItem(item)
                                item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 175)))
                    else:
                        if attrs[i] == 'publish':
                            dirpath = os.path.join(self.departmentDir, attrs[i])
                            rgb = [75, 175, 75]
                        else:
                            if 'series' in self.departmentDir:
                                dirpath = self.departmentDir.replace('series', 'dailies').replace('shots', 'series')
                            elif 'film' in self.departmentDir:
                                dirpath = self.departmentDir.replace('film', 'dailies').replace('shots', 'film')
                            rgb = [175, 175, 75]
                        dirs = cmds.getFileList(folder=dirpath, filespec=lists[1])
                        if dirs:
                            dirs.sort(reverse=True)
                            for dir in dirs:
                                file = dirpath + '/' + dir + '/' + lists[0]
                                if os.path.exists(file):
                                    item = QtWidgets.QListWidgetItem(attrs[i] + '/' + dir + '/' + lists[0])
                                    self.QlwArchive.addItem(item)
                                    item.setForeground(QtGui.QBrush(QtGui.QColor(rgb[0], rgb[1], rgb[2])))
                                # 列举偏移后动画文件
                                if self.project not in ['PPLU']:
                                    if attrs[i] == 'publish' and self.abbr in ['ani']:
                                        for ma in files:
                                            cfile = dirpath + '/' + dir + '/cache/' + ma
                                            if os.path.exists(cfile):
                                                item = QtWidgets.QListWidgetItem(attrs[i] + '/' + dir + '/cache/' + ma)
                                                self.QlwArchive.addItem(item)
                                                item.setForeground(QtGui.QBrush(QtGui.QColor(125, 75, 125)))
                                                break

    def archiveApply(self, mode):
        if mode == 'open':
            if not self.QlwArchive.selectedItems():
                interface.scriptEditor(self.label, 'warning', '选择任务及文件对象后单击[打开]按钮')
            else:
                item = self.QlwArchive.currentItem().text()
                if 'dailies/' in item:
                    if 'series' in self.departmentDir:
                        dirpath = self.departmentDir.replace('series', 'dailies').replace('shots', 'series')
                    elif 'film' in self.departmentDir:
                        dirpath = self.departmentDir.replace('film', 'dailies').replace('shots', 'film')
                    mfile = os.path.join(dirpath, item.replace('dailies/', ''))
                else:
                    mfile = os.path.join(self.departmentDir, item)
                cmds.file(mfile, f=1, options="v=0;", ignoreVersion=1, o=1)
                arNode = self.task + '_set_AR'
                if cmds.objExists(arNode):
                    cmds.assembly(arNode, edit=True, activeLabel='ModCache')
                self.refreshUi()
                interface.scriptEditor(self.label, 'command', '成功打开文件')
        elif mode == 'import':
            if not self.QlwUpstream.selectedItems():
                interface.scriptEditor(self.label, 'warning', '选择文件对象后单击[导入]按钮')
            else:
                mfile = self.taskDir + '/' + self.QlwUpstream.currentItem().text()
                if self.kind == 'assets':
                    if '.mb' in mfile:
                        cmds.file(mfile,
                                  i=1,
                                  type='mayaBinary',
                                  ignoreVersion=True,
                                  ra=True,
                                  mergeNamespacesOnClash=True,
                                  namespace=':',
                                  options='v=0;',
                                  pr=True,
                                  importFrameRate=True,
                                  importTimeRange="override")
                        interface.scriptEditor(self.label, 'result', '文件导入成功: {}'.format(mfile))
                    elif '.abc' in mfile:
                        # 加载插件
                        if not cmds.pluginInfo('AbcImport.mll', q=1, loaded=1):
                            cmds.loadPlugin('AbcImport.mll')
                        cmds.AbcImport(mfile,
                                       mode='import',
                                       fitTimeRange=1)
                    interface.scriptEditor(self.label, 'result', '文件导入成功: {}'.format(mfile))
                elif self.kind == 'shots':
                    if self.abbr in ['lay']:
                        if cmds.objExists('CamGroup'):
                            interface.scriptEditor(self.label, 'warning', "禁止重复导入['examples/layout/camera_ue4.mb']")
                        else:
                            cfile = envpath.MAYAPATH + '/' + self.QlwUpstream.currentItem().text()
                            if not os.path.exists(cfile):
                                interface.scriptEditor(self.label, 'error', "摄像机绑定文件内部摄像命名必须为['camera_ue4'],请将绑定师绑定通过的摄像机文件存放到如下路径\n"
                                                                            "地址: {}".format(cfile))
                            else:
                                cmds.file(cfile,
                                          i=1,
                                          type='mayaBinary',
                                          ignoreVersion=True,
                                          ra=True,
                                          mergeNamespacesOnClash=True,
                                          namespace=':',
                                          options='v=0;',
                                          pr=True,
                                          importFrameRate=True,
                                          importTimeRange="override")
                                interface.scriptEditor(self.label, 'result', '文件导入成功: {}'.format(cfile))
                    else:
                        cmds.file(mfile, f=1, options="v=0;", ignoreVersion=1, o=1)
                        interface.scriptEditor(self.label, 'command', '上游文件成功打开')
        else:
            if not self.QlwTask.selectedItems():
                interface.scriptEditor(self.label, 'warning', "请选择任务对象后完成存档菜单下['保存','工程']功能")
            else:
                # 移除无用节点
                removes.Munknown().default()
                # 保存文件
                exn = cmds.file(q=1, exn=1)
                if mode == 'save':
                    if '/untitled' in exn:
                        interface.scriptEditor(self.label, 'error', '空标题文件禁止保存')
                    else:
                        if '/submit/' in exn or '/publish/' in exn or '/dailies/' in exn:
                            interface.scriptEditor(self.label, 'warning', '提交/通过的文件禁止保存,单击[工程新版]转为工程新版')
                        else:
                            if self.departmentDir not in exn:
                                interface.scriptEditor(self.label, 'warning', '请使用存档下[打开]按钮打开文件')
                                return
                            if cmds.file(q=True, modified=True):
                                cmds.file(f=1, save=1)
                                interface.scriptEditor(self.label, 'command', '成功保存文件')
                            else:
                                interface.scriptEditor(self.label, 'command', '无需保存文件')
                elif mode == 'work':
                    if '/untitled' in cmds.file(q=1, exn=1):
                        interface.scriptEditor(self.label, 'error', '空标题文件,可以手动另存文件后再次单击[工程新版]')
                    else:
                        if '/publish/' in exn and '/v' in exn and '/cache/' in exn:
                            interface.scriptEditor(self.label, 'warning', '缓存文件禁止转为工程新版,单击[保存当前]按钮完成文件保存;通过[aniabc]工具完成缓存输出覆盖')
                        else:
                            task = self.QlwTask.currentItem().text()
                            filename = '_'.join([self.project, self.template, task, self.abbr])
                            p = []
                            count = self.QlwArchive.count()
                            if count:
                                for i in range(count):
                                    item = self.QlwArchive.item(i).text()
                                    if 'work/' in item:
                                        p.append(1)
                                        array = item.split('_')
                                        count = int(re.sub('\D', '', array[-1])) + 1
                                        filename += '_v' + str(count).zfill(3) + self.format[0]
                                        break
                            if not p:
                                filename += '_v001' + self.format[0]
                            workDir = self.departmentDir + '/work'
                            cmds.sysFile(workDir, makeDir=True)
                            mfile = workDir + '/' + filename
                            cmds.file(rename=mfile)
                            cmds.file(f=1, save=1, type=self.format[1])
                            interface.scriptEditor(self.label, 'command', '工程新版保存成功')
                            # self.archiveFiles(self)
                            self.tabChangedUi(False)

    def importPlugin(self, plug, department=None):
        dirs = ['publish', 'plugins']
        if department:
            dirs.append(department)

        dirs.append(plug)
        module = '.'.join(dirs)

        # pluginMod = importlib.import_module(module)
        pluginMod = __import__(module, fromlist=plug)
        reload(pluginMod)

        plugin = None
        for name, obj in inspect.getmembers(pluginMod):
            if inspect.isclass(obj):
                # LOG.info('imported plugin "{}"'.format(name))
                if self.kind in obj.ignoreType:
                    pass
                elif self.abbr in obj.ignoreType:
                    pass
                else:
                    if obj.default == True:
                        plugin = obj
        return plugin

    def getPlugins(self):
        '''
        collectors: 解析给定的工作场景中可用的实例
        checklist: 在验证器之前运行检查表插件
        validators: 验证/检查/测试单个实例的正确性
        extractors: 在物理上将Instance和Application分离到相应的资源中
        integrators: 将发布集成到发布管道中
        '''
        pluginDict = {'collectors': [],
                      'checklist': [],
                      'validators': [],
                      'extractors': [],
                      'integrators': []
                      }
        search = []
        processedPlugins = []
        for location in (PLUGROOT, self.modules):
            search.append(location)
            path = os.path.join(*search)
            if not os.path.exists(path):
                break
            for plugFile in os.listdir(path):
                # 指定格式加载
                if not plugFile.endswith('.pyd'):
                    if not plugFile.endswith('.pyc'):
                        if not plugFile.endswith('.py'):
                            continue

                if plugFile in ['__init__.py', '__init__.pyc']:
                    continue

                # 定义模块路径
                plugPath = os.path.join(path, plugFile)
                plugName = plugFile.split('.')[0]

                # 移除重复加载
                if plugName in processedPlugins:
                    continue
                # LOG.info('plugName {}'.format(plugName))
                processedPlugins.append(plugName)

                # 动态模块加载
                args = search[1:]
                _plugin = self.importPlugin(plugName, *args)
                if _plugin is None:
                    # LOG.info('__unload plugin "{}"'.format(plugName))
                    continue

                # 插件分类装载
                if plugName.startswith('collect_'):
                    pluginDict['collectors'].append(_plugin)
                elif plugName.startswith('checklist_'):
                    pluginDict['checklist'].append(_plugin)
                elif plugName.startswith('validate_'):
                    pluginDict['validators'].append(_plugin)
                elif plugName.startswith('extract_'):
                    pluginDict['extractors'].append(_plugin)
                elif plugName.startswith('integrate_'):
                    pluginDict['integrators'].append(_plugin)
                else:
                    LOG.warning('Invalid plugin skipped: "{}"'.format(plugPath))

        # 按照plugin的order数值排序
        for key in pluginDict.keys():
            pluginDict[key] = sorted(pluginDict[key], key=lambda value: value.order)
        return pluginDict

    def refreshUi(self, *args):
        if self.plugLoading:
            self.state = False
            self.helpDict = {}
            self.QpbSubmit.setText('验证')
            for k, vList in self.plugins.items():
                cmds.refresh()
                for i in range(len(vList)):
                    plugin = vList[i]['plugin']
                    plugui = vList[i]['plugui']
                    helpui = vList[i]['helpui']
                    category = self.QcbCategory.currentText()
                    if category in plugin.ignoreType:
                        self.plugins[k][i]['status'] = 'skip'
                        plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                       "padding-left: 4px;"
                                                       "padding-bottom: 2px;"
                                                       "background-color: rgb(50,50,50);")
                    else:
                        self.plugins[k][i]['status'] = None
                        plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                       "padding-left: 4px;"
                                                       "padding-bottom: 2px;"
                                                       "background-color: rgb(100,100,100);")
                    if helpui:
                        for m in range(helpui.gridLayout.count()):
                            helpui.gridLayout.itemAt(m).widget().deleteLater()
                        self.plugins[k][i]['helpui'] = None
            self.gbSubmit.setVisible(False)
            interface.scriptEditor(self.label, 'result', '提交菜单界面刷新完成')

    def publishUi(self):
        self.helpDict = {}
        '''
        module: 模块对象
        plugin: 插件实例对象
        plugui: 页面实例对象
        status: 实例进程状态
        helpui: 帮助页面实例
        params: 帮助页面参数
        '''
        self.state = False
        self.plugins = self.getPlugins()
        for k, plugList in self.plugins.items():
            for i in range(len(plugList)):
                cmds.refresh()
                plugObject = plugList[i]()
                pwuiObject = PluguiWidget(label=plugObject.label)
                self.plugins[k][i] = {
                    'module': plugList[i],
                    'plugin': plugObject,
                    'plugui': pwuiObject,
                    'status': None,
                    'helpui': None,
                    'params': {
                        'doc': plugList[i].__doc__,
                        'classed': plugList[i].__name__,
                        'optional': plugObject.optional,
                        'default': plugObject.default,
                        'error': None
                    }
                }

                if k == 'collectors':
                    self.collectorsLayout.addLayout(pwuiObject.vLayout)
                elif k == 'checklist':
                    self.checklistLayout.addLayout(pwuiObject.vLayout)
                elif k == 'validators':
                    self.validatorsLayout.addLayout(pwuiObject.vLayout)
                elif k == 'extractors':
                    self.extractorsLayout.addLayout(pwuiObject.vLayout)
                elif k == 'integrators':
                    self.integratorsLayout.addLayout(pwuiObject.vLayout)

                if hasattr(plugObject, 'process'):
                    pwuiObject.QpbExpand.clicked.connect(partial(self.subroutine, self.plugins[k][i]))
                else:
                    pwuiObject.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                       "padding-left: 4px;"
                                                       "padding-bottom: 2px;"
                                                       "background-color: rgb(50,50,50);")
                    pwuiObject.QpbHelp.setStyleSheet("background-color: rgb(50,50,50);"
                                                     "padding-bottom: 2px;")

    def publishEditUi(self):
        if self.tabObjectName == 'tabSubmit':
            category = self.QcbCategory.currentText()
            for k, plugList in self.plugins.items():
                for i in range(len(plugList)):
                    plugin = plugList[i]['plugin']
                    plugui = plugList[i]['plugui']
                    if category in plugin.ignoreType:
                        self.plugins[k][i]['status'] = 'skip'
                        plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                       "padding-left: 4px;"
                                                       "padding-bottom: 2px;"
                                                       "background-color: rgb(50,50,50);")
                    else:
                        status = plugList[i]['status']
                        if status == 'skip':
                            self.plugins[k][i]['status'] = None
                            plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                           "padding-left: 4px;"
                                                           "padding-bottom: 2px;"
                                                           "background-color: rgb(100,100,100);")

    def subroutine(self, args):
        plugin = args['plugin']
        plugui = args['plugui']
        status = args['status']
        params = args['params']
        if status not in [None, 'skip']:
            if plugui not in self.helpDict:
                helpui = HelpuiWidget(plugin, status, params)
                args['helpui'] = helpui
                plugui.vLayout.addLayout(helpui.gridLayout)
                helpui.SigRepair.connect(partial(self.repair, args))
                helpui.SigIgnore.connect(partial(self.ignore, args))
                self.helpDict[plugui] = helpui
                plugui.QpbHelp.setText('-')
            else:
                plugui.QpbHelp.setText('+')
                helpui = self.helpDict[plugui]
                for i in range(helpui.gridLayout.count()):
                    helpui.gridLayout.itemAt(i).widget().deleteLater()
                self.helpDict.pop(plugui)

    def repair(self, args):
        plugin = args['plugin']
        plugui = args['plugui']
        helpui = args['helpui']
        try:
            plugin.repair(args)
        except Exception as dialog:
            helpui.Qerror.setText(str(dialog))

        # 继续验证界面内所有['黄色', '红色']条目,性价比 -> 改为单条验证
        self.submit(mode='one', item=plugin)
        status = args['status']
        if status == 'approve':
            if helpui:
                for i in range(helpui.gridLayout.count()):
                    helpui.gridLayout.itemAt(i).widget().deleteLater()
                self.helpDict.pop(plugui)
        interface.scriptEditor(self.label, 'repair', '<' + plugin.label + '>')

    def ignore(self, args):
        plugin = args['plugin']
        plugui = args['plugui']
        helpui = args['helpui']
        plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                       "padding-left: 4px;"
                                       "padding-bottom: 2px;"
                                       "background-color: rgb(100,100,100);"
                                       )
        plugui.QpbHelp.setText('+')
        if helpui:
            for i in range(helpui.gridLayout.count()):
                helpui.gridLayout.itemAt(i).widget().deleteLater()
            args['status'] = 'approve'
            self.helpDict.pop(plugui)

        # [收集：Rig与Cfx历史版本层级对比] 跳转规则,定义是否输出alembic
        module = args['module'].__name__
        if 'CollectRig2CfxDataContrast' in module:
            if cmds.objExists('Group.stage'):
                cmds.setAttr('Group.stage', 'half', type='string')

        # 打印
        interface.scriptEditor(self.label, 'ignore', '<' + plugin.label + '>')

    def submit(self, mode, item=None):
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'warning', '请选择任务对象')
            return
        if not self.QlwArchive.selectedItems():
            interface.scriptEditor(self.label, 'warning', '请切回存档菜单选择文件对象后再单击[验证]按钮')
            return
        if '/work/' not in cmds.file(q=1, exn=1):
            interface.scriptEditor(self.label, 'warning', '请单击存档菜单下的[工程新版]按钮')
            return

        if self.state == None:
            self.QpbSubmit.setText('验证')
            self.state = False
            self.refreshUi()
        elif self.state == False:
            window = {
                'category': self.QcbCategory.currentText(),
                'department': self.abbr,
                'departmentDir': self.departmentDir,
                'task': self.task,
                'taskDir': self.taskDir,
                'playbackSpeed': self.fps,
                'resolutions': self.resolutions,
                'startFrame': self.startFrame,
                'assetsDir': self.drive + '/' + self.project + '/assets',
                'project': self.project,
                'instance': self,
                'render': self.mayaRender,
                'business': self.QcbBusiness.currentText()
            }

            error = []
            for k, vlist in self.plugins.items():
                for i in range(len(vlist)):
                    cmds.refresh()
                    plugin = vlist[i]['plugin']
                    plugui = vlist[i]['plugui']
                    status = vlist[i]['status']

                    if status not in ['approve', 'skip']:
                        if mode == 'one' and item == plugin:
                            try:
                                plugin.process(**window)
                                plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                               "padding-left: 4px;"
                                                               "padding-bottom: 2px;"
                                                               "background-color: rgb(50,100,50);")
                                self.plugins[k][i]['status'] = 'approve'
                            except Exception as e:
                                optional = plugin.optional
                                self.plugins[k][i]['params']['optional'] = optional
                                if optional == True or hasattr(plugin, 'repair'):
                                    plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                                   "padding-left: 4px;"
                                                                   "padding-bottom: 2px;"
                                                                   "background-color: rgb(125,125,50);")
                                    self.plugins[k][i]['status'] = 'warning'
                                else:
                                    plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                                   "padding-left: 4px;"
                                                                   "padding-bottom: 2px;"
                                                                   "background-color: rgb(125,50,50);")
                                    self.plugins[k][i]['status'] = 'error'
                                self.plugins[k][i]['params']['error'] = e
                            return
                        elif mode == 'all':
                            try:
                                plugin.process(**window)
                                plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                               "padding-left: 4px;"
                                                               "padding-bottom: 2px;"
                                                               "background-color: rgb(50,100,50);")
                                self.plugins[k][i]['status'] = 'approve'
                            except Exception as e:
                                optional = plugin.optional
                                self.plugins[k][i]['params']['optional'] = optional
                                if optional == True or hasattr(plugin, 'repair'):
                                    plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                                   "padding-left: 4px;"
                                                                   "padding-bottom: 2px;"
                                                                   "background-color: rgb(125,125,50);")
                                    self.plugins[k][i]['status'] = 'warning'
                                    error.append(e)
                                else:
                                    plugui.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                                                   "padding-left: 4px;"
                                                                   "padding-bottom: 2px;"
                                                                   "background-color: rgb(125,50,50);")
                                    self.plugins[k][i]['status'] = 'error'
                                    error.append(e)
                                self.plugins[k][i]['params']['error'] = e

            if error:
                interface.scriptEditor(self.label, 'error', '请自上而下依次解决红色或黄色检查项')
            else:
                self.QpbSubmit.setText('提交')
                self.state = True
                if self.kind == 'shots':
                    self.gbSubmit.setVisible(True)
        elif self.state == True:
            taskDict = {
                'category': self.QcbCategory.currentText(),
                'dirpath': self.departmentDir,
                'task': self.task,
                'abbr': self.abbr,
                'format': self.format,
                'comment': None,
                'project': self.project,
                'instance': self,
                'render': self.mayaRender
            }
            if self.kind == 'assets':
                self.state = None
                self.QpbSubmit.setText('刷新')
                from publish import submitAssets
                reload(submitAssets)
                SA = submitAssets.SubmitAssets(**taskDict)
                SA.SigScriptEditor.connect(partial(interface.scriptEditor, self.label))
                SA.publish()
            elif self.kind == 'shots':
                v = []
                if self.QrbDailies.isChecked():
                    v.append('dailies')
                if self.QrbPublish.isChecked():
                    v.append('publish')

                if not v:
                    interface.scriptEditor(self.label, 'warning', '选择任意模式后,再次单击[提交]按钮.')
                else:
                    taskDict['submit'] = v[0]
                    self.state = None
                    self.QpbSubmit.setText('刷新')
                    self.gbSubmit.setVisible(False)
                    from publish import submitShots
                    reload(submitShots)
                    SS = submitShots.SubmitShots(**taskDict)
                    SS.SigScriptEditor.connect(partial(interface.scriptEditor, self.label))
                    SS.publish()


class MayaHud(QtCore.QObject):
    SigDict = QtCore.Signal(dict)

    def __init__(self):
        super(MayaHud, self).__init__()
        self.SigDict.connect(self.__params__)

    def __params__(self, msg):
        self.project = msg['project']
        self.scale = msg['scale']
        self.app = msg['instance']

    def hudProject(self):
        # project = self.app.QcbProject.currentText()
        return self.project

    def hudResolution(self):
        w = cmds.getAttr('defaultResolution.width')
        h = cmds.getAttr('defaultResolution.height')
        # scale = self.app.QsbScale.value()
        rslt = str(w) + '*' + str(h) + ' [' + str(self.scale) + '%]'
        return rslt

    def hudDate(self):
        currentDate = cmds.date()
        return currentDate

    def hudUser(self):
        username = os.environ['USERNAME'].lower()
        return username

    def hudCamera(self):
        camera = cmds.lookThru(q=1).split('|')[-1]
        # 获取版本号及版本路径
        if cmds.objExists('persp.version'):
            ver = cmds.getAttr('persp.version')
        else:
            ver = 'v001'
        return (camera.upper() + ' / ' + ver)

    def hudFrame(self):
        currentTime = cmds.currentTime(q=1)
        maxTime = cmds.playbackOptions(q=1, maxTime=1)
        time = str(int(currentTime)).zfill(3) + ' / ' + str(int(maxTime))
        return time

    def hudFocalLength(self):
        camera = cmds.lookThru(q=1)
        focal = cmds.getAttr(camera + '.focalLength')
        return focal

    def hudPlayblastSpeed(self):
        '''
        fps = self.app.QcbPlaybackSpeed.currentText()
        return fps
        '''
        cu = cmds.currentUnit(query=True, time=True)
        if cu == 'game':
            fps = '15fps'
        elif cu == 'film':
            fps = '24fps'
        elif cu == 'pal':
            fps = '25fps'
        elif cu == 'ntsc':
            fps = '30fps'
        elif cu == 'show':
            fps = '48fps'
        elif cu == 'palf':
            fps = '50fps'
        elif cu == 'ntscf':
            fps = '60fps'
        else:
            fps = cu
        return fps

    def hudSound(self):
        sounds = cmds.ls(type='audio')
        if sounds:
            sfile = cmds.getAttr(sounds[0]+'.filename')
            if os.path.exists(sfile):
                gPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
                audio = cmds.timeControl(gPlayBackSlider, q=1, sound=1)
                if audio:
                    return 'on'
                else:
                    return 'off'
            else:
                return 'none'
        else:
            return 'no audio'

    def hudRemove(self):
        # 删除初始HUD
        if cmds.headsUpDisplay(listHeadsUpDisplays=True):
            for i in cmds.headsUpDisplay(listHeadsUpDisplays=True):
                cmds.headsUpDisplay(i, remove=True)

    def headsUpDisplay(self):
        # 预设信息
        self.hudRemove()
        cmds.displayColor("headsUpDisplayLabels", 16, dormant=1)
        cmds.displayColor("headsUpDisplayValues", 16, dormant=1)
        cmds.displayPref(fm=2)
        cmds.displayPref(sfs=12)
        cmds.displayPref(dfs=16)

        # 创建自定义HUD
        # top
        cmds.headsUpDisplay('HUDProject', section=0, block=0, blockSize='large', labelFontSize='large',dataFontSize='large', c=self.hudProject, event='timeChanged')
        cmds.headsUpDisplay('HUDResolution', section=2, block=0, blockSize='large', labelFontSize='large',dataFontSize='large', c=self.hudResolution, event='timeChanged')
        cmds.headsUpDisplay('HUDDate', section=4, block=0, blockSize='large', label='', labelFontSize='large',dataFontSize='large', c=self.hudDate, atr=1)
        # bottom
        cmds.headsUpDisplay('HUDUser', section=5, block=0, label='Artist:', blockSize='large', labelFontSize='large',dataFontSize='large', c=self.hudUser, event='timeChanged')
        cmds.headsUpDisplay('HUDSound', section=5, block=1, label='Sound:', labelFontSize='large', dataFontSize='large',c=self.hudSound, event='timeChanged')
        cmds.headsUpDisplay('HUDCamera', section=7, block=0, blockSize='large', labelFontSize='large',dataFontSize='large', c=self.hudCamera, event='timeChanged')
        cmds.headsUpDisplay('HUDFrame', section=9, block=0, label='Frame:', blockSize='large', labelFontSize='large',dataFontSize='large', c=self.hudFrame, atr=1)
        cmds.headsUpDisplay('HUDFocal', section=9, block=1, label='Focal length:', labelFontSize='large',dataFontSize='large', c=self.hudFocalLength, event='timeChanged')
        cmds.headsUpDisplay('HUDSpeed', section=9, block=2, label='Playback speed:', labelFontSize='large',dataFontSize='large', c=self.hudPlayblastSpeed, event='timeChanged')

    def changed(self, mode):
        modelPanel = cmds.getPanel(withFocus=True)
        if mode == 'viewport20':
            if self.app.QcbDisplayViewport20.isChecked():
                mel.eval('setRendererInModelPanel  "ogsRenderer" "' + modelPanel + '";')
            else:
                mel.eval('setRendererInModelPanel  "base_OpenGL_Renderer" "' + modelPanel + '";')
        elif mode == 'ssao':
            if self.app.QcbOcclusion.isChecked():
                cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 1)
                cmds.setAttr('hardwareRenderingGlobals.ssaoAmount', 1.0)
                cmds.setAttr('hardwareRenderingGlobals.ssaoRadius', 16)
                cmds.setAttr('hardwareRenderingGlobals.ssaoFilterRadius', 16)
                cmds.setAttr('hardwareRenderingGlobals.ssaoSamples', 16)
            else:
                cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 0)
        elif mode == 'motionBlur':
            if self.app.QcbBlur.isChecked():
                cmds.setAttr('hardwareRenderingGlobals.motionBlurEnable', 1)
                cmds.setAttr('hardwareRenderingGlobals.motionBlurShutterOpenFraction', 0.2)
                cmds.setAttr('hardwareRenderingGlobals.motionBlurSampleCount', 8)
            else:
                cmds.setAttr('hardwareRenderingGlobals.motionBlurEnable', 0)
        elif mode == 'safeAction':
            camera = cmds.lookThru(q=True)
            if self.app.QcbSafeAction.isChecked():
                cmds.setAttr(camera + '.displaySafeAction', 1)
            else:
                cmds.setAttr(camera + '.displaySafeAction', 0)
        elif mode == 'hud':
            if self.app.QcbDisplayHUD.isChecked():
                self.headsUpDisplay()
            else:
                self.hudRemove()
        elif mode == 'shade':
            cmds.modelEditor(modelPanel, e=1, udm=0)
            if self.app.QcbDisplayShade.isChecked():
                cmds.modelEditor(modelPanel, edit=1, displayAppearance='smoothShaded', displayTextures=1,
                                 displayLights="default")
            else:
                cmds.modelEditor(modelPanel, edit=1, displayAppearance='smoothShaded', displayTextures=0,
                                 displayLights="default")
        elif mode == 'wireframe':
            if self.app.QcbDisplayWireframe.isChecked():
                cmds.modelEditor(modelPanel, e=1, wireframeOnShaded=1)
            else:
                cmds.modelEditor(modelPanel, e=1, wireframeOnShaded=0)
        elif mode == 'curves':
            if self.app.QcbDisplayCurves.isChecked():
                cmds.modelEditor(modelPanel, e=1, nurbsCurves=1)
            else:
                cmds.modelEditor(modelPanel, e=1, nurbsCurves=0)
        elif mode == 'grid':
            if self.app.QcbDisplayGrid.isChecked():
                cmds.modelEditor(modelPanel, e=1, grid=1)
            else:
                cmds.modelEditor(modelPanel, e=1, grid=0)