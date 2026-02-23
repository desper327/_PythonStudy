# -*- coding: utf-8 -*-

import sys
import os
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

from shiboken2 import wrapInstance
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui
import wsControl
from wsControl import toolkitWindow as UI
import logging
from core import interface

LOG = logging.getLogger("// Result")
long_type = int if sys.version_info[0] >= 3 else long


class ChunToolkit(QtWidgets.QMainWindow, UI.Ui_MainWindow):
    def __init__(self):
        super(ChunToolkit, self).__init__()
        self.setupUi(self)
        self.setStyleSheet('''
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
                border-radius: 2px;
                color: rgb(35, 35, 35)
            }
            QListWidget::item:hover{
                padding-top: 2px;
                background-color: rgb(75,60,75);
                border-radius: 5px;
                color: rgb(150, 100, 150)
            }
            QListWidget::item:selected{
                border: 2px solid rgb(75,50,75);
                border-radius: 5px;
            }
            QListWidget::item:selected:!active{
                padding: 1px;
                border: 1px solid rgb(50,50,50);
                border-radius: 5px;
            }
            QTextEdit{
                background-color: rgb(75,75,75);
                border-radius: 5px;
            }
        ''')

        # 服务日期
        if interface.license():
            self.pageUi()
            self.toolsUi(self)
            self.toolBox.currentChanged.connect(self.toolsUi)
        else:
            page = QtWidgets.QWidget()
            page.setStyleSheet("border-radius: 10px")
            self.toolBox.addItem(page, 'license'.upper())
            layout = QtWidgets.QVBoxLayout(page)
            layout.setSpacing(5)
            layout.setContentsMargins(5, 5, 5, 5)
            font = QtGui.QFont()
            font.setPointSize(11)
            edit = QtWidgets.QTextEdit()
            edit.setFont(font)
            edit.setText('''
            这个世界里有什么是不会过期的？
            你我曾经一起在项目的点点滴滴！
            ''')
            layout.addWidget(edit)

    def pageUi(self):
        self.path = os.path.dirname(__file__)
        # 按__init__.py自定义排序生成部门工具集
        self.tools = self.relative(self.path, mode=True)
        if self.tools:
            for ctuple in self.tools:
                module = ctuple[1].split('.')[-1]
                suffix = ctuple[2]
                widget = QtWidgets.QWidget()
                widget.setStyleSheet("border-radius: 10px")
                layout = QtWidgets.QVBoxLayout(widget)
                layout.setSpacing(5)
                layout.setContentsMargins(5, 5, 5, 5)
                self.toolBox.addItem(widget, module.upper() + ' ' + suffix)

    def toolsUi(self, args):
        si = self.toolBox.currentIndex()
        department = self.tools[si][1].split('.')[-1]
        widget = self.toolBox.currentWidget()
        path = self.path + '/' + department

        # 加载部门/子集文件夹下
        childDirs = self.relative(path, mode=True)
        if childDirs:
            layout = widget.children()[0]
            for i in reversed(range(layout.count())):
                # print(layout.itemAt(i).widget())
                layout.itemAt(i).widget().close()
                layout.takeAt(i)

            font = QtGui.QFont()
            font.setPointSize(9)
            for ctuple in childDirs:
                module = ctuple[1].split('.')[-1]
                label = QtWidgets.QLabel(widget)
                layout.addWidget(label)
                label.setText(module.upper())
                listWidget = QtWidgets.QListWidget(widget)
                listWidget.setViewMode(QtWidgets.QListView.IconMode)
                listWidget.setSpacing(3)
                listWidget.setResizeMode(listWidget.Adjust)
                listWidget.setDragEnabled(False)
                listWidget.setFont(font)
                layout.addWidget(listWidget)

                # 加载部门/子集文件夹下的工具
                # 样式
                s = 48
                p = 4
                tools = self.relative(path + '/' + module, mode=False)
                # 信号槽
                listWidget.itemClicked.connect(partial(self.running, listWidget, tools))
                listWidget.setIconSize(QtCore.QSize(s, s))
                if tools:
                    icons = self.path.rsplit('\\', 2)[0] + '/icons'
                    for tool in tools:
                        name = tool[1].split('.')[-1]
                        item = QtWidgets.QListWidgetItem(QtGui.QIcon(icons+'/'+tool[3]), name)
                        item.setSizeHint(QtCore.QSize(s+p, (s+p)+18))
                        item.setBackground(QtGui.QBrush(QtGui.QColor(100, 100, 100)))
                        listWidget.addItem(item)
                        item.setToolTip('\n'
                                        'Scripts: ' + tool[1] + '\n'
                                        'ToolTip: ' + tool[4] +
                                        '\n'
                                        )

    def relative(self, path, mode=True):
        '''
        :param path: os.path.dirname(__file__)
        :param mode: {True: ['dir'], False: ['py', 'pyd']}
        :return: ('relative', 'package', 'suffix', 'icon', 'tooltip', 'pyfile')
        '''
        data = []
        dirs = os.listdir(path)
        if mode == True:
            for dir in dirs:
                if os.path.isdir(os.path.join(path, dir)):
                    init = os.path.join(path, dir, '__init__.py')
                    if os.path.exists(init):
                        data.append(dir)
        else:
            if '__init__.py' in dirs:
                for dir in dirs:
                    if os.path.isfile(os.path.join(path, dir)):
                        if '__init__' in dir:
                            pass
                        else:
                            if dir.endswith('.py') or dir.endswith('.pyd'):
                                data.append(dir)

        # 根据RELATIVE属性排序
        if not data:
            return data
        else:
            relative, unrelative = [], []
            for i in range(len(data)):
                modules = data[i].split('.')[0]
                package = path.split('\\')[-1].replace('/', '.') + '.' + modules
                pyfile = __import__(package, fromlist=[modules])
                reload(pyfile)

                # 获取 SUFFIX 字段属性
                if hasattr(pyfile, 'SUFFIX'):
                    if pyfile.SUFFIX == None:
                        suffix = ''
                    else:
                        suffix = pyfile.SUFFIX
                else:
                    suffix = '__SUFFIX'

                # 获取 ICON 字段属性
                if hasattr(pyfile, 'ICON'):
                    if pyfile.ICON == None:
                        icon = 'tool.png'
                    else:
                        icon = pyfile.ICON
                else:
                    icon = 'tool.png'

                # 获取 TOOLTIP 字段属性
                if hasattr(pyfile, 'TOOLTIP'):
                    if pyfile.TOOLTIP == None:
                        tooltip = '_TOOLTIP'
                    else:
                        tooltip = pyfile.TOOLTIP
                else:
                    tooltip = '__TOOLTIP'


                # 获取 RELATIVE 顺序属性
                if hasattr(pyfile, 'RELATIVE'):
                    if pyfile.RELATIVE == None:
                        relative.append((i, package, suffix, icon, tooltip, pyfile))
                    else:
                        relative.append((pyfile.RELATIVE, package, suffix, icon, tooltip, pyfile))
                else:
                    unrelative.append((i, package, suffix, icon, tooltip, pyfile))
            relative.sort(reverse=False)
            data = relative + unrelative
            return data

    def running(self, *msg):
        '''
        :param msg[0]: QListWidget
        :param msg[1]: ('relative', 'module', 'suffix', 'icon', 'tooltip', 'pyfile')
        :param msg[2]: QListWidgetItem
        '''
        index = msg[0].currentRow()
        param = msg[1]
        for p in param:
            if index == p[0]:
                module = p[1]
                pyfile = p[5]

        # 执行判断
        if hasattr(pyfile, 'main'):
            try:
                eval(module + '.main()')
                # LOG.info(module)
            except:
                cmds.warning('<' + module + u'.main( )> 方法运行存在异常')
        else:
            cmds.warning(u'请添加 <' + module + u'.main( )> 方法作为工具启动入口')


def createChunToolkit(restore=False):
    # Constants
    ChunDockControlName = r'ChunDockWidget'
    ChunToolkitObjectName = r'ChunToolkitWidget'
    # ChunIntialWidthValue = r'workspacesWidePanelInitialWidth'

    # One-time initialization of the main widget
    # wsControl.ChunToolkit = None
    if wsControl.ChunToolkit is None:
        # Create the main interactive groom spline editor widget
        cmds.waitCursor(state=1)
        wsControl.ChunToolkit = ChunToolkit()
        wsControl.ChunToolkit.setObjectName(ChunToolkitObjectName)
        cmds.waitCursor(state=0)
        # This will happen when someone manually delete the main widget without
        # deleting the owner dock control. Most likely for debugging purpose.
        if not restore:
            # We don't want to raise a control with invalid content so we
            # delete previous control.
            if cmds.workspaceControl(ChunDockControlName, q=True, ex=True):
                cmds.deleteUI(ChunDockControlName)

    # Use workspaceControl command to hold the main widget
    if restore:
        # Get the layout of the parent workspace control and the main widget
        parent = omui.MQtUtil.getCurrentParent()
        widget = omui.MQtUtil.findControl(ChunToolkitObjectName)

        # Add the main widget to the workspace control layout
        omui.MQtUtil.addWidgetToMayaLayout(long_type(widget), long_type(parent))

        # Maya workspace control should never delete its content widget when
        # retain flag is true. But it still deletes in certain cases. We avoid
        # deleting the global widget by removing it from its parent's children.
        # destroyed signal is emitted right before deleting children.
        parentWidget = wrapInstance(long_type(parent), QtWidgets.QWidget)

        #if parentWidget:
        #parentWidget.destroyed.connect(xgg.IgSplineEditor.detachMe)
    else:
        # Create the workspace control from Maya menu
        if cmds.workspaceControl(ChunDockControlName, q=True, ex=True):
            # Raise the workspace control if exists
            cmds.workspaceControl(ChunDockControlName, e=True, vis=True, r=True,
                                  # initialWidth=cmds.optionVar(q=ChunIntialWidthValue),
                                  # minimumWidth=cmds.optionVar(q=ChunIntialWidthValue)
                                  initialWidth=330,
                                  minimumWidth=2
                                  )
        else:
            # Create the workspace control
            LEcomponent = mel.eval(r'getUIComponentDockControl("Channel Box / Layer Editor", false);')
            cmds.workspaceControl(ChunDockControlName,
                                  vis=True,
                                  tabToControl=(LEcomponent, -1),
                                  label='Chun Toolkit',
                                  uiScript='toolkitMain.createChunToolkit(restore=True)',
                                  # initialWidth=cmds.optionVar(q=ChunIntialWidthValue),
                                  # minimumWidth=cmds.optionVar(q=ChunIntialWidthValue)
                                  initialWidth=330,
                                  minimumWidth=2
                                  )
            cmds.workspaceControl(ChunDockControlName, e=True, r=True)