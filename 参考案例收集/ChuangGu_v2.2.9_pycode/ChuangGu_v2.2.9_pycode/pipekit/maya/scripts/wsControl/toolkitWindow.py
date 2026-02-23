# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolkitWindow.ui',
# licensing of 'toolkitWindow.ui' applies.
#
# Created: Sun Dec 19 23:07:09 2021
#      by: pyside2-uic  running on PySide2 5.12.5
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(337, 764)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frameToolkit = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameToolkit.sizePolicy().hasHeightForWidth())
        self.frameToolkit.setSizePolicy(sizePolicy)
        self.frameToolkit.setFocusPolicy(QtCore.Qt.TabFocus)
        self.frameToolkit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameToolkit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameToolkit.setObjectName("frameToolkit")
        self.verticalLayoutToolkit = QtWidgets.QVBoxLayout(self.frameToolkit)
        self.verticalLayoutToolkit.setSpacing(5)
        self.verticalLayoutToolkit.setContentsMargins(5, 5, 5, 5)
        self.verticalLayoutToolkit.setObjectName("verticalLayoutToolkit")
        self.toolBox = QtWidgets.QToolBox(self.frameToolkit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.toolBox.setFont(font)
        self.toolBox.setStyleSheet("color: rgb(35, 35, 35);")
        self.toolBox.setObjectName("toolBox")
        self.verticalLayoutToolkit.addWidget(self.toolBox)
        self.horizontalLayout.addWidget(self.frameToolkit)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))

