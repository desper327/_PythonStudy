# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from Qt.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from Qt.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from Qt.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
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
        self.show_label.setGeometry(QRect(100, 190, 111, 51))
        self.button_thread = QPushButton(self.centralwidget)
        self.button_thread.setObjectName(u"button_thread")
        self.button_thread.setGeometry(QRect(90, 280, 241, 21))
        self.thread_label = QLabel(self.centralwidget)
        self.thread_label.setObjectName(u"thread_label")
        self.thread_label.setGeometry(QRect(90, 320, 111, 51))
        self.button_process = QPushButton(self.centralwidget)
        self.button_process.setObjectName(u"button_process")
        self.button_process.setGeometry(QRect(90, 420, 241, 21))
        self.process_label = QLabel(self.centralwidget)
        self.process_label.setObjectName(u"process_label")
        self.process_label.setGeometry(QRect(90, 480, 111, 51))
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
        self.button_thread.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5b50\u7ebf\u7a0b", None))
        self.thread_label.setText(QCoreApplication.translate("MainWindow", u"\u672a\u5b9a\u4e49", None))
        self.button_process.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5b50\u8fdb\u7a0b", None))
        self.process_label.setText(QCoreApplication.translate("MainWindow", u"\u672a\u5b9a\u4e49", None))
    # retranslateUi

