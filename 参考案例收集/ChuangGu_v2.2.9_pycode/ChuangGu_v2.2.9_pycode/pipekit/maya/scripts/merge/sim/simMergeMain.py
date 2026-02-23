# -*- coding: utf-8 -*-

import os
import re
import json
from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
import maya.mel as mel

from core import config, interface, framework
from startup import removes
from merge.sim import simMergeWindow as UI
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

    def abcMenu(self):
        menu = QtWidgets.QMenu(self.parent)
        menu.addAction("选择头像/关闭当前 {毛发, 布料} 解算器").triggered.connect(partial(self.abcApply, 'sel', 'close'))
        menu.addAction("选择头像/打开当前 {毛发, 布料} 解算器").triggered.connect(partial(self.abcApply, 'sel', 'open'))
        menu.addSeparator()
        menu.addAction("所有头像/关闭所有 {毛发, 布料} 解算器").triggered.connect(partial(self.abcApply, 'all', 'close'))
        menu.addAction("所有头像/打开所有 {毛发, 布料} 解算器").triggered.connect(partial(self.abcApply, 'all', 'open'))
        menu.addSeparator()
        menu.addAction("所有头像/显示解算 {曲线, 布料} 的对象").triggered.connect(partial(self.abcApply, 'vis', 'all'))
        menu.popup(QtGui.QCursor.pos())

    def abcApply(self, mode, kind):
        if not self.msg['select']:
            self.SigScripts.emit(['error', '选择头像后右键完成命令操作.'])
        else:
            if mode == 'vis':
                reference = cmds.file(q=1, reference=1)
                if reference:
                    for i in reference:
                        rfn = cmds.referenceQuery(i, rfn=1)
                        if cmds.referenceQuery(rfn, isLoaded=1):
                            null = cmds.referenceQuery(rfn, nodes=1)[0]
                            nsid = null.split(':')[0]
                            if ':srfNUL' in null:
                                cmds.setAttr(nsid + ':srfNUL.v', 1)
                                cmds.setAttr(nsid + ':clothNUL.v', 0)
                                cmds.setAttr(nsid + ':noRenderNUL.v', 0)
                            elif ':cfxNUL' in null:
                                # srfNUL
                                cmds.setAttr(nsid + ':srfNUL.v', 1)
                                cmds.setAttr(nsid + ':clothNUL.v', 0)
                                cmds.setAttr(nsid + ':noRenderNUL.v', 0)
                                # simNUL
                                cmds.setAttr(nsid + ':simNUL.v', 1)
                                if cmds.filterExpand(nsid + ':noRenderNUL', ex=1, sm=12):
                                    cmds.setAttr(nsid + ':hairGrmNUL.v', 0)
                                else:
                                    cmds.setAttr(nsid + ':hairGrmNUL.v', 1)
                                cmds.setAttr(nsid + ':clothWpNUL.v', 1)
                                # fx2NUL
                                cmds.setAttr(nsid + ':fx2NUL.v', 1)
                                cmds.setAttr(nsid + ':hairNodeNUL.v', 1)
                                cmds.setAttr(nsid + ':hairCurveNUL.v', 1)
                                cmds.setAttr(nsid + ':clothMeshNUL.v', 0)
            else:
                nucleus = []
                if mode == 'sel':
                    for k, vDict in self.msg['select'].items():
                        fx2NUL = vDict['category'] + '_' + k + ':fx2NUL'
                        if cmds.objExists(fx2NUL):
                            nodes = cmds.listRelatives(fx2NUL, ad=1, type=['nucleus'])
                            if nodes:
                                nucleus.extend(nodes)
                elif mode == 'all':
                    nodes = cmds.ls(type=['nucleus'])
                    if nodes:
                        nucleus.extend(nodes)
                # 执行
                if nucleus:
                    if kind == 'close':
                        for i in nucleus:
                            cmds.setAttr(i + '.enable', 0)
                            cmds.setAttr(i + '.startFrame', 999)
                        if mode == 'sel':
                            self.SigScripts.emit(['command', '关闭当前 {毛发, 布料} 解算器.'])
                        else:
                            self.SigScripts.emit(['command', '关闭所有 {毛发, 布料} 解算器.'])
                    elif kind == 'open':
                        for i in nucleus:
                            cmds.setAttr(i + '.enable', 1)
                            cmds.setAttr(i + '.startFrame', 50)
                        if mode == 'sel':
                            self.SigScripts.emit(['command', '打开当前 {毛发, 布料} 解算器.'])
                        else:
                            self.SigScripts.emit(['command', '打开所有 {毛发, 布料} 解算器.'])

    def asmMenu(self):
        menu = QtWidgets.QMenu(self.parent)
        menu.addAction("选择图标AR切换到 Locator 模式").triggered.connect(partial(self.asmApply, 'Locator'))
        menu.addSeparator()
        menu.addAction("选择图标AR切换到 ModBbox 模式").triggered.connect(partial(self.asmApply, 'ModBbox'))
        menu.addAction("选择图标AR切换到 ModCache 模式").triggered.connect(partial(self.asmApply, 'ModCache'))
        menu.addSeparator()
        menu.addAction("选择图标AR切换到 RigFiles 模式").triggered.connect(partial(self.asmApply, 'RigFiles'))
        menu.addSeparator()
        menu.addAction("选择图标AR切换到 SrfProxy 模式").triggered.connect(partial(self.asmApply, 'SrfProxy'))
        menu.addAction("选择图标AR切换到 SrfFiles 模式").triggered.connect(partial(self.asmApply, 'SrfFiles'))
        menu.popup(QtGui.QCursor.pos())

    def asmApply(self, mode):
        if not self.msg['select']:
            self.SigScripts.emit(['error', '选择头像后右键完成命令操作.'])
        else:
            error0 = []
            error1 = []
            for k, vDict in self.msg['select'].items():
                obj = vDict['outliner']
                if not cmds.objExists(obj):
                    error0.append(k)
                    break
                else:
                    cmds.refresh()
                    category = vDict['category']
                    if category in ['set']:
                        childs = cmds.listRelatives(obj, children=1)
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
                self.SigScripts.emit(['error', 'RN对象 {} 不支持AssemblyReference功能,隶属于RN切换功能.'.format(error1)])
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
        self.item = None

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
                QLabel,QSpinBox,QDoubleSpinBox{
                    border-radius: 2px;
                }
                QLabel:disabled,QCheckBox:disabled,QDoubleSpinBox:disabled{
                    color: rgb(135, 135, 135);
                }
                QDoubleSpinBox::up-button,QDoubleSpinBox::down-button
                {
                    width: 0px;
                }
                QSpinBox::up-button,QSpinBox::down-button
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
            ''')
            # 右键菜单
            self.VchrM = MenuView(self.QlwAniCharacter)
            self.VchrM.SigScripts.connect(self.scriptsUi)
            self.QlwAniCharacter.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.QlwAniCharacter.customContextMenuRequested.connect(partial(self.viewMenuUi, 'chr'))

            self.VprpM = MenuView(self.QlwAniProp)
            self.VprpM.SigScripts.connect(self.scriptsUi)
            self.QlwAniProp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.QlwAniProp.customContextMenuRequested.connect(partial(self.viewMenuUi, 'prp'))

            self.VsetM = MenuView(self.QlwAniScene)
            self.VsetM.SigScripts.connect(self.scriptsUi)
            self.QlwAniScene.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.QlwAniScene.customContextMenuRequested.connect(partial(self.viewMenuUi, 'set'))

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

    def viewMenuUi(self, *args):
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
                    if args[0] in ['chr', 'prp', 'veh']:
                        keys = ['alembic']
                    elif args[0] in ['set']:
                        keys = ['camera', 'scene']

                    for i in items:
                        key = i.text()
                        for n in keys:
                            if self.itemDict[n]:
                                for k, vDict in self.itemDict[n].items():
                                    if key == k:
                                        editDict['select'][k] = vDict

                    if args[0] in ['chr']:
                        self.VchrM.SigParams.emit(editDict)
                        self.VchrM.abcMenu()
                    elif args[0] in ['prp', 'veh']:
                        self.VprpM.SigParams.emit(editDict)
                        self.VprpM.abcMenu()
                    elif args[0] in ['set']:
                        self.VsetM.SigParams.emit(editDict)
                        self.VsetM.asmMenu()
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
        plugins = ['fbxmaya.mll', 'AbcImport.mll', 'sceneAssembly.mll', 'gpuCache.mll']
        for plugin in plugins:
            try:
                if not cmds.pluginInfo(plugin, q=1, loaded=1):
                    cmds.loadPlugin(plugin)
            except:
                print('//Result: plug-ins {} skip.'.format(plugin))

        # 加载任务
        self.projectUi(self)

        if self.kind == 'shots':
            self.QcbBusiness.addItem('series')
            self.QcbBusiness.addItem('film')

        # 控件预设参数
        self.QlwAniCharacter.setIconSize(QtCore.QSize(68, 68))
        self.QlwAniProp.setIconSize(QtCore.QSize(68, 68))
        self.QlwAniScene.setIconSize(QtCore.QSize(128, 70))
        self.tabEditAssemblyUi()

        font = QtGui.QFont()
        font.setPointSize(10)
        listWidgets = [self.QlwAniCharacter, self.QlwAniProp, self.QlwAniScene]
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

        listWidgets = [self.QlwHairNode, self.QlwClothNode]
        for listWidget in listWidgets:
            listWidget.setStyleSheet('''
                QListWidget{
                    outline: 0px;
                    background-color: rgb(75,75,75);
                }
                QListWidget::item{
                    color: rgb(175,175,175);
                }
                QListWidget::item:hover{
                    background-color: rgb(75,75,75);
                    border-radius: 2px;
                    color: rgb(175, 100, 175)
                }
                QListWidget::item:selected{
                    color: rgb(200,200,75);
                    border: 1px solid rgb(200,200,75);
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
        # Tab
        self.tabView.currentChanged.connect(self.tabViewChangedUi)
        self.tabEdit.currentChanged.connect(self.tabEditChangedUi)
        # Tab.View.Ani
        self.QlwAniVersion.itemClicked.connect(self.tabViewSubsetsUi)
        self.QlwAniCharacter.itemClicked.connect(partial(self.avatarClickUi, 'chr'))
        self.QlwAniProp.itemClicked.connect(partial(self.avatarClickUi, 'prp'))
        # Tab.Archive
        self.QpbOpen.clicked.connect(partial(self.tabEditArchive, 'open'))
        self.QpbSave.clicked.connect(partial(self.tabEditArchive, 'save'))
        self.QpbWork.clicked.connect(partial(self.tabEditArchive, 'work'))
        self.QpbMerge.clicked.connect(self.tabEditAssembly)
        # Tab.Assembly
        self.QrbMergeReplace.clicked.connect(self.tabEditAssemblyUi)
        self.QrbMergeCombine.clicked.connect(self.tabEditAssemblyUi)
        self.QrbMergeAlembic.clicked.connect(self.tabEditAssemblyUi)
        self.QrbImportAll.clicked.connect(self.tabEditAssemblyUi)
        self.QrbImportSel.clicked.connect(self.tabEditAssemblyUi)
        # Tab.Ncache
        self.QlwHairNode.itemClicked.connect(partial(self.tabEditOutliner, 'hair'))
        self.QlwClothNode.itemClicked.connect(partial(self.tabEditOutliner, 'cloth'))
        self.QpbNcache.clicked.connect(self.tabEditNcache)

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
            for task in tasks:
                cmds.refresh()
                if task[0] == 'c' and task[1:5].isdigit():
                    item = QtWidgets.QListWidgetItem(task)
                    self.QlwTask.addItem(item)
                    v = 0
                    publishDir = self.categoryDir + '/' + task + '/ani/publish'
                    if os.path.exists(publishDir):
                        vers = cmds.getFileList(folder=publishDir, filespec='v*.')
                        if vers:
                            vers.sort(reverse=True)
                            abcs = cmds.getFileList(folder=publishDir + '/' + vers[0] + '/cache', filespec='*.abc')
                            if abcs:
                                v += 1
                                sims = cmds.getFileList(folder=publishDir + '/' + vers[0] + '/cache', filespec='*_sim.abc')
                                if sims:
                                    v += 1
                    if v == 1:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(35, 150, 200)))
                    elif v == 2:
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

    def avatarClickUi(self, *args):
        editVar = self.tabEdit.currentIndex()
        if editVar == 2:
            items = []
            self.nodesDict = {}
            self.QlwHairNode.clear()
            self.QlwClothNode.clear()
            if args[0] == 'chr':
                self.QlwAniProp.clearSelection()
                items.extend(self.QlwAniCharacter.selectedItems())
            elif args[0] in ['prp', 'veh']:
                self.QlwAniCharacter.clearSelection()
                items.extend(self.QlwAniProp.selectedItems())

            if items:
                nsid = None
                for k, vDict in self.itemDict['alembic'].items():
                    if items[0].text() == k:
                        category = vDict['category']
                        if cmds.objExists('persp.mode'):
                            if cmds.getAttr('persp.mode') == 'replace':
                                nsid = items[0].text()
                            else:
                                nsid = category + '_' + items[0].text()
                        else:
                            nsid = category + '_' + items[0].text()
                        break

                if nsid:
                    self.item = nsid
                    nulls = ['hairSystemNUL', 'clothNodeNUL']
                    for null in nulls:
                        if null == 'hairSystemNUL':
                            self.QlwHairNode.clear()
                            null = nsid + ':hairSystemNUL'
                            icon = XBMLANGPATH + '/hairSystem.png'
                            widget = self.QlwHairNode
                            kind = 'hairSystem'
                        elif null == 'clothNodeNUL':
                            self.QlwClothNode.clear()
                            # null = nsid + ':clothNodeNUL'
                            # icon = XBMLANGPATH + '/nCloth.png'
                            null = nsid + ':clothWpNUL'
                            icon = XBMLANGPATH + '/geometry.png'
                            widget = self.QlwClothNode
                            kind = 'nCloth'
                        if cmds.objExists(null):
                            child = cmds.listRelatives(null, c=1)
                            if child:
                                widget.setIconSize(QtCore.QSize(20, 20))
                                widget.setSpacing(3)
                                widget.setResizeMode(widget.Adjust)
                                for i in child:
                                    cmds.refresh()
                                    name = i.split(':')[-1]
                                    if cmds.nodeType(i) == 'nucleus':
                                        item = QtWidgets.QListWidgetItem(QtGui.QIcon(XBMLANGPATH + '/nucleus.png'), name)
                                        self.nodesDict[name] = 'nucleus'
                                    else:
                                        item = QtWidgets.QListWidgetItem(QtGui.QIcon(icon), name)
                                        self.nodesDict[name] = kind
                                    widget.addItem(item)
                            interface.scriptEditor(self.label, 'command', "场景内对应数据正常加载.")
                        else:
                            interface.scriptEditor(self.label, 'warning', "场景内未找到 {} 头像数据,请优先组装此头像.".format(nsid.split('_')[-1]))
                            break

    def tabViewChangedUi(self, args):
        self.viewVar = self.tabView.currentIndex()
        # 更新左侧界面
        if self.QlwTask.selectedItems():
            # tab.ani
            if self.viewVar == 0:
                self.publishDir = self.taskDir + '/ani/publish'
                self.QlwAniCharacter.clear()
                self.QlwAniProp.clear()
                self.QlwAniScene.clear()
                self.QlwAniVersion.clear()
            self.tabViewQueryedUi(args)

    def tabViewQueryedUi(self, args):
        # 添加版本
        vers = cmds.getFileList(folder=self.publishDir, filespec='v*.')
        if vers:
            vers.sort(reverse=True)
            for ver in vers:
                item = QtWidgets.QListWidgetItem(ver)
                self.QlwAniVersion.addItem(item)

                abcs = cmds.getFileList(folder=self.publishDir + '/' + ver + '/cache', filespec='*.abc')
                if abcs:
                    item.setForeground(QtGui.QBrush(QtGui.QColor(75, 150, 75)))
                else:
                    files = cmds.getFileList(folder=self.publishDir + '/' + ver, filespec='*.json')
                    if files:
                        item.setForeground(QtGui.QBrush(QtGui.QColor(150, 150, 75)))

            # 缓存使用版本及子集控件
            if self.taskDir in cmds.file(q=1, exn=1):
                if cmds.objExists('simRN'):
                    ver = cmds.referenceQuery('simRN', filename=1).rsplit('/')[-3]
                    item = self.QlwAniVersion.findItems(ver, QtCore.Qt.MatchRegExp)[0]
                    self.QlwAniVersion.setCurrentItem(item)
                    self.QlwAniVersion.scrollToItem(item)
                else:
                    if cmds.objExists('persp.history'):
                        ver = cmds.getAttr('persp.history')
                        item = self.QlwAniVersion.findItems(ver, QtCore.Qt.MatchRegExp)[0]
                        self.QlwAniVersion.setCurrentItem(item)
                        self.QlwAniVersion.scrollToItem(item)
                    else:
                        self.QlwAniVersion.setCurrentRow(0)
            else:
                self.QlwAniVersion.setCurrentRow(0)
            self.tabViewSubsetsUi(args)

    def tabViewSubsetsUi(self, args):
        self.itemDict = {}
        # Tab.Ani
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
                item.setToolTip('Task: ' + k + '\n'
                                'Kind: ' + category
                                )
                if category == 'chr':
                    self.QlwAniCharacter.addItem(item)
                elif category in ['prp', 'veh']:
                    self.QlwAniProp.addItem(item)
                # 定义字典
                aniabc = self.cacheDir + '/' + '_'.join([self.project, category, k, 'ani.abc'])
                simabc = self.cacheDir + '/' + '_'.join([self.project, category, k, 'sim.abc'])
                cfxfile = taskDir + '/cfx/publish/' + name + '_cfx.mb'
                # 颜色区分
                if not os.path.exists(aniabc):
                    v = [125, 125, 125]
                    s = None
                else:
                    if os.path.exists(simabc):
                        jfile = taskDir + '/cfx/publish/' + name + '_cfx.json'
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
                        v = [75, 135, 75]
                        s = 'anim'

                    self.itemDict['alembic'][k] = {
                        'cfxFile': cfxfile,
                        'refFile': aniabc,
                        'simFile': simabc,
                        'category': category,
                        'outliner': category + '_' + k + ':srfNUL',
                        'stage': s,
                        "namespace": vDict['namespace'],
                        "referenceNode": vDict['referenceNode']
                    }
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
                    v = [75, 135, 75]
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
                            v = [75, 135, 75]
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

    def tabEditChangedUi(self, args):
        editVar = self.tabEdit.currentIndex()
        if editVar == 2:
            interface.scriptEditor(self.label, 'note', "缓存菜单")
            self.QlwAniCharacter.clearSelection()
            self.QlwAniProp.clearSelection()
            self.QlwAniCharacter.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.QlwAniProp.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.QlwAniScene.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            self.QlwHairNode.clear()
            self.QlwClothNode.clear()
        else:
            self.QlwAniCharacter.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.QlwAniProp.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.QlwAniScene.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            if editVar == 0:
                self.archiveVar(False)
            elif editVar == 1:
                interface.scriptEditor(self.label, 'note', "组装菜单")
                if cmds.objExists('persp.mode'):
                    mode = cmds.getAttr('persp.mode')
                    if mode == 'replace':
                        self.QrbMergeReplace.setChecked(True)
                    elif mode == 'combine':
                        self.QrbMergeCombine.setChecked(True)
                    elif mode == 'alembic':
                        self.QrbMergeAlembic.setChecked(True)
            elif editVar == 3:
                interface.scriptEditor(self.label, 'note', "缓存菜单")
                self.QlwAniScene.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
                if 'setting' in self.itemDict:
                    cfx2Slider = self.itemDict['setting']['cfx2Slider']
                    timeSlider = self.itemDict['setting']['timeSlider']
                    self.QdsbStart.setValue(cfx2Slider[0])
                    self.QdsbEnd.setValue(timeSlider[1])
                    cmds.playbackOptions(e=1, minTime=cfx2Slider[0])
                    cmds.playbackOptions(e=1, maxTime=timeSlider[1])

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
        elif editVar == 2:
            pass

    def tabEditAssemblyUi(self):
        if self.QrbMergeReplace.isChecked() or self.QrbMergeCombine.isChecked():
            if self.QrbImportAll.isChecked():
                self.QcbCharacter.setChecked(True)
                self.QcbProp.setChecked(False)
                self.QcbScene.setChecked(False)
                self.QcbCamera.setChecked(False)
                self.QcbCharacter.setEnabled(True)
                self.QcbProp.setEnabled(True)
                self.QcbScene.setEnabled(False)
                self.QcbCamera.setEnabled(False)
            elif self.QrbImportSel.isChecked():
                self.QcbCharacter.setChecked(False)
                self.QcbProp.setChecked(False)
                self.QcbScene.setChecked(False)
                self.QcbCamera.setChecked(False)
                self.QcbCharacter.setEnabled(False)
                self.QcbProp.setEnabled(False)
                self.QcbScene.setEnabled(False)
                self.QcbCamera.setEnabled(False)
        elif self.QrbMergeAlembic.isChecked():
            if self.QrbImportAll.isChecked():
                self.QcbCharacter.setChecked(True)
                self.QcbProp.setChecked(False)
                self.QcbScene.setChecked(False)
                self.QcbCamera.setChecked(True)
                self.QcbCharacter.setEnabled(True)
                self.QcbProp.setEnabled(True)
                self.QcbScene.setEnabled(True)
                self.QcbCamera.setEnabled(True)
            elif self.QrbImportSel.isChecked():
                self.QcbCharacter.setChecked(False)
                self.QcbProp.setChecked(False)
                self.QcbScene.setChecked(False)
                self.QcbCamera.setChecked(False)
                self.QcbCharacter.setEnabled(False)
                self.QcbProp.setEnabled(False)
                self.QcbScene.setEnabled(False)
                self.QcbCamera.setEnabled(False)

    def tabEditArchive(self, mode):
        if mode == 'open':
            if not self.QlwArchive.selectedItems():
                interface.scriptEditor(self.label, 'warning', '选择工程文件对象后单击[打开文件]按钮')
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
        # 判断文件
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'warning', '请选择镜头任务对象')
            return

        if 'tabLayout' in self.itemDict:
            tab = self.itemDict['tabLayout']
            if tab == 'ani':
                # 对象入口
                objs = {
                    'alembic': {},
                    'camera': {},
                    'scene': {}
                }
                # 选择模式
                if self.QrbImportAll.isChecked():
                    for k, vDcit in self.itemDict.items():
                        # abc
                        if k == 'alembic':
                            for k1, v1 in self.itemDict['alembic'].items():
                                if self.QcbCharacter.isChecked() and v1['category'] in ['chr']:
                                    objs['alembic'][k1] = v1
                                elif self.QcbProp.isChecked() and v1['category'] in ['prp', 'veh']:
                                    objs['alembic'][k1] = v1
                        # cam
                        if self.QcbCamera.isChecked():
                            if k == 'camera':
                                objs['camera'] = vDcit
                        # set
                        if self.QcbScene.isChecked():
                            if k == 'scene':
                                objs['scene'] = vDcit
                elif self.QrbImportSel.isChecked():
                    # 摄像机和场景
                    for i in self.QlwAniScene.selectedItems():
                        k = i.text()
                        if k == 'camera':
                            objs['camera'] = self.itemDict['camera']
                        else:
                            objs['scene'] = self.itemDict['scene']
                            break
                    # 角色和道具
                    items = []
                    items.extend(self.QlwAniCharacter.selectedItems())
                    items.extend(self.QlwAniProp.selectedItems())
                    for i in items:
                        k = i.text()
                        for k1, v1 in self.itemDict['alembic'].items():
                            if k == k1:
                                objs['alembic'][k] = self.itemDict['alembic'][k]

                # 修复恶意场景参数
                for i in ['initialShadingGroup', 'initialParticleSE']:
                    v = cmds.lockNode(i, q=1, lu=True)
                    if v[0]:
                        cmds.lockNode(i, lu=False)

                # 组装模式
                if self.QrbMergeReplace.isChecked() or self.QrbMergeCombine.isChecked():
                    if cmds.objExists('persp.mode'):
                        mode = cmds.getAttr('persp.mode')
                        if mode == 'alembic':
                            interface.scriptEditor(self.label, 'error', "当前文件为缓存模式禁止使用['替换', '组合']模式,新建空场景后可以使用类型模式组装")
                            return
                        if self.QrbMergeReplace.isChecked() and mode == 'combine':
                            interface.scriptEditor(self.label, 'error', "当前文件为组合模式禁止使用['替换', '缓存']模式,新建空场景后可以使用类型模式组装")
                            return
                        if self.QrbMergeCombine.isChecked() and mode == 'replace':
                            interface.scriptEditor(self.label, 'error', "当前文件为替换模式禁止使用['组合', '缓存']模式,新建空场景后可以使用类型模式组装")
                            return

                    if not bool(objs['alembic']):
                        interface.scriptEditor(self.label, 'warning', '至少选择一个头像或改为所有模式后,再次单击[执行]')
                        return

                    cfile = cmds.getFileList(folder=self.cacheDir, filespec='classic.ma')
                    pfile = cmds.getFileList(folder=self.cacheDir, filespec='prompt.ma')
                    files = cfile + pfile
                    if not files:
                        interface.scriptEditor(self.label, 'error', "未找到 ['classic.ma', 'prompt.ma'] 其中一种文件,程序被迫中止")
                        return
                    else:
                        # 打开动画文件
                        exn = cmds.file(q=1, exn=1)
                        aniDir = self.cacheDir.rsplit('/', 2)[0]
                        simDir = aniDir.replace('ani', 'sim') + '/work'
                        if aniDir in exn or simDir in exn:
                            interface.scriptEditor(self.label, 'note', '动画偏移后的文件已经打开')
                        else:
                            # 新建空场景
                            cmds.file(f=1, new=1)
                            cmds.file(self.cacheDir + '/' + files[0], f=1, options="v=0;", ignoreVersion=1, loadReferenceDepth="none", typ="mayaAscii", o=1)
                            # 相机命名
                            if not cmds.namespace(exists='sim'):
                                cam = cmds.ls('*_s*_c*_ani')
                                if cam:
                                    cmds.namespace(add='sim')
                                    cmds.rename(cam[0], 'sim:' + cam[0])

                        # 限定模式
                        ver = self.QlwAniVersion.currentItem().text()
                        if not cmds.objExists('persp.history'):
                            cmds.addAttr('persp', ln='history', dt='string')
                            cmds.setAttr('persp' + '.history', ver, type='string')
                        else:
                            old = cmds.getAttr('persp.history')
                            if ver != old:
                                interface.scriptEditor(self.label, 'warning', "['替换', '组合']组装模式不允许切换版本,新建空场景后选择其他版本再次组装")
                                return
                        # 添加模式属性
                        if not cmds.objExists('persp.mode'):
                            cmds.addAttr('persp', ln='mode', dt='string')

                    if self.QrbMergeReplace.isChecked():
                        cmds.setAttr('persp.mode', 'replace', type='string')
                        # alembic
                        if objs['alembic']:
                            for k, vDict in objs['alembic'].items():
                                cmds.refresh()
                                stage = vDict['stage']
                                solfile = vDict['cfxFile'].replace('_cfx.mb', '_rigsol.mb')
                                if stage in ['hair', 'cloth', 'cfx2']:
                                    if not os.path.exists(solfile):
                                        interface.scriptEditor(self.label, 'error', '{} 的rigsol.mb文件丢失,组装被迫中止'.format(k))
                                    else:
                                        # 加载装配文件
                                        rigRN = vDict['referenceNode']
                                        rigNS = vDict['namespace']
                                        if not cmds.referenceQuery(rigRN, isLoaded=1):
                                            cmds.file(solfile, loadReferenceDepth='asPrefs', loadReference=rigRN, type="mayaBinary", options="v=0;")
                                            if self.QcbBlendshape.isChecked():
                                                if cmds.filterExpand(rigNS + ':clothNUL', ex=1, sm=12):
                                                    bsnode = cmds.blendShape(rigNS + ':clothMeshNUL', rigNS + ':clothNUL', origin='local', name='blendShape_' + rigNS + '_clothMeshNUL')
                                                    cmds.setAttr(bsnode[0] + '.clothMeshNUL', 1)
                                        '''
                                        # 初次显示设置
                                        cmds.setAttr(rigNS + ':Geometry.v', 1)
                                        cmds.setAttr(rigNS + ':noRenderNUL.v', 0)
                                        cmds.setAttr(rigNS + ':clothWpNUL.v', 1)
                                        cmds.setAttr(rigNS + ':srfNUL.v', 1)
                                        hairGrmNUL = cmds.ls(rigNS + ':hairGrmNUL*')
                                        if hairGrmNUL:
                                            if cmds.filterExpand(rigNS + ':noRenderNUL', ex=1, sm=12):
                                                for i in hairGrmNUL:
                                                    cmds.setAttr(i + '.v', 0)
                                            else:
                                                for i in hairGrmNUL:
                                                    cmds.setAttr(i + '.v', 1)
                                        cmds.setAttr(rigNS + ':clothWpNUL.v', 1)
                                        cmds.setAttr(rigNS + ':fx2NUL.v', 1)
                                        cmds.setAttr(rigNS + ':hairNodeNUL.v', 1)
                                        cmds.setAttr(rigNS + ':hairCurveNUL.v', 1)
                                        cmds.setAttr(rigNS + ':clothMeshNUL.v', 0)
                                        '''
                                else:
                                    # 加载装配文件
                                    if not cmds.referenceQuery(k + 'RN', isLoaded=1):
                                        cmds.file(loadReferenceDepth='asPrefs', loadReference=k + "RN")
                    elif self.QrbMergeCombine.isChecked():
                        cmds.setAttr('persp' + '.mode', 'combine', type='string')
                        # alembic
                        if objs['alembic']:
                            for k, vDict in objs['alembic'].items():
                                cmds.refresh()
                                stage = vDict['stage']
                                cfxfile = vDict['cfxFile']
                                nsid = vDict['category'] + '_' + k
                                if stage in ['hair', 'cloth', 'cfx2'] and os.path.exists(cfxfile):
                                    # 加载装配文件
                                    rigRN = vDict['referenceNode']
                                    rigNS = vDict['namespace']
                                    if not cmds.referenceQuery(rigRN, isLoaded=1):
                                        cmds.file(loadReferenceDepth='asPrefs', loadReference=rigRN)
                                    cmds.setAttr(rigNS + ':Geometry.v', 0)

                                    # reference cfx file
                                    if not cmds.objExists(nsid + 'RN'):
                                        cmds.file(cfxfile,
                                                  r=1,
                                                  type="mayaBinary",
                                                  ignoreVersion=1,
                                                  gl=1,
                                                  mergeNamespacesOnClash=False,
                                                  namespace=nsid,
                                                  options="v=0;")
                                        if self.QcbBlendshape.isChecked():
                                            nulls = ['srfNUL', 'simNUL']
                                            for null in nulls:
                                                cfxNul = nsid + ':' + null
                                                rigNul = rigNS + ':' + null
                                                if cmds.objExists(cfxNul) and cmds.objExists(rigNul):
                                                    if cmds.filterExpand(cfxNul, ex=1, sm=12):
                                                        bsnode = cmds.blendShape(rigNul, cfxNul, origin='local', name='blendShape_' + nsid + '_' + null)
                                                        cmds.setAttr(bsnode[0] + '.' + null, 1)
                                            if cmds.filterExpand(nsid + ':clothNUL', ex=1, sm=12):
                                                bsnode = cmds.blendShape(nsid + ':clothMeshNUL', nsid + ':clothNUL', origin='local', name='blendShape_' + nsid + '_clothMeshNUL')
                                                cmds.setAttr(bsnode[0] + '.clothMeshNUL', 1)
                                        interface.scriptEditor(self.label, 'command', '引用 {} 的cfx组装文件'.format(k))

                                    # 初次显示设置
                                    # cfxNUL
                                    cmds.setAttr(nsid + ':cfxNUL.v', 1)
                                    # srfNUL
                                    cmds.setAttr(nsid + ':srfNUL.v', 1)
                                    cmds.setAttr(nsid + ':clothNUL.v', 0)
                                    cmds.setAttr(nsid + ':noRenderNUL.v', 0)
                                    # simNUL
                                    cmds.setAttr(nsid + ':simNUL.v', 1)
                                    if cmds.filterExpand(nsid + ':noRenderNUL', ex=1, sm=12):
                                        cmds.setAttr(nsid + ':hairGrmNUL.v', 0)
                                    else:
                                        cmds.setAttr(nsid + ':hairGrmNUL.v', 1)
                                    cmds.setAttr(nsid + ':clothWpNUL.v', 1)
                                    # fx2NUL
                                    cmds.setAttr(nsid + ':fx2NUL.v', 1)
                                    cmds.setAttr(nsid + ':hairNodeNUL.v', 1)
                                    cmds.setAttr(nsid + ':hairCurveNUL.v', 1)
                                    cmds.setAttr(nsid + ':clothMeshNUL.v', 0)
                                else:
                                    # 加载装配文件
                                    if not cmds.referenceQuery(k + 'RN', isLoaded=1):
                                        cmds.file(loadReferenceDepth='asPrefs', loadReference=k + "RN")
                        # setting
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
                                cfx2Slider = setting['cfx2Slider']
                                timeSlider = setting['timeSlider']
                                cmds.playbackOptions(e=1, minTime=cfx2Slider[0])
                                cmds.playbackOptions(e=1, maxTime=timeSlider[1])
                        interface.scriptEditor(self.label, 'command', '动画索引数据导入/更新完成')
                elif self.QrbMergeAlembic.isChecked():
                    # 禁止模式
                    cam = cmds.ls('sim:*_s*_c*_ani')
                    if cam:
                        if not cmds.referenceQuery(cam[0], isNodeReferenced=1):
                            interface.scriptEditor(self.label, 'error', '当前文件为替换或组合模式禁止使用缓存模式,新建空场景后可以使用缓存模式组装')
                            return

                    run = 0
                    # alembic
                    if objs['alembic']:
                        # 添加模式属性
                        if not cmds.objExists('persp.mode'):
                            cmds.setAttr('persp' + '.mode', 'alembic', type='string')

                        run += 1
                        for k, vDict in objs['alembic'].items():
                            cmds.refresh()
                            stage = vDict['stage']
                            cfxfile = vDict['cfxFile']
                            simfile = vDict['simFile']
                            nsid = vDict['category'] + '_' + k
                            if stage in ['hair', 'cloth', 'cfx2'] and os.path.exists(cfxfile) and os.path.exists(simfile):
                                # reference cfx file
                                if not cmds.objExists(nsid + 'RN'):
                                    cmds.file(cfxfile,
                                              r=1,
                                              type="mayaBinary",
                                              ignoreVersion=1,
                                              gl=1,
                                              mergeNamespacesOnClash=False,
                                              namespace=nsid,
                                              options="v=0;")
                                    if self.QcbBlendshape.isChecked():
                                        if cmds.objExists(nsid + ':clothMeshNUL') and cmds.objExists(nsid + ':clothNUL'):
                                            if cmds.filterExpand(nsid + ':clothNUL', ex=1, sm=12):
                                                bsnode = cmds.blendShape(nsid + ':clothMeshNUL', nsid + ':clothNUL', origin='local', name='blendShape_' + nsid)
                                                cmds.setAttr(bsnode[0] + '.clothMeshNUL', 1)
                                    interface.scriptEditor(self.label, 'command', '导入 {} 的Alembic缓存'.format(k))
                                else:
                                    cmds.setAttr(nsid + ':cfxNUL.v', 1)

                                # merge srf/sim alembic
                                if stage in ['hair']:
                                    attrs = ['sim']
                                else:
                                    attrs = ['ani', 'sim']

                                for i in attrs:
                                    if i == 'sim':
                                        abcfile = vDict['simFile']
                                        cnnnull = nsid + ":simNUL"
                                    else:
                                        abcfile = vDict['refFile']
                                        cnnnull = nsid + ":srfNUL"

                                    if os.path.exists(abcfile):
                                        abcnode = abcfile.split('/')[-1].replace('.abc', '_AlembicNode')
                                        if not cmds.objExists(abcnode):
                                            cmds.AbcImport(abcfile, mode='import', fitTimeRange=1, connect=cnnnull)
                                            interface.scriptEditor(self.label, 'command', '导入 {0} 的{1}.Alembic缓存'.format(k, i))
                                        else:
                                            abcpath = cmds.getAttr(abcnode + '.abc_File')
                                            if abcpath != abcfile:
                                                cmds.delete(abcnode)
                                                cmds.AbcImport(abcfile, mode='import', fitTimeRange=1, connect=cnnnull)
                                                interface.scriptEditor(self.label, 'command', '更新 {0} 的{1}.Alembic缓存'.format(k, i))
                                # 初次显示设置
                                # srfNUL
                                cmds.setAttr(nsid + ':srfNUL.v', 1)
                                cmds.setAttr(nsid + ':clothNUL.v', 0)
                                cmds.setAttr(nsid + ':noRenderNUL.v', 0)
                                # simNUL
                                cmds.setAttr(nsid + ':simNUL.v', 1)
                                if cmds.filterExpand(nsid + ':noRenderNUL', ex=1, sm=12):
                                    cmds.setAttr(nsid + ':hairGrmNUL.v', 0)
                                else:
                                    cmds.setAttr(nsid + ':hairGrmNUL.v', 1)
                                cmds.setAttr(nsid + ':clothWpNUL.v', 1)
                                # fx2NUL
                                cmds.setAttr(nsid + ':fx2NUL.v', 1)
                                cmds.setAttr(nsid + ':hairNodeNUL.v', 1)
                                cmds.setAttr(nsid + ':hairCurveNUL.v', 1)
                                cmds.setAttr(nsid + ':clothMeshNUL.v', 0)
                            else:
                                # reference ani file
                                anifile = vDict['refFile']
                                if not cmds.objExists(nsid + 'RN'):
                                    cmds.file(anifile,
                                              r=1,
                                              type="Alembic",
                                              ignoreVersion=1,
                                              gl=1,
                                              mergeNamespacesOnClash=False,
                                              namespace=nsid)
                                    interface.scriptEditor(self.label, 'command', '导入 {} 的Alembic缓存'.format(k))
                                else:
                                    cmds.setAttr(nsid + ':srfNUL.v', 1)
                                    cmds.file(anifile, loadReference=nsid + 'RN', type="Alembic")
                                    interface.scriptEditor(self.label, 'command', '更新 {} 的Alembic缓存'.format(k))

                    # camera
                    if objs['camera']:
                        run += 1
                        for k, vDict in self.itemDict['camera'].items():
                            camfile = vDict['refFile']
                            if os.path.exists(camfile):
                                if not cmds.objExists('simRN'):
                                    cmds.file(camfile,
                                              r=1,
                                              type="FBX",
                                              ignoreVersion=1,
                                              gl=1,
                                              mergeNamespacesOnClash=False,
                                              namespace='sim',
                                              options="v=0;")
                                    interface.scriptEditor(self.label, 'command', '引用摄像机文件')
                                else:
                                    cmds.file(camfile, loadReference='simRN', type="FBX")
                                    interface.scriptEditor(self.label, 'command', '更新摄像机文件')
                                camera = 'sim:' + k
                                if cmds.objExists(camera):
                                    cmds.lookThru(camera)

                    # scene
                    if objs['scene']:
                        run += 1
                        for k, vDict in self.itemDict['scene'].items():
                            reffile = vDict['refFile']
                            if os.path.exists(reffile):
                                sets = cmds.ls(['*_set_AR*', '*:*_RD'])
                                if not sets:
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
                        # AR动画曲线链接
                        if 'connect' in self.itemDict:
                            for k, v in self.itemDict['connect'].items():
                                if cmds.objExists(k) and cmds.objExists(v):
                                    if not cmds.connectionInfo(k, isSource=True):
                                        cmds.connectAttr(k, v, f=1)

                    # setting
                    if run > 0:
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
                                cfx2Slider = setting['cfx2Slider']
                                timeSlider = setting['timeSlider']
                                cmds.playbackOptions(e=1, minTime=cfx2Slider[0])
                                cmds.playbackOptions(e=1, maxTime=timeSlider[1])
                        interface.scriptEditor(self.label, 'command', '动画缓存数据导入/更新完成')
                    else:
                        interface.scriptEditor(self.label, 'warning', '至少选择一个头像或改为所有模式后,再次单击[执行]')

    def tabEditOutliner(self, *args):
        if self.item:
            items = []
            if args[0] == 'hair':
                self.QlwClothNode.clearSelection()
                items.extend(self.QlwHairNode.selectedItems())
            elif args[0] == 'cloth':
                self.QlwHairNode.clearSelection()
                items.extend(self.QlwClothNode.selectedItems())

            if items:
                objs = []
                for i in items:
                    obj = self.item + ':' + i.text()
                    if cmds.objExists(obj):
                        objs.append(obj)
                if objs:
                    cmds.select(objs, r=1)
                    interface.scriptEditor(self.label, 'command', '选择到大纲对象')

    def tabEditNcache(self):
        # 判断文件
        if not self.QlwTask.selectedItems():
            interface.scriptEditor(self.label, 'warning', '请选择镜头任务对象')
            return
        if not self.QlwArchive.selectedItems():
            interface.scriptEditor(self.label, 'warning', '请切换存档菜单选择对象后单击[打开文件]按钮')
            return
        if '/work/' not in cmds.file(q=1, exn=1):
            interface.scriptEditor(self.label, 'warning', '请单击存档菜单下的[工程新版]按钮')
            return

        if not self.item:
            interface.scriptEditor(self.label, 'warning', '请选择镜头下的头像对象')
        else:
            # 对象入口
            items = []
            items.extend(self.QlwHairNode.selectedItems())
            items.extend(self.QlwClothNode.selectedItems())
            if not items:
                interface.scriptEditor(self.label, 'warning', "单选或多选 ['hairSystem', 'nCloth']节点后再次单击执行按钮")
            else:
                hairSystem = []
                nCloth = []
                for i in items:
                    text = i.text()
                    if text in self.nodesDict.keys():
                        kind = self.nodesDict[text]
                        task = self.item + ':' + text
                        if kind == 'hairSystem':
                            hairSystem.append(task)
                        elif kind == 'nCloth':
                            nCloth.append(task)

                alls = hairSystem + nCloth
                if alls:
                    # 界面参数
                    start = str(self.QdsbStart.value())
                    end = str(self.QdsbEnd.value())
                    evaluateEvery = str(self.QdspEvaluateEvery.value())
                    saveEvery = str(self.QsbSaveEvery.value())
                    ver = self.QlwArchive.currentItem().text().split('_')[-1].split('.')[0]

                    # 优化输出
                    for k, vDict in self.itemDict['alembic'].items():
                        item = vDict['category'] + '_' + k
                        if cmds.objExists(item + 'RN'):
                            rootNUL = cmds.referenceQuery(item + 'RN', nodes=1)[0]
                            if self.item == item:
                                cmds.setAttr(rootNUL + '.v', 1)
                            else:
                                cmds.setAttr(rootNUL + '.v', 0)

                            fx2NUL = vDict['category'] + '_' + k + ':fx2NUL'
                            if cmds.objExists(fx2NUL):
                                nucleus = cmds.listRelatives(fx2NUL, ad=1, type=['nucleus'])
                                if nucleus:
                                    if self.item == item:
                                        for i in nucleus:
                                            cmds.setAttr(i + '.enable', 1)
                                            cmds.setAttr(i + '.startFrame', 50)
                                    else:
                                        for i in nucleus:
                                            cmds.setAttr(i + '.enable', 0)
                                            cmds.setAttr(i + '.startFrame', 999)

                    # 毛发缓存
                    if hairSystem:
                        interface.scriptEditor(self.label, 'command', '{0} 的{1}.nCache缓存正在输出'.format(self.item, 'hairSystem'))
                        cmds.refresh()
                        cacheDir = self.departmentDir + '/cache/' + ver + '/hairSystem/' + self.item
                        for i in hairSystem:
                            cache = i.replace(':', '_') + 'ShapeCache1'
                            if cmds.objExists(cache):
                                cmds.delete(cache)
                            shape = i.replace(':', '_') + 'Shape'
                            files = cmds.getFileList(folder=cacheDir, filespec=shape+'.*')
                            if files:
                                for f in files:
                                    cmds.sysFile(cacheDir + '/' + f, delete=True)

                        if not os.path.exists(cacheDir):
                            cmds.sysFile(cacheDir, makeDir=True)
                        cmds.select(hairSystem, r=1)
                        mel.eval('doCreateNclothCache 5 { "3", "' + start + '", "' + end +
                                 '", "OneFile", "1", "' +
                                 cacheDir + '","1","","0", "add", "0", "' +
                                 evaluateEvery + '", "' + saveEvery + '","0","1","mcc" } ;')

                    # 布料缓存
                    if nCloth:
                        interface.scriptEditor(self.label, 'command', '{0} 的{1}.nCache缓存正在输出'.format(self.item, 'nCloth'))
                        cmds.refresh()
                        cacheDir = self.departmentDir + '/cache/' + ver + '/nCloth/' + self.item
                        for i in nCloth:
                            node = cmds.listConnections(i + 'Shape.worldMesh', d=1)
                            cache = node[0].replace(':', '_') + 'ShapeCache1'
                            if cmds.objExists(cache):
                                cmds.delete(cache)
                            shape = node[0].replace(':', '_') + 'Shape'
                            files = cmds.getFileList(folder=cacheDir, filespec=shape + '.*')
                            if files:
                                for f in files:
                                    cmds.sysFile(cacheDir + '/' + f, delete=True)

                        if not os.path.exists(cacheDir):
                            cmds.sysFile(cacheDir, makeDir=True)
                        cmds.select(nCloth, r=1)
                        mel.eval('doCreateNclothCache 5 { "3", "' + start + '", "' + end +
                                 '", "OneFile", "1", "' +
                                 cacheDir + '","1","","0", "add", "0", "' +
                                 evaluateEvery + '", "' + saveEvery + '","0","1","mcc" } ;')

                    # 全部显示
                    for k, vDict in self.itemDict['alembic'].items():
                        rn = vDict['category'] + '_' + k + 'RN'
                        if cmds.objExists(rn):
                            rootNUL = cmds.referenceQuery(rn, nodes=1)[0]
                            cmds.setAttr(rootNUL + '.v', 1)

                    # 保存文件
                    cmds.file(f=1, save=1)
                    interface.scriptEditor(self.label, 'result', 'nCache缓存输出完成')