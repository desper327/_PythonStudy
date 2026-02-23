# -*- coding: utf-8 -*-

from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial
from core import interface


class HelpuiWidget(QtWidgets.QWidget):
    SigIgnore = QtCore.Signal()
    SigRepair = QtCore.Signal()

    def __init__(self, plugin, status, params):
        super(HelpuiWidget, self).__init__()
        self.plugin = plugin
        self.params = params
        self.status = status
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        copyright = interface.copyright()
        if 'PiPiLu' in copyright or 'Chun' in copyright:
            labelName = ['doc', 'class', 'optional', 'default']
            for i in range(len(labelName)):
                label = QtWidgets.QLabel(labelName[i])
                label.setMinimumSize(QtCore.QSize(64, 0))
                label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.gridLayout.addWidget(label, i, 0, 1, 1)
                label.setDisabled(True)
                label.setStyleSheet("background-color: rgb(50, 75, 50);"
                                    "border-radius: 2px;"
                                    "padding-right: 5px;"
                                    )

            font = QtGui.QFont()
            font.setPointSize(9)
            self.Qdoc = QtWidgets.QTextEdit()
            self.Qdoc.setMaximumSize(QtCore.QSize(16777215, 64))
            self.gridLayout.addWidget(self.Qdoc, 0, 1, 1, 1)
            self.Qdoc.setDisabled(True)
            self.Qclassed = QtWidgets.QLineEdit()
            self.gridLayout.addWidget(self.Qclassed, 1, 1, 1, 1)
            self.Qclassed.setDisabled(True)
            self.Qoptional = QtWidgets.QLineEdit()
            self.gridLayout.addWidget(self.Qoptional, 2, 1, 1, 1)
            self.Qoptional.setDisabled(True)
            self.Qdefault = QtWidgets.QLineEdit()
            self.gridLayout.addWidget(self.Qdefault, 3, 1, 1, 1)
            self.Qdefault.setDisabled(True)

            doc = self.params['doc']
            classed = self.params['classed']
            optional = self.params['optional']
            default = self.params['default']
            self.Qdoc.setText(str(doc))
            self.Qclassed.setText(str(classed))
            self.Qoptional.setText(str(optional))
            self.Qdefault.setText(str(default))
            n = 3
        else:
            labelName = ['class', 'optional']
            for i in range(len(labelName)):
                label = QtWidgets.QLabel(labelName[i])
                label.setMinimumSize(QtCore.QSize(64, 0))
                label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
                self.gridLayout.addWidget(label, i, 0, 1, 1)
                label.setDisabled(True)
                label.setStyleSheet("background-color: rgb(50, 75, 50);"
                                    "border-radius: 2px;"
                                    "padding-right: 5px;"
                                    )

            font = QtGui.QFont()
            font.setPointSize(9)
            self.Qclassed = QtWidgets.QLineEdit()
            self.gridLayout.addWidget(self.Qclassed, 0, 1, 1, 1)
            self.Qclassed.setDisabled(True)
            self.Qoptional = QtWidgets.QLineEdit()
            self.gridLayout.addWidget(self.Qoptional, 1, 1, 1, 1)
            self.Qoptional.setDisabled(True)

            classed = self.params['classed']
            optional = self.params['optional']
            self.Qclassed.setText(str(classed))
            self.Qoptional.setText(str(optional))
            n = 1

        if self.status not in ['approve', 'skip']:
            error = self.params['error']
            if error:
                n += 1
                label = QtWidgets.QLabel('error')
                label.setMinimumSize(QtCore.QSize(64, 0))
                label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.gridLayout.addWidget(label, n, 0, 1, 1)
                label.setStyleSheet("background-color: rgb(75, 50, 50);"
                                    "border-radius: 2px;"
                                    "padding-right: 5px;"
                                    )
                self.Qerror = QtWidgets.QTextEdit()
                self.gridLayout.addWidget(self.Qerror, n, 1, 1, 1)
                self.Qerror.setDisabled(True)
                self.Qerror.setStyleSheet("background-color: rgb(75, 50, 50);")
                self.Qerror.setText(str(error))
                self.Qerror.setFont(font)
                self.Qerror.setMaximumSize(QtCore.QSize(16777215, 64))

            if hasattr(self.plugin, 'actions'):
                actions = self.plugin.actions
                for action in actions:
                    n += 1
                    self.QpbButton = QtWidgets.QPushButton(action)
                    self.gridLayout.addWidget(self.QpbButton, n, 1, 1, 1)
                    self.QpbButton.setMinimumSize(QtCore.QSize(0, 20))
                    self.QpbButton.clicked.connect(partial(self.method, action))

            if hasattr(self.plugin, 'repair'):
                n += 1
                self.QpbRepair = QtWidgets.QPushButton('repair')
                self.gridLayout.addWidget(self.QpbRepair, n, 1, 1, 1)
                self.QpbRepair.setMinimumSize(QtCore.QSize(0, 20))
                self.QpbRepair.clicked.connect(self.SigRepair.emit)

            if optional:
                n += 1
                self.QpbIgnore = QtWidgets.QPushButton('ignore')
                self.gridLayout.addWidget(self.QpbIgnore, n, 1, 1, 1)
                self.QpbIgnore.setMinimumSize(QtCore.QSize(0, 20))
                self.QpbIgnore.clicked.connect(self.SigIgnore.emit)

    def method(self, action):
        eval('self.plugin.' + action + '()')