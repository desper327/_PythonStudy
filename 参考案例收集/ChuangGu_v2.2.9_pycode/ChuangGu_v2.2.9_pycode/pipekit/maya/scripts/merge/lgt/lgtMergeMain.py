# -*- coding: utf-8 -*-

import os
import re
import json
from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
import xgenm as xg

from core import config, interface, framework
from startup import removes
from merge.lgt import lgtMergeWindow as UI
import envpath

PROJECTS = envpath.ROOTPATH.rsplit('\\', 3)[0] + '/config/projects'
XBMLANGPATH = envpath.ROOTPATH.rsplit('\\', 1)[0] + '/icons'


class MenuView(QtWidgets.QMenu):
    SigParams = QtCore.Signal(dict)
    SigScripts = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(MenuView, self).__init__()
        self.parent = parent
        self.SigParams.connect(self.__parameter__)

    def __parameter__(self, msg):
        self.msg = msg

    def aniMenu(self):
        menu = QtWidgets.QMenu(self.parent)
        menu.addAction("选择图标AR切换到 Locator 模式").triggered.connect(partial(self.assemblyEdit, 'Locator'))
        menu.addSeparator()
        menu.addAction("选择图标AR切换到 ModBbox 模式").triggered.connect(partial(self.assemblyEdit, 'ModBbox'))
        menu.addAction("选择图标AR切换到 ModCache 模式").triggered.connect(partial(self.assemblyEdit, 'ModCache'))
        menu.addSeparator()
        menu.addAction("选择图标AR切换到 RigFiles 模式").triggered.connect(partial(self.assemblyEdit, 'RigFiles'))
        menu.addSeparator()
        menu.addAction("选择图标AR切换到 SrfProxy 模式").triggered.connect(partial(self.assemblyEdit, 'SrfProxy'))
        menu.addAction("选择图标AR切换到 SrfFiles 模式").triggered.connect(partial(self.assemblyEdit, 'SrfFiles'))
        menu.popup(QtGui.QCursor.pos())

    def assemblyEdit(self, mode):
        if not self.msg['select']:
            self.SigScripts.emit(['error', '选择头像后右键完成命令操作.'])
        else:
            error0 = []
            error1 = []
            for k, vDict in self.msg['select'].items():
                ar = vDict['outliner']
                if not cmds.objExists(ar):
                    tmp = 'set_' + ar.split('_')[0] + re.sub('\D', '', ar) + ':Group'
                    if cmds.objExists(tmp):
                        error1.append(tmp)
                    else:
                        error0.append(k)
                    break
                else:
                    cmds.refresh()
                    category = vDict['category']
                    if category in ['set']:
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
                        error1.append(k)

            if error0:
                self.SigScripts.emit(['error', '请在右侧组装菜单下完成执行后, 再次使用此功能.'])
            elif error1:
                self.SigScripts.emit(['warning', '{} 不支持AssemblyReference功能,隶属于RN切换功能.'.format(error1)])
            else:
                self.SigScripts.emit(['command', 'AR对象切换成功.'])


class MenuEdit(QtWidgets.QMenu):
    SigParams = QtCore.Signal(dict)
    SigScripts = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(MenuEdit, self).__init__()
        self.parent = parent
        self.SigParams.connect(self.__parameter__)

    def __parameter__(self, msg):
        self.abbrDir = msg['dirpath']

    def archiveMenu(self):
        menu = QtWidgets.QMenu(self.parent)
        menu.addAction("打开 work 文件夹...").triggered.connect(partial(self.openDir, 'work'))
        menu.addAction("打开 dailies 文件夹...").triggered.connect(partial(self.openDir, 'dailies'))
        menu.addSeparator()
        menu.addAction("打开 publish 文件夹...").triggered.connect(partial(self.openDir, 'publish'))
        menu.popup(QtGui.QCursor.pos())

    def openDir(self, stage):
        # 路径转换
        if stage == 'dailies':
            kind = self.abbrDir.split('/')[2]
            pathdir = self.abbrDir.replace(kind, 'dailies').replace('shots', kind)
        else:
            pathdir = self.abbrDir + '/' + stage
        # 打开文件夹
        if not os.path.exists(pathdir):
            self.SigScripts.emit(['warning', '{} 路径不存在'.format(pathdir)])
        else:
            os.startfile(pathdir)
            self.SigScripts.emit(['command', '文件夹成功打开'])


class Merge(MayaQWidgetDockableMixin, QtWidgets.QWidget, UI.Ui_MergeWin):
    def __init__(self, abbr=None, tooltip=None):
        '''
        :param abbr: 部门简写
        :param tooltip: 工具提示
        '''
        super(Merge, self).__init__()

        # 删除界面
        try:
            cmds.deleteUI('MergeWorkspaceControl')
        except RuntimeError:
            pass

        # 静态参数
        self.abbr = abbr
        self.format = framework.fileFormat(self.abbr)
        self.kind = framework.department(self.abbr)[0]
        self.modules = framework.department(self.abbr)[1]

        # 动态参数
        self.itemLoading = False
        self.itemDict = {}

        # 注册日期
        if interface.license():
            # 初始界面
            self.setupUi(self)
            # 组装界面
            self.assemblyUi()
            # 信号与曹
            self.connectUi()
            # 记忆操作
            # self.archiveVar(True)
            # 设置风格
            self.label.setText(interface.copyright())
            self.version.setText('版本: ' + envpath.CTOOLKIT)
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
                QGroupBox{
                    color: rgb(175, 175, 175);
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
            ''')
            # 右键菜单
            self.VM = MenuView(self.tabView)
            self.VM.SigScripts.connect(self.scriptsUi)
            self.tabView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.tabView.customContextMenuRequested.connect(self.viewMenuUi)
            self.EM = MenuEdit(self.tabEdit)
            self.EM.SigScripts.connect(self.scriptsUi)
            self.tabEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.tabEdit.customContextMenuRequested.connect(self.editMenuUi)

        # 显示界面
        self.setObjectName('Merge')
        self.show(dockable=True)
        # 记忆操作
        if interface.license():
            self.archiveVar(True)
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

    def viewMenuUi(self, args):
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'warning', '选择任务对象后再次鼠标右键')
        else:
            if self.itemDict['tabLayout'] == 'ani':
                chr = self.QlwAniCharacter.selectedItems()
                prp = self.QlwAniProp.selectedItems()
                set = self.QlwAniScene.selectedItems()
                items = chr + prp + set
                if items:
                    editDict = {'select': {}}
                    keys = ['alembic', 'camera', 'scene']
                    for i in items:
                        key = i.text()
                        for n in keys:
                            if self.itemDict[n]:
                                for k, vDict in self.itemDict[n].items():
                                    if key == k:
                                        editDict['select'][k] = vDict
                    self.VM.SigParams.emit(editDict)
                    self.VM.aniMenu()
                else:
                    interface.scriptEditor(self.label, 'warning', '选择头像对象后再次鼠标右键')
            else:
                pass

    def editMenuUi(self, args):
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'warning', '选择任务对象后再次鼠标右键')
        else:
            si = self.tabEdit.currentIndex()
            if si == 0:
                editDict = {
                    'dirpath': self.taskDir + '/' + self.abbr
                }
                self.EM.SigParams.emit(editDict)
                self.EM.archiveMenu()
            else:
                pass

    def scriptsUi(self, msg):
        interface.scriptEditor(self.label, msg[0], msg[1])

    def assemblyUi(self):
        # 加载插件
        plugins = ['animImportExport.mll', 'fbxmaya.mll', 'AbcImport.mll', 'sceneAssembly.mll', 'gpuCache.mll']
        for plugin in plugins:
            try:
                if not cmds.pluginInfo(plugin, q=1, loaded=1):
                    cmds.loadPlugin(plugin)
            except:
                print('//Result: plug-ins {} skip.'.format(plugin))

        # 加载任务
        self.projectUi(self)
        # 添加控件
        if self.abbr in ['efx', 'sim']:
            self.tabView.removeTab(1)
            self.tabView.removeTab(1)
        else:
            self.QlwEfxCache.setIconSize(QtCore.QSize(128, 70))
            self.QlwSimCharacter.setIconSize(QtCore.QSize(68, 68))
            self.QlwSimProp.setIconSize(QtCore.QSize(68, 68))

        if self.kind == 'shots':
            self.QcbBusiness.addItem('series')
            self.QcbBusiness.addItem('film')

        # 控件预设参数
        self.QlwAniCharacter.setIconSize(QtCore.QSize(68, 68))
        self.QlwAniProp.setIconSize(QtCore.QSize(68, 68))
        self.QlwAniScene.setIconSize(QtCore.QSize(128, 70))

        font = QtGui.QFont()
        font.setPointSize(10)
        listWidgets = [
            self.QlwAniCharacter, self.QlwAniProp, self.QlwAniScene,
            self.QlwEfxCache,
            self.QlwSimCharacter, self.QlwSimProp
        ]
        for listWidget in listWidgets:
            listWidget.setViewMode(QtWidgets.QListView.IconMode)
            listWidget.setResizeMode(listWidget.Adjust)
            listWidget.setDragEnabled(False)
            listWidget.setFont(font)
            listWidget.setSpacing(5)

            listWidget.setStyleSheet('''
                QListWidget{
                    outline: 0px;
                }
                QListWidget::item{
                    color: rgb(50,50,50);
                }
                QListWidget::item:hover{
                    background-color: rgb(75,75,75);
                    border-radius: 2px;
                    color: rgb(175, 100, 175)
                }
                QListWidget::item:selected{
                    color: rgb(200,200,75);
                    border: 2px solid rgb(200,200,75);
                    border-radius: 4px;
                }
            ''')

    def connectUi(self):
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
        self.QcbProject.activated.connect(self.tabEditChangedUi)

        self.QcbExtend1.activated.connect(partial(self.extend2Ui, True))
        self.QcbExtend1.activated.connect(self.categoryUi)
        self.QcbExtend1.activated.connect(self.taskUi)
        self.QcbExtend2.activated.connect(partial(self.extend2Ui, False))
        self.QcbExtend2.activated.connect(self.categoryUi)
        self.QcbExtend2.activated.connect(self.taskUi)
        self.QcbCategory.activated.connect(self.taskUi)
        self.QlwTask.itemClicked.connect(self.taskClickUi)
        # version
        self.QlwAniVersion.itemClicked.connect(self.tabViewSubsetsUi)
        self.QlwEfxVersion.itemClicked.connect(self.tabViewSubsetsUi)
        self.QlwSimVersion.itemClicked.connect(self.tabViewSubsetsUi)
        # TabView
        self.tabView.currentChanged.connect(self.tabViewChangedUi)
        self.tabEdit.currentChanged.connect(self.tabEditChangedUi)
        # Tab.Archive
        self.QpbOpen.clicked.connect(partial(self.tabEditArchive, 'open'))
        self.QpbSave.clicked.connect(partial(self.tabEditArchive, 'save'))
        self.QpbWork.clicked.connect(partial(self.tabEditArchive, 'work'))
        self.QpbMerge.clicked.connect(self.tabEditAssembly)

    def projectUi(self, args):
        self.QcbProject.clear()
        jfiles = cmds.getFileList(folder=PROJECTS, filespec='*.json')
        if jfiles:
            jfiles.sort(reverse=False)
            for jfile in jfiles:
                proj = jfile.split('.')[0]
                if len(proj) == 4:
                    self.QcbProject.addItem(proj)

    def businessUi(self, args):
        # 清除控件
        self.QlwAniCharacter.clear()
        self.QlwAniProp.clear()
        self.QlwAniScene.clear()
        self.QlwAniVersion.clear()
        self.QlwEfxCache.clear()
        self.QlwEfxVersion.clear()
        self.QlwSimCharacter.clear()
        self.QlwSimProp.clear()
        self.QlwSimVersion.clear()
        self.QlwArchive.clear()

        # 初始参数
        self.__parameter__()
        self.business = self.QcbBusiness.currentText()
        # 剧集: series
        if self.business == 'series':
            self.frameBusiness2Shots.setHidden(False)
            self.QcbExtend2.setHidden(False)
            self.QcbExtend1.setMaximumSize(QtCore.QSize(60, 16777215))
            self.shotsDir = self.drive + '/' + self.project + '/series/shots'
            self.extend1Ui()
            self.extend2Ui(True)
        # 电影: film
        elif self.business == 'film':
            self.frameBusiness2Shots.setHidden(False)
            self.QcbExtend2.setHidden(True)
            self.QcbExtend1.setMaximumSize(QtCore.QSize(128, 16777215))
            self.shotsDir = self.drive + '/' + self.project + '/film/shots'
            self.extend1Ui()

    def extend1Ui(self):
        # 季 & 部
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
        # 剧集/集
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
        self.QcbCategory.clear()
        # 镜头特定字符判断
        dirs = cmds.getFileList(folder=self.workDir, filespec='*.')
        if dirs:
            dirs.sort(reverse=True)
            for dir in dirs:
                if dir[0] == 's' and dir[-3:].isdigit():
                    self.QcbCategory.addItem(dir)

    def taskUi(self, args):
        self.QlwTask.clear()
        if not self.QcbCategory.count():
            return

        # core: ['series', 'film']
        category = self.QcbCategory.currentText()
        if self.business == 'series':
            self.template = '_'.join([self.QcbExtend1.currentText(), self.QcbExtend2.currentText(), category])
        elif self.business == 'film':
            self.template = '_'.join([self.QcbExtend1.currentText(), category])
        self.category = category
        self.categoryDir = self.workDir + '/' + category

        tasks = cmds.getFileList(folder=self.categoryDir, filespec='*.')
        if tasks:
            tasks.sort(reverse=True)
            attrs = ['ani', 'efx', 'sim']
            for task in tasks:
                cmds.refresh()
                if task[0] == 'c' and task[1:5].isdigit():
                    item = QtWidgets.QListWidgetItem(task)
                    self.QlwTask.addItem(item)
                    v = 0
                    for attr in attrs:
                        publishDir = self.categoryDir + '/' + task + '/' + attr + '/publish'
                        if os.path.exists(publishDir):
                            vers = cmds.getFileList(folder=publishDir, filespec='v*.')
                            if vers:
                                vers.sort(reverse=True)
                                abcs = cmds.getFileList(folder=publishDir + '/' + vers[0] + '/cache', filespec='*.abc')
                                if attr == 'ani':
                                    if abcs:
                                        v += 1
                                    else:
                                        fbxs = cmds.getFileList(folder=publishDir + '/' + vers[0] + '/cache', filespec='*_cam.fbx')
                                        if fbxs:
                                            v += 1
                                else:
                                    if abcs:
                                        v += 1

                    if v == 1:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(35, 150, 200)))
                    elif v == 2:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(175, 175, 75)))
                    elif v == 3:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(175, 75, 175)))

    def archiveVar(self, args):
        exn = cmds.file(q=1, exn=1)
        if '/series/' in exn or '/film/' in exn:
            array = exn.split('/')
            if len(array) < 8:
                pass
            else:
                project = array[1]
                if '/series/' in exn:
                    business = 'series'
                    category = array[6]
                    task = array[7]
                elif '/film/' in exn:
                    business = 'film'
                    category = array[5]
                    task = array[6]
                mfile = '/'.join(array[-2:])

                if args == True:
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
                    # 镜头条目
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
                    # 工程版本
                    self.taskClickUi(False)
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

    def taskClickUi(self, args):
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'Notes', '请选择任务对象')
            return
        else:
            interface.scriptEditor(self.label, 'command', '已选择任务对象')

        # 初始化
        self.itemDict = {}
        self.task = self.QlwTask.currentItem().text()
        self.taskDir = self.categoryDir + '/' + self.task
        self.departmentDir = self.taskDir + '/' + self.abbr

        # 触发编辑菜单
        self.tabEditQueryedUi(args)
        # 触发视窗菜单
        self.tabViewChangedUi(args)

    def tabViewChangedUi(self, args):
        self.viewVar = self.tabView.currentIndex()
        editVar = self.tabEdit.currentIndex()
        # 更新组装界面
        self.QcbMerge.clear()
        self.itemDict = {}
        if editVar == 1:
            if self.viewVar == 0:
                if self.mayaRender[0] == 'Arnold':
                    self.QcbMerge.addItems(['MaterialX'])
                else:
                    self.QcbMerge.addItems(['Connect'])
            elif self.viewVar == 1:
                self.QcbMerge.addItems(['Reference'])
            elif self.viewVar == 2:
                self.QcbMerge.addItems(['Replace'])
        # 更新左侧界面
        if self.QlwTask.selectedItems():
            if self.viewVar == 0:
                interface.scriptEditor(self.label, 'command', '动画缓存菜单')
                self.publishDir = self.taskDir + '/ani/publish'
                self.QlwAniCharacter.clear()
                self.QlwAniProp.clear()
                self.QlwAniScene.clear()
                self.QlwAniVersion.clear()
            elif self.viewVar == 1:
                interface.scriptEditor(self.label, 'command', '特效缓存菜单')
                self.publishDir = self.taskDir + '/efx/publish'
                self.QlwEfxCache.clear()
                self.QlwEfxVersion.clear()
            elif self.viewVar == 2:
                interface.scriptEditor(self.label, 'command', '解算缓存菜单')
                self.publishDir = self.taskDir + '/sim/publish'
                self.QlwSimCharacter.clear()
                self.QlwSimProp.clear()
                self.QlwSimVersion.clear()
                if editVar == 1:
                    self.QcbMerge.addItems(['Replace'])
            self.tabViewQueryedUi(args)

    def tabViewQueryedUi(self, args):
        # 添加版本
        vers = cmds.getFileList(folder=self.publishDir, filespec='v*.')
        if vers:
            vers.sort(reverse=True)
            for ver in vers:
                item = QtWidgets.QListWidgetItem(ver)
                if self.viewVar == 0:
                    self.QlwAniVersion.addItem(item)
                elif self.viewVar == 1:
                    self.QlwEfxVersion.addItem(item)
                elif self.viewVar == 2:
                    self.QlwSimVersion.addItem(item)

                if self.viewVar in [0, 1]:
                    abcs = cmds.getFileList(folder=self.publishDir + '/' + ver + '/cache', filespec='*.abc')
                    if abcs:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(75, 150, 75)))
                    else:
                        files = cmds.getFileList(folder=self.publishDir + '/' + ver, filespec='*.json')
                        if files:
                            item.setForeground(QtGui.QBrush(QtGui.QColor(150, 150, 75)))
                else:
                    dirs = cmds.getFileList(folder=self.publishDir + '/' + ver + '/cache', filespec='*_*.')
                    if dirs:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(75, 150, 75)))

            # 缓存使用版本及子集控件
            if self.taskDir in cmds.file(q=1, exn=1):
                if self.viewVar == 0:
                    if cmds.objExists('lgtRN'):
                        ver = cmds.referenceQuery('lgtRN', filename=1).rsplit('/')[-3]
                        item = self.QlwAniVersion.findItems(ver, QtCore.Qt.MatchRegExp)[0]
                        self.QlwAniVersion.setCurrentItem(item)
                        self.QlwAniVersion.scrollToItem(item)
                    else:
                        self.QlwAniVersion.setCurrentRow(0)
                elif self.viewVar == 1:
                    rns = cmds.ls('efx_*RN*')
                    if rns:
                        ver = cmds.referenceQuery(rns[0], filename=1).rsplit('/')[-3]
                        item = self.QlwEfxVersion.findItems(ver, QtCore.Qt.MatchRegExp)[0]
                        self.QlwEfxVersion.setCurrentItem(item)
                        self.QlwEfxVersion.scrollToItem(item)
                    else:
                        self.QlwEfxVersion.setCurrentRow(0)
                elif self.viewVar == 2:
                    self.QlwSimVersion.setCurrentRow(0)
                    rns = cmds.ls(['chr_*RN*', 'prp_*RN*'])
                    if rns:
                        filename = cmds.referenceQuery(rns[0], filename=1)
                        if '/sim/publish/v' in filename:
                            ver = filename.rsplit('/')[-4]
                            item = self.QlwSimVersion.findItems(ver, QtCore.Qt.MatchRegExp)[0]
                            self.QlwSimVersion.setCurrentItem(item)
                            self.QlwSimVersion.scrollToItem(item)
                        else:
                            self.QlwSimVersion.setCurrentRow(0)
                    else:
                        self.QlwSimVersion.setCurrentRow(0)
            else:
                if self.viewVar == 0:
                    self.QlwAniVersion.setCurrentRow(0)
                elif self.viewVar == 1:
                    self.QlwEfxVersion.setCurrentRow(0)
                elif self.viewVar == 2:
                    self.QlwSimVersion.setCurrentRow(0)
            self.tabViewSubsetsUi(args)

    def tabViewSubsetsUi(self, args):
        # Tab.Ani
        if self.viewVar == 0:
            self.itemDict['tabLayout'] = 'ani'
            # 清除控件
            self.QlwAniCharacter.clear()
            self.QlwAniProp.clear()
            self.QlwAniScene.clear()
            self.cacheDir = self.publishDir + '/' + self.QlwAniVersion.currentItem().text() + '/cache'

            jfile = self.cacheDir + '/__init__.json'
            if not os.path.exists(jfile):
                interface.scriptEditor(self.label, 'error', '非标准数据,禁止加载')
            else:
                interface.scriptEditor(self.label, 'command', '标准数据,正常加载')
                with open(jfile, 'r') as fo:
                    cdict = json.load(fo)

            # 参数设置
            if 'setting' in cdict:
                self.itemDict['setting'] = cdict['setting']
            if 'connect' in cdict:
                self.itemDict['connect'] = cdict['connect']

            # 角色道具
            if 'alembic' in cdict:
                self.itemDict['alembic'] = {}
                for k, vDict in cdict['alembic'].items():
                    cmds.refresh()
                    category = vDict['category']
                    # 头像地址
                    name = re.sub(r'[0-9]+', '', k)
                    taskDir = self.drive + '/' + self.project + '/assets/' + category + '/' + name
                    avatar = taskDir + '/avatar.jpg'
                    if not os.path.exists(avatar):
                        avatar = XBMLANGPATH + '/task.jpg'

                    # 添加控件
                    item = QtWidgets.QListWidgetItem(k)
                    item.setSizeHint(QtCore.QSize(72, 72 + 18))
                    item.setIcon(QtGui.QIcon(avatar))
                    if category == 'chr':
                        self.QlwAniCharacter.addItem(item)
                    elif category in ['prp', 'veh']:
                        self.QlwAniProp.addItem(item)
                    # 定义字典
                    abcfile = self.cacheDir + '/' + '_'.join([self.project, category, k, 'ani.abc'])
                    srffile = taskDir + '/srf/publish/' + name + '_srf.mb'
                    shdfile = taskDir + '/srf/publish/' + name + '_srf_shd.mb'
                    sjsfile = taskDir + '/srf/publish/' + name + '_srf.json'
                    mtxfile = taskDir + '/srf/publish/' + name + '_srf.mtlx'
                    self.itemDict['alembic'][k] = {
                        'srfFile': srffile,
                        'shdFile': shdfile,
                        'sjsFile': sjsfile,
                        'mtxFile': mtxfile,
                        'refFile': abcfile,
                        'category': category,
                        'outliner': category + '_' + k + ':srfNUL'
                    }
                    # 颜色区分
                    if not os.path.exists(abcfile):
                        v = [125, 125, 125]
                    else:
                        simfile = self.cacheDir + '/' + '_'.join([self.project, category, k, 'sim.abc'])
                        if self.mayaRender[0] == 'Arnold':
                            if os.path.exists(mtxfile):
                                if os.path.exists(simfile):
                                    v = [150, 75, 150]
                                else:
                                    v = [75, 150, 75]
                            else:
                                v = [35, 150, 200]
                        else:
                            if os.path.exists(sjsfile):
                                if os.path.exists(simfile):
                                    v = [150, 75, 150]
                                else:
                                    v = [75, 150, 75]
                            else:
                                v = [35, 150, 200]
                    item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))

            # 摄像机
            if 'camera' in cdict:
                self.itemDict['camera'] = {}
                for k, vDict in cdict['camera'].items():
                    fbxfile = self.cacheDir + '/' + k.replace('ani', 'cam') + '.fbx'
                    self.itemDict['camera'][k] = {
                        'refFile': fbxfile,
                        'category': 'cam',
                        'outliner': 'lgt:' + k
                    }
                    if not os.path.exists(fbxfile):
                        v = [125, 125, 125]
                        avatar = XBMLANGPATH + '/camera_16x9_404.png'
                    else:
                        v = [75, 150, 75]
                        avatar = XBMLANGPATH + '/camera_16x9.png'
                    # 添加控件
                    item = QtWidgets.QListWidgetItem('camera')
                    item.setSizeHint(QtCore.QSize(128, 72 + 18))
                    item.setIcon(QtGui.QIcon(avatar))
                    item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))
                    self.QlwAniScene.addItem(item)

            # 场景元素
            if 'scene' in cdict:
                self.itemDict['scene'] = {}
                sexfile = self.cacheDir + '/' + '_'.join([self.project, 'set', 'scene', 'ani.ma'])
                for k, vDict in cdict['scene'].items():
                    cmds.refresh()
                    # 颜色区分
                    if not os.path.exists(sexfile):
                        v = [125, 125, 125]
                        avatar = XBMLANGPATH + '/scene_16x9_404.png'
                    else:
                        category = vDict['category']
                        if category == 'old':
                            v = [112, 128, 144]
                            avatar = XBMLANGPATH + '/scene_16x9.png'
                            self.itemDict['scene'][k] = {
                                'refFile': sexfile,
                                'category': category,
                                'outliner': vDict['outliner']
                            }
                        elif category == 'set':
                            name = re.sub(r'[0-9]+', '', k)
                            setfile = self.drive + '/' + self.project + '/assets/' + category + '/' + name + '/asm/publish/' + name + '_set.mb'
                            if os.path.exists(setfile):
                                v = [75, 150, 75]
                            else:
                                v = [125, 125, 125]

                            # 头像地址
                            avatar = self.drive + '/' + self.project + '/assets/' + category + '/' + name + '/avatar.jpg'
                            if not os.path.exists(avatar):
                                avatar = XBMLANGPATH + '/task_16x9.jpg'
                            self.itemDict['scene'][k] = {
                                'asmFile': setfile,
                                'refFile': sexfile,
                                'category': category,
                                'outliner': vDict['outliner']
                            }
                    # 添加控件
                    item = QtWidgets.QListWidgetItem(k)
                    item.setSizeHint(QtCore.QSize(128, 72 + 18))
                    item.setIcon(QtGui.QIcon(avatar))
                    item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))
                    self.QlwAniScene.addItem(item)
        # Tab.Efx
        elif self.viewVar == 1:
            self.itemDict['tabLayout'] = 'efx'
            self.QlwEfxCache.clear()
            self.cacheDir = self.publishDir + '/' + self.QlwEfxVersion.currentItem().text() + '/cache'
            abcs = cmds.getFileList(folder=self.cacheDir, filespec='*.abc')
            if abcs:
                self.itemDict['alembic'] = {}
                # 添加控件
                abcs.sort(reverse=False)
                for abc in abcs:
                    k = abc.split('.')[0]
                    item = QtWidgets.QListWidgetItem(k)
                    item.setSizeHint(QtCore.QSize(128, 72 + 18))
                    item.setIcon(QtGui.QIcon(XBMLANGPATH + '/alembic_16x9.png'))
                    item.setBackground(QtGui.QBrush(QtGui.QColor(75, 150, 75)))
                    self.QlwEfxCache.addItem(item)
                    # 定义字典
                    self.itemDict['alembic'][k] = {
                        'refFile': self.cacheDir + '/' + abc
                    }
        # Tab.Sim
        elif self.viewVar == 2:
            self.itemDict['tabLayout'] = 'sim'
            self.QlwSimCharacter.clear()
            self.QlwSimProp.clear()
            self.cacheDir = self.publishDir + '/' + self.QlwSimVersion.currentItem().text() + '/cache'

            jfile = self.cacheDir + '/__init__.json'
            if not os.path.exists(jfile):
                interface.scriptEditor(self.label, 'error', '非标准数据,禁止加载')
            else:
                interface.scriptEditor(self.label, 'command', '标准数据,正常加载')
                with open(jfile, 'r') as fo:
                    cdict = json.load(fo)

            if 'alembic' in cdict:
                self.itemDict['alembic'] = {}
                for k, vDict in cdict['alembic'].items():
                    category = vDict['category']
                    stage = vDict['stage']
                    # 头像
                    name = re.sub(r'[0-9]+', '', k)
                    taskDir = self.drive + '/' + self.project + '/assets/' + category + '/' + name
                    avatar = taskDir + '/avatar.jpg'
                    if not os.path.exists(avatar):
                        avatar = XBMLANGPATH + '/task.jpg'

                    # 颜色
                    if stage == 'hair':
                        v = [0, 150, 150]
                        s = 'hair'
                    elif stage == 'cloth':
                        v = [214, 128, 109]
                        s = 'cloth'
                    elif stage == 'cfx2':
                        v = [150, 75, 150]
                        s = 'cfx2'

                    # 控件
                    item = QtWidgets.QListWidgetItem(k)
                    item.setSizeHint(QtCore.QSize(72, 72 + 18))
                    item.setIcon(QtGui.QIcon(avatar))
                    item.setBackground(QtGui.QBrush(QtGui.QColor(v[0], v[1], v[2])))
                    item.setToolTip('\n'
                                    'Name: ' + k + '\n'
                                    'Time: ' + s + '\n')
                    if category == 'chr':
                        self.QlwSimCharacter.addItem(item)
                    elif category in ['prp', 'veh']:
                        self.QlwSimCloth.addItem(item)

                    # 字典
                    simAst = taskDir + '/cfx/publish/' + name + '_sim.mb'
                    simDir = self.cacheDir + '/' + category + '_' + k
                    self.itemDict['alembic'][k] = {
                        'simAst': simAst,
                        'simDir': simDir,
                        'stage': s,
                        'category': category
                    }

    def tabEditChangedUi(self, args):
        editVar = self.tabEdit.currentIndex()
        if editVar == 0:
            self.archiveVar(False)
        elif editVar == 1:
            self.QcbMerge.clear()
            viewVar = self.tabView.currentIndex()
            if viewVar == 0:
                if self.mayaRender[0] == 'Arnold':
                    self.QcbMerge.addItems(['MaterialX'])
                    self.QcbMerge.addItems(['Connect'])
                else:
                    self.QcbMerge.addItems(['Connect'])
            elif viewVar == 1:
                self.QcbMerge.addItems(['Reference'])
            elif viewVar == 2:
                self.QcbMerge.addItems(['Replace'])

    def tabEditQueryedUi(self, args):
        editVar = self.tabEdit.currentIndex()
        if editVar == 0:
            self.QlwArchive.clear()
            if not self.QlwTask.selectedItems():
                interface.scriptEditor(self.label, 'note', "选择任务后触发存档刷新")
            else:
                workDir = self.departmentDir + '/work'
                template = '_'.join([self.project, self.template, self.task, self.abbr, 'v*' + self.format[0]])
                files = cmds.getFileList(folder=workDir, filespec=template)
                if files:
                    files.sort(reverse=True)
                    for i in files:
                        item = QtWidgets.QListWidgetItem('work/' + i)
                        self.QlwArchive.addItem(item)
                        item.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 175)))
        elif editVar == 1:
            pass

    def tabEditArchive(self, mode):
        if mode == 'open':
            if not self.QlwArchive.selectedItems():
                interface.scriptEditor(self.label, 'warning', '选择工程文件对象后单击[打开]按钮')
            else:
                item = self.QlwArchive.currentItem().text()
                mfile = os.path.join(self.departmentDir, item)
                cmds.file(mfile, f=1, options="v=0;", ignoreVersion=1, o=1)
                interface.scriptEditor(self.label, 'command', '成功打开文件')
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
                        return

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
                    self.tabEditChangedUi(self)

    def tabEditAssembly(self):
        if 'tabLayout' in self.itemDict:
            tab = self.itemDict['tabLayout']
            if tab == 'ani':
                mode = self.QcbMerge.currentText()
                # alembic
                if 'alembic' in self.itemDict:
                    for k, vDict in self.itemDict['alembic'].items():
                        cmds.refresh()
                        # 导入[chr, prp] alembic缓存
                        abcfile = vDict['refFile']
                        if os.path.exists(abcfile):
                            srffile = vDict['srfFile']
                            astkind = srffile.split('/')[3]
                            astname = srffile.split('/')[4]
                            if not cmds.objExists(astkind + '_' + k + 'RN'):
                                cmds.file(abcfile,
                                          r=1,
                                          type="Alembic",
                                          ignoreVersion=1,
                                          gl=1,
                                          mergeNamespacesOnClash=False,
                                          namespace=astkind + '_' + k)
                                interface.scriptEditor(self.label, 'command', '导入 {} 的Alembic缓存'.format(k))
                            else:
                                cmds.file(abcfile, loadReference=astkind + '_' + k + 'RN', type="Alembic")
                                interface.scriptEditor(self.label, 'command', '替换 {} 的Alembic缓存'.format(k))
                            # 强制显示
                            nulls = ['srfNUL', 'defaultNUL', 'clothNUL', 'renderGeo_grp']
                            for i in nulls:
                                null = astkind + '_' + k + ':' + i
                                if cmds.objExists(null):
                                    cmds.setAttr(null + '.v', 1)

                            if mode == 'Connect':
                                # 引用材质球
                                shdfile = vDict['shdFile']
                                if os.path.exists(shdfile):
                                    if not cmds.objExists(astkind + '_' + astname + '_shdRN'):
                                        cmds.file(shdfile,
                                                  r=1,
                                                  type="mayaBinary",
                                                  ignoreVersion=1,
                                                  gl=1,
                                                  mergeNamespacesOnClash=False,
                                                  namespace=astkind + '_' + astname + '_shd',
                                                  options="v=0;")
                                        interface.scriptEditor(self.label, 'command', '导入 {} 的材质球文件'.format(astname))

                                    # 链接材质球
                                    sjsfile = vDict['sjsFile']
                                    if os.path.exists(sjsfile):
                                        with open(sjsfile, 'r') as fo:
                                            tdict = json.load(fo)
                                        ver = tdict.keys()
                                        ver.sort(reverse=True)
                                        materials = tdict[ver[0]]['lookdev']['materials']
                                        for s, gList in materials.items():
                                            mat = ':'.join([astkind + '_' + astname + '_shd', s])
                                            if cmds.nodeType(mat) not in ['displacementShader']:
                                                geo = [astkind + '_' + k + ':' + i for i in gList]
                                                cmds.select(geo)
                                                cmds.hyperShade(assign=mat)
                                        interface.scriptEditor(self.label, 'command', '链接 {} 的材质球'.format(k))
                            elif mode == 'MaterialX':
                                mtxfile = vDict['mtxFile']
                                if os.path.exists(mtxfile):
                                    # aiMerge
                                    aiMerge = 'aiMerge_' + self.project
                                    if not cmds.objExists(aiMerge):
                                        cmds.createNode('aiMerge', n=aiMerge)
                                        cmds.connectAttr(aiMerge + '.message', 'defaultArnoldRenderOptions.operator', f=1)
                                    # aiMaterialx
                                    aiMtlx = '_'.join(['aiMtlx', astkind, astname])
                                    if not cmds.objExists(aiMtlx):
                                        cmds.createNode('aiMaterialx', n=aiMtlx)
                                        v = len(cmds.defaultNavigation(dtv=1, d=aiMerge + '.inputs'))
                                        cmds.connectAttr(aiMtlx + '.out', aiMerge + '.inputs[' + str(v) + ']', f=1)
                                        cmds.setAttr(aiMtlx + '.selection', '*', type='string')
                                        cmds.setAttr(aiMtlx + '.filename', mtxfile, type='string')
                                        cmds.setAttr(aiMtlx + '.look', 'LookA', type='string')
                                        interface.scriptEditor(self.label, 'command', '创建 {} 的 aiMaterialx'.format(k))
                # camera
                if 'camera' in self.itemDict:
                    for k, vDict in self.itemDict['camera'].items():
                        camfile = vDict['refFile']
                        if os.path.exists(camfile):
                            if not cmds.objExists('lgtRN'):
                                cmds.file(camfile,
                                          r=1,
                                          type="FBX",
                                          ignoreVersion=1,
                                          gl=1,
                                          mergeNamespacesOnClash=False,
                                          namespace='lgt',
                                          options="v=0;")
                                interface.scriptEditor(self.label, 'command', '引用摄像机文件')
                            else:
                                cmds.file(camfile, loadReference='lgtRN', type="FBX")
                                interface.scriptEditor(self.label, 'command', '更新摄像机文件')
                            camera = 'lgt:' + k
                            if cmds.objExists(camera):
                                cmds.lookThru(camera)

                # scene
                if 'scene' in self.itemDict:
                    for k, vDict in self.itemDict['scene'].items():
                        reffile = vDict['refFile']
                        if os.path.exists(reffile):
                            sets = cmds.ls(['*_set_AR*', 'set_*:Group', '*:*_RD'])
                            if not sets:
                                if cmds.objExists('editsManager1'):
                                    cmds.delete('editsManager1')
                                cmds.file(reffile,
                                          i=1,
                                          type="mayaAscii",
                                          ignoreVersion=1,
                                          ra=True,
                                          mergeNamespacesOnClash=True,
                                          namespace=":",
                                          options="v=0;",
                                          pr=1,
                                          importFrameRate=True,
                                          importTimeRange="override")
                            interface.scriptEditor(self.label, 'command', '导入场景文件')
                    # 场景模式导入
                    if self.QrbSceneAR.isChecked():
                        # AR动画曲线链接
                        if 'connect' in self.itemDict:
                            interface.scriptEditor(self.label, 'command', 'AR动画曲线链接')
                            for k, v in self.itemDict['connect'].items():
                                if cmds.objExists(k) and cmds.objExists(v):
                                    if not cmds.connectionInfo(k, isSource=True):
                                        cmds.connectAttr(k, v, f=1)
                    elif self.QrbSceneRN.isChecked():
                        error = []
                        for k, vDict in self.itemDict['scene'].items():
                            if vDict['category'] == 'set':
                                ar = vDict['outliner'].split(':')[0].replace('NS', 'AR')
                                rn = 'set_' + ar.split('_')[0] + re.sub('\D', '', ar)
                                group = rn + ':Group'
                                main = rn + ':Main'
                                srffile = vDict['asmFile'].replace('asm', 'srf').replace('_set.mb', '_srf.mb')
                                if os.path.exists(srffile):
                                    #导入场景资产
                                    if not cmds.objExists(rn+'RN'):
                                        interface.scriptEditor(self.label, 'command', '导入RN场景资产')
                                        t = cmds.getAttr(ar + '.t')[0]
                                        r = cmds.getAttr(ar + '.r')[0]
                                        s = cmds.getAttr(ar + '.s')[0]
                                        if cmds.objExists(ar):
                                            cmds.delete(ar)
                                        cmds.file(srffile,
                                                  r=1,
                                                  type="mayaBinary",
                                                  ignoreVersion=1,
                                                  gl=1,
                                                  mergeNamespacesOnClash=False,
                                                  namespace=rn,
                                                  options="v=0;")
                                        if not cmds.objExists(main):
                                            cmds.setAttr(group + '.tx', t[0])
                                            cmds.setAttr(group + '.tx', t[1])
                                            cmds.setAttr(group + '.tx', t[2])
                                            cmds.setAttr(group + '.rx', r[0])
                                            cmds.setAttr(group + '.ry', r[1])
                                            cmds.setAttr(group + '.rz', r[2])
                                            cmds.setAttr(group + '.sx', s[0])
                                            cmds.setAttr(group + '.sy', s[1])
                                            cmds.setAttr(group + '.sz', s[2])
                                    #导入/更新场景动画
                                    animfile = self.itemDict['setting']['dirpath'] + '/' + self.project + '_' + rn + '_ani.anim'
                                    if os.path.exists(animfile):
                                        interface.scriptEditor(self.label, 'command', '导入/更新RN场景动画')
                                        cmds.select(group, r=1)
                                        cmds.file(animfile,
                                                  i=1,
                                                  type="animImport",
                                                  ignoreVersion=True,
                                                  ra=True,
                                                  mergeNamespacesOnClash=True,
                                                  namespace=":",
                                                  options="targetTime=4;copies=1;option=replace;pictures=0;connect=0;",
                                                  pr=True,
                                                  importTimeRange="combine")
                                else:
                                    error.append(srffile)
                        if error:
                            interface.scriptEditor(self.label, 'warning', '文件丢失 {}'.format('\n'.join(error)))
                            raise ValueError('srf: {}'.format('\n'.join(error)))
                interface.scriptEditor(self.label, 'command', '动画缓存数据导入/更新完成')
            elif tab == 'efx':
                if 'alembic' in self.itemDict:
                    for k, vDict in self.itemDict['alembic'].items():
                        abcfile = vDict['refFile']
                        if os.path.exists(abcfile):
                            if not cmds.objExists('efx_' + k + 'RN'):
                                cmds.file(abcfile,
                                          r=1,
                                          type="Alembic",
                                          ignoreVersion=1,
                                          gl=1,
                                          mergeNamespacesOnClash=False,
                                          namespace='efx_' + k)
                                interface.scriptEditor(self.label, 'command', '引用 {} 的Alembic缓存'.format(k))
                            else:
                                cmds.file(abcfile, loadReference='efx_' + k + 'RN', type="Alembic")
                                interface.scriptEditor(self.label, 'command', '替换 {} 的Alembic缓存'.format(k))
                            interface.scriptEditor(self.label, 'command', '特效缓存数据导入/更新完成')
            elif tab == 'sim':
                if 'alembic' in self.itemDict:
                    error = []
                    for k, vDict in self.itemDict['alembic'].items():
                        category = vDict['category']
                        srfRN = category + '_' + k +'RN'
                        if not cmds.objExists(srfRN):
                            error.append(k)

                    # 入口
                    if error:
                        interface.scriptEditor(self.label, 'warning', '请先完成Ani菜单下的数据组装后再次完成Sim数据更新')
                    else:
                        for k, vDict in self.itemDict['alembic'].items():
                            cmds.refresh()
                            stage = vDict['stage']
                            category = vDict['category']
                            # 挂在毛发
                            simDir = vDict['simDir']
                            if stage in ['hair', 'cfx2']:
                                # 归档
                                if not cmds.objExists('xGenNUL'):
                                    cmds.group(em=True, name='xGenNUL')

                                simAst = vDict['simAst']
                                if os.path.exists(simAst):
                                    # xgen引用资产
                                    if not cmds.objExists('sim_' + k + 'RN'):
                                        cmds.file(simAst,
                                                  r=1,
                                                  type="mayaBinary",
                                                  ignoreVersion=1,
                                                  gl=1,
                                                  mergeNamespacesOnClash=True,
                                                  namespace='sim_' + k,
                                                  options="v=0;")
                                        cmds.parent('sim_' + k + ':cfxNUL', 'xGenNUL')
                                        interface.scriptEditor(self.label, 'command', '导入 {} 的Xgen资产文件'.format(k))
                                    cmds.setAttr(category + '_' + k + ':noRenderNUL.v', 0)
                                    cmds.setAttr('sim_' + k + ':cfxNUL.v', 1)
                                    cmds.setAttr('sim_' + k + ':simNUL.v', 0)

                                    # DES添加缓存
                                    curves = cmds.getFileList(folder=simDir, filespec='*_OutputCurves.abc')
                                    palettes = cmds.listRelatives('sim_' + k + ':cfxNUL', ad=1, type=['xgmPalette'])
                                    if curves and palettes:
                                        for crvAbc in curves:
                                            description = 'sim_' + k + ':' + crvAbc.split('.')[0].replace('_OutputCurves', '_xgen_DES')
                                            if cmds.objExists(description):
                                                xg.setAttr('liveMode', '0', str(palettes[0]), str(description), 'SplinePrimitive')
                                                xg.setAttr('cacheFileName', str(simDir + '/' + crvAbc), str(palettes[0]), str(description), 'SplinePrimitive')

                                    # simNUL合并缓存
                                    if cmds.objExists('lgtRN'):
                                        cmds.refresh()
                                        # 替换 sim alembic
                                        simfile = simDir + '/' + self.project + '_' + category + '_' + k + '_sim.abc'
                                        if not os.path.exists(simfile):
                                            simfile = cmds.referenceQuery('lgtRN', filename=1).rsplit('/', 1)[0] + '/' + self.project + '_' + category + '_' + k + '_sim.abc'
                                        if not cmds.objExists('ani_' + k + 'RN'):
                                            cmds.file(simfile,
                                                      r=1,
                                                      type="Alembic",
                                                      ignoreVersion=1,
                                                      gl=1,
                                                      mergeNamespacesOnClash=False,
                                                      namespace='ani_' + k)
                                            bsnode = cmds.blendShape('ani_' + k + ':hairGrmNUL', 'sim_' + k + ':hairGrmNUL', origin='local', name='blendShape_sim_' + k)
                                            cmds.setAttr(bsnode[0] + '.hairGrmNUL', 1)
                                            cmds.parent('ani_' + k + ':simNUL', 'xGenNUL')
                                        else:
                                            cmds.file(simfile, loadReference='ani_' + k + 'RN', type="Alembic")
                                            interface.scriptEditor(self.label, 'command', '更新 {} 的Sim.Alembic缓存'.format(k))
                                        cmds.setAttr('sim_' + k + ':simNUL.v', 0)
                                        cmds.setAttr('ani_' + k + ':simNUL.v', 0)

                            # 挂在渲染模型/srfNUL
                            if stage in ['cloth', 'cfx2']:
                                abcs = cmds.getFileList(folder=simDir, filespec='*_ani.abc')
                                if abcs:
                                    cmds.refresh()
                                    abcfile = simDir + '/' + abcs[0]
                                    cmds.file(abcfile, loadReference=category + '_' + k + 'RN', type="Alembic")
                                    cmds.setAttr(category + '_' + k + ':clothNUL.v', 1)
                                    cmds.setAttr(category + '_' + k + ':noRenderNUL.v', 0)
                                    interface.scriptEditor(self.label, 'command', '更新 {} 的Cloth.Alembic缓存'.format(k))

            # 场景预设
            if 'setting' in self.itemDict:
                setting = self.itemDict['setting']
                if self.QcbResolution.isChecked():
                    interface.scriptEditor(self.label, 'command', "设置 ['渲染尺寸'] 参数")
                    resolution = setting['resolution']
                    cmds.setAttr('defaultResolution.width', resolution[0])
                    cmds.setAttr('defaultResolution.height', resolution[1])

                if self.QcbSpeed.isChecked():
                    interface.scriptEditor(self.label, 'command', "设置 ['播放速度'] 参数")
                    playbackSpeed = setting['playbackSpeed']
                    cmds.currentUnit(time=playbackSpeed)

                if self.QcbRange.isChecked():
                    interface.scriptEditor(self.label, 'command', "设置 ['起始结束帧'] 参数")
                    timeSlider = setting['timeSlider']
                    cmds.playbackOptions(e=1, minTime=timeSlider[0])
                    cmds.playbackOptions(e=1, maxTime=timeSlider[1])