# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(437, 612)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.line_edit = QLineEdit(self.centralwidget)
        self.line_edit.setObjectName(u"line_edit")
        self.line_edit.setGeometry(QRect(100, 70, 181, 21))
        self.button = QPushButton(self.centralwidget)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(100, 130, 171, 25))
        self.show_label = QLabel(self.centralwidget)
        self.show_label.setObjectName(u"show_label")
        self.show_label.setGeometry(QRect(110, 190, 111, 51))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MVC\u901a\u7528\u57fa\u7840", None))
        self.line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u4e00\u4e2a\u540d\u79f0", None))
        self.button.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a", None))
        self.show_label.setText(QCoreApplication.translate("MainWindow", u"\u672a\u5b9a\u4e49", None))
    # retranslateUi

