# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogWidget.ui',
# licensing of 'dialogWidget.ui' applies.
#
# Created: Sat Jan 29 22:18:42 2022
#      by: pyside2-uic  running on PySide2 5.12.5
#
# WARNING! All changes made in this file will be lost!
from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds


class Ui_Form(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, oldList, newList):
        super(Ui_Form, self).__init__()
        self.oldList = oldList
        self.newList = newList
        self.setupUi(self)
        self.assemblyUi()
        self.QpbClose.clicked.connect(self.close)
        self.QlwOld.itemClicked.connect(self.old2newSelect)
        self.QlwNew.itemClicked.connect(self.new2oldSelect)

    def assemblyUi(self):
        oldCount = len(self.oldList)
        newCount = len(self.newList)
        if oldCount < newCount:
            count = newCount
        else:
            count = oldCount

        for i in range(count):
            # old item
            if i < oldCount:
                oldItem = QtWidgets.QListWidgetItem(self.oldList[i])
            else:
                oldItem = QtWidgets.QListWidgetItem('None')
            # new item
            if i < newCount:
                newItem = QtWidgets.QListWidgetItem(self.newList[i])
            else:
                newItem = QtWidgets.QListWidgetItem('None')

            self.QlwOld.addItem(oldItem)
            self.QlwNew.addItem(newItem)
            if oldItem.text() == newItem.text():
                oldItem.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
                newItem.setForeground(QtGui.QBrush(QtGui.QColor(75, 175, 75)))
            else:
                oldItem.setForeground(QtGui.QBrush(QtGui.QColor(175, 75, 75)))
                newItem.setForeground(QtGui.QBrush(QtGui.QColor(175, 75, 75)))

    def old2newSelect(self, args):
        old = self.QlwOld.currentIndex().row()
        self.QlwNew.setCurrentRow(old)

    def new2oldSelect(self, args):
        item = self.QlwNew.currentItem().text().split('|')[-1]
        if 'Shape' in item:
            item = item.split('{')[0]
        if cmds.objExists(item):
            cmds.select(item, r=1)
        new = self.QlwNew.currentIndex().row()
        self.QlwOld.setCurrentRow(new)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(741, 852)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.QlwNew = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.QlwNew.setFont(font)
        self.QlwNew.setObjectName("QlwNew")
        self.gridLayout.addWidget(self.QlwNew, 1, 0, 1, 1)
        self.QlwOld = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.QlwOld.setFont(font)
        self.QlwOld.setObjectName("QlwOld")
        self.gridLayout.addWidget(self.QlwOld, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.QpbClose = QtWidgets.QPushButton(Form)
        self.QpbClose.setMinimumSize(QtCore.QSize(80, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.QpbClose.setFont(font)
        self.QpbClose.setObjectName("QpbClose")
        self.horizontalLayout.addWidget(self.QpbClose)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "大纲版本", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "历史版本", None, -1))
        self.QpbClose.setText(QtWidgets.QApplication.translate("Form", "关闭", None, -1))