# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mayaToFBeekWIcJ.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Ytool(object):
    def setupUi(self, Ytool):
        if Ytool.objectName():
            Ytool.setObjectName(u"Ytool")
        Ytool.resize(1665, 691)
        self.label_5 = QLabel(Ytool)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(590, 30, 341, 41))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.layoutWidget = QWidget(Ytool)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 210, 1611, 100))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setWeight(75)
        self.label_6.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(100, 16777215))
        font2 = QFont()
        font2.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font2.setPointSize(12)
        self.label_8.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_8)

        self.select_cam = QTextEdit(self.layoutWidget)
        self.select_cam.setObjectName(u"select_cam")
        self.select_cam.setMaximumSize(QSize(200, 40))
        font3 = QFont()
        font3.setPointSize(12)
        self.select_cam.setFont(font3)

        self.horizontalLayout_2.addWidget(self.select_cam)

        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_10)

        self.cam_ex_name = QTextEdit(self.layoutWidget)
        self.cam_ex_name.setObjectName(u"cam_ex_name")
        self.cam_ex_name.setMaximumSize(QSize(300, 40))
        self.cam_ex_name.setFont(font3)

        self.horizontalLayout_2.addWidget(self.cam_ex_name)

        self.label_11 = QLabel(self.layoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_11)

        self.cam_ex_path = QTextEdit(self.layoutWidget)
        self.cam_ex_path.setObjectName(u"cam_ex_path")
        self.cam_ex_path.setMaximumSize(QSize(400, 40))
        self.cam_ex_path.setFont(font3)

        self.horizontalLayout_2.addWidget(self.cam_ex_path)

        self.cam_ex_button = QPushButton(self.layoutWidget)
        self.cam_ex_button.setObjectName(u"cam_ex_button")
        self.cam_ex_button.setFont(font2)

        self.horizontalLayout_2.addWidget(self.cam_ex_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.layoutWidget1 = QWidget(Ytool)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(30, 340, 1611, 111))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.layoutWidget1)
        self.label_7.setObjectName(u"label_7")
        font4 = QFont()
        font4.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font4.setPointSize(14)
        font4.setBold(True)
        font4.setWeight(75)
        self.label_7.setFont(font4)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.AniEX_Hbox = QHBoxLayout()
        self.AniEX_Hbox.setObjectName(u"AniEX_Hbox")
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)

        self.AniEX_Hbox.addWidget(self.label)

        self.ref_name = QTextEdit(self.layoutWidget1)
        self.ref_name.setObjectName(u"ref_name")
        self.ref_name.setMaximumSize(QSize(165, 40))
        self.ref_name.setFont(font3)

        self.AniEX_Hbox.addWidget(self.ref_name)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.AniEX_Hbox.addWidget(self.label_4)

        self.ex_bone = QTextEdit(self.layoutWidget1)
        self.ex_bone.setObjectName(u"ex_bone")
        self.ex_bone.setMaximumSize(QSize(200, 40))
        self.ex_bone.setFont(font3)

        self.AniEX_Hbox.addWidget(self.ex_bone)

        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)

        self.AniEX_Hbox.addWidget(self.label_3)

        self.ex_name = QTextEdit(self.layoutWidget1)
        self.ex_name.setObjectName(u"ex_name")
        self.ex_name.setMaximumSize(QSize(300, 40))
        self.ex_name.setFont(font3)

        self.AniEX_Hbox.addWidget(self.ex_name)

        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.AniEX_Hbox.addWidget(self.label_2)

        self.ex_path = QTextEdit(self.layoutWidget1)
        self.ex_path.setObjectName(u"ex_path")
        self.ex_path.setMaximumSize(QSize(400, 40))
        self.ex_path.setFont(font3)

        self.AniEX_Hbox.addWidget(self.ex_path)

        self.ex_buttom = QPushButton(self.layoutWidget1)
        self.ex_buttom.setObjectName(u"ex_buttom")
        self.ex_buttom.setFont(font2)

        self.AniEX_Hbox.addWidget(self.ex_buttom)


        self.verticalLayout_2.addLayout(self.AniEX_Hbox)

        self.layoutWidget2 = QWidget(Ytool)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(130, 120, 1051, 61))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.layoutWidget2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(200, 16777215))
        self.label_9.setFont(font1)

        self.horizontalLayout.addWidget(self.label_9)

        self.mayaPath = QTextEdit(self.layoutWidget2)
        self.mayaPath.setObjectName(u"mayaPath")
        self.mayaPath.setMaximumSize(QSize(400, 40))
        self.mayaPath.setFont(font3)

        self.horizontalLayout.addWidget(self.mayaPath)

        self.selectMayaFile = QPushButton(self.layoutWidget2)
        self.selectMayaFile.setObjectName(u"selectMayaFile")
        font5 = QFont()
        font5.setFamily(u"AcadEref")
        font5.setPointSize(12)
        self.selectMayaFile.setFont(font5)

        self.horizontalLayout.addWidget(self.selectMayaFile)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.retranslateUi(Ytool)

        QMetaObject.connectSlotsByName(Ytool)
    # setupUi

    def retranslateUi(self, Ytool):
        Ytool.setWindowTitle(QCoreApplication.translate("Ytool", u"Dialog", None))
        self.label_5.setText(QCoreApplication.translate("Ytool", u"\u5bfc\u51famaya\u52a8\u753b\u5230FBX", None))
        self.label_6.setText(QCoreApplication.translate("Ytool", u"\u76f8\u673a\u52a8\u753b", None))
        self.label_8.setText(QCoreApplication.translate("Ytool", u"\u9009\u62e9\u76f8\u673a", None))
        self.label_10.setText(QCoreApplication.translate("Ytool", u"\u5bfc\u51fa\u540d\u79f0", None))
        self.label_11.setText(QCoreApplication.translate("Ytool", u"\u5bfc\u51fa\u8def\u5f84", None))
        self.cam_ex_button.setText(QCoreApplication.translate("Ytool", u"\u5bfc\u51fa", None))
        self.label_7.setText(QCoreApplication.translate("Ytool", u"\u9aa8\u9abc\u52a8\u753b", None))
        self.label.setText(QCoreApplication.translate("Ytool", u"\u5f15\u7528\u6587\u4ef6\u540d", None))
        self.label_4.setText(QCoreApplication.translate("Ytool", u"\u9009\u62e9\u5bfc\u51fa\u7684\u9aa8\u9abc\u5c42\u7ea7", None))
        self.label_3.setText(QCoreApplication.translate("Ytool", u"\u5bfc\u51fa\u540d\u79f0", None))
        self.label_2.setText(QCoreApplication.translate("Ytool", u"\u5bfc\u51fa\u8def\u5f84", None))
        self.ex_buttom.setText(QCoreApplication.translate("Ytool", u"\u5bfc\u51fa", None))
        self.label_9.setText(QCoreApplication.translate("Ytool", u"maya\u6587\u4ef6\u8def\u5f84", None))
        self.selectMayaFile.setText(QCoreApplication.translate("Ytool", u"\u9009\u62e9\u6587\u4ef6", None))
    # retranslateUi

