# -*- coding: utf-8 -*-

from PySide2 import QtWidgets, QtCore


class PluguiWidget(QtWidgets.QWidget):
    def __init__(self, label=None):
        super(PluguiWidget, self).__init__()
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.setSpacing(2)
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setSpacing(3)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.addLayout(self.hLayout)
        self.QpbExpand = QtWidgets.QPushButton(label)
        self.QpbExpand.setMinimumHeight(18)
        self.QpbExpand.setStyleSheet("font: 12px;text-align: left;"
                                     "padding-left: 4px;"
                                     "padding-bottom: 2px;")
        self.hLayout.addWidget(self.QpbExpand)

        self.QpbHelp = QtWidgets.QPushButton('+')
        self.QpbHelp.setDisabled(True)
        self.QpbHelp.setMaximumSize(QtCore.QSize(16, 16))
        self.QpbHelp.setStyleSheet("font: bold 12px;"
                                   "padding-bottom: 2px;")
        self.hLayout.addWidget(self.QpbHelp)