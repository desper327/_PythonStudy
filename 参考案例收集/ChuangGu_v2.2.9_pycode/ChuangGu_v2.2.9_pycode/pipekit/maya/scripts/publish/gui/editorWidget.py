# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editorWidget.ui',
# licensing of 'editorWidget.ui' applies.
#
# Created: Thu Mar  3 17:16:25 2022
#      by: pyside2-uic  running on PySide2 5.12.5
#
# WARNING! All changes made in this file will be lost!
from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from functools import partial
import maya.cmds as cmds


class Ui_Form(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(Ui_Form, self).__init__()
        self.uidict = kwargs
        self.setupUi(self)
        self.assemblyUi()

        # 预设界面
        self.setStyleSheet('''
                QLabel{
                    color: rgb(175, 175, 175);
                }
                QLineEdit, QTextEdit{
                    border-radius: 2px;
                    border:1px solid rgb(50,50,50);
                    background-color: rgb(65,50,50);
                }
                QPushButton{
                    border-radius: 2px;
                    color: rgb(175, 175, 175);
                    background-color: rgb(85,85,85);
                }
                QPushButton:hover{
                    color: rgb(200, 200, 200);
                    background-color: rgb(100,100,100);
                    font:bold 12px
                }
                QPushButton:pressed{
                    color: rgb(150, 100, 150);
                    background-color: rgb(50,50,50);
                    font:bold 12px
                }
        ''')

    def assemblyUi(self):
        k = self.uidict['error']
        v = self.uidict[k]['files']
        if v:
            for i in range(len(v)):
                k1 = v[i].keys()[0]
                v1 = v[i].values()[0]
                pushButton = QtWidgets.QPushButton()
                pushButton.setMinimumSize(QtCore.QSize(240, 20))
                pushButton.setText(k1)
                pushButton.clicked.connect(partial(self.select, k1))
                self.gridLayout.addWidget(pushButton, i, 0, 1, 1)

                lineEdit = QtWidgets.QLineEdit()
                lineEdit.setText(v1)
                lineEdit.setMinimumSize(QtCore.QSize(0, 20))
                lineEdit.setFrame(False)
                lineEdit.setEnabled(False)
                self.gridLayout.addWidget(lineEdit, i, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, len(v)+1, 1, 1, 1)
        self.setWindowTitle('SRF{}: '.format([k]) + self.uidict[k]['title'])
        self.pushButton.clicked.connect(self.close)

    def select(self, obj):
        if cmds.objExists(obj):
            cmds.select(obj, r=1)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(686, 802)
        self.gridLayoutWin = QtWidgets.QGridLayout(Form)
        self.gridLayoutWin.setSpacing(6)
        self.gridLayoutWin.setContentsMargins(5, 5, 5, 5)
        self.gridLayoutWin.setObjectName("gridLayoutWin")
        self.labelPath = QtWidgets.QLabel(Form)
        self.labelPath.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelPath.setFont(font)
        self.labelPath.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelPath.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPath.setObjectName("labelPath")
        self.gridLayoutWin.addWidget(self.labelPath, 0, 1, 1, 1)
        self.labelName = QtWidgets.QLabel(Form)
        self.labelName.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelName.setFont(font)
        self.labelName.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelName.setObjectName("labelName")
        self.gridLayoutWin.addWidget(self.labelName, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(80, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayoutWin.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Panel)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 674, 728))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWin.addWidget(self.scrollArea, 1, 0, 1, 2)
        self.gridLayoutWin.setColumnStretch(0, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.labelPath.setText(QtWidgets.QApplication.translate("Form", "file文件路径", None, -1))
        self.labelName.setText(QtWidgets.QApplication.translate("Form", "file节点名称", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "关闭", None, -1))