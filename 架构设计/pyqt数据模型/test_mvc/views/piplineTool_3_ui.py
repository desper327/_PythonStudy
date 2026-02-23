# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'piplineTool_3.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QListView, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1390, 770)
        MainWindow.setMinimumSize(QSize(1390, 770))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        self.actionshot = QAction(MainWindow)
        self.actionshot.setObjectName(u"actionshot")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        self.actionshot.setFont(font1)
        self.actionasset = QAction(MainWindow)
        self.actionasset.setObjectName(u"actionasset")
        self.actionasset.setFont(font1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_8 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_main = QTabWidget(self.centralwidget)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setTabPosition(QTabWidget.West)
        self.tab_shot = QWidget()
        self.tab_shot.setObjectName(u"tab_shot")
        self.tab_shot.setEnabled(True)
        self.tab_shot.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.horizontalLayout_29 = QHBoxLayout(self.tab_shot)
        self.horizontalLayout_29.setSpacing(6)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.widget_shot = QWidget(self.tab_shot)
        self.widget_shot.setObjectName(u"widget_shot")
        self.verticalLayout_13 = QVBoxLayout(self.widget_shot)
        self.verticalLayout_13.setSpacing(6)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, -1, -1, 0)
        self.label_logo = QLabel(self.widget_shot)
        self.label_logo.setObjectName(u"label_logo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setMinimumSize(QSize(64, 64))
        self.label_logo.setMaximumSize(QSize(256, 256))
        self.label_logo.setStyleSheet(u"")
        self.label_logo.setTextFormat(Qt.AutoText)
        self.label_logo.setPixmap(QPixmap(u"icons/oc studio animation-\u767d\u5b57\u9ed1\u5e95256.jpg"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setWordWrap(True)

        self.horizontalLayout_14.addWidget(self.label_logo)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_proj = QLabel(self.widget_shot)
        self.label_proj.setObjectName(u"label_proj")
        font2 = QFont()
        font2.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setPointSize(11)
        self.label_proj.setFont(font2)
        self.label_proj.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_proj)

        self.comboBox_proj = QComboBox(self.widget_shot)
        self.comboBox_proj.setObjectName(u"comboBox_proj")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_proj.sizePolicy().hasHeightForWidth())
        self.comboBox_proj.setSizePolicy(sizePolicy1)
        self.comboBox_proj.setFont(font2)

        self.verticalLayout.addWidget(self.comboBox_proj)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_stage = QLabel(self.widget_shot)
        self.label_stage.setObjectName(u"label_stage")
        self.label_stage.setFont(font2)
        self.label_stage.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_stage)

        self.comboBox_stage = QComboBox(self.widget_shot)
        self.comboBox_stage.setObjectName(u"comboBox_stage")
        sizePolicy1.setHeightForWidth(self.comboBox_stage.sizePolicy().hasHeightForWidth())
        self.comboBox_stage.setSizePolicy(sizePolicy1)
        self.comboBox_stage.setFont(font2)

        self.verticalLayout_5.addWidget(self.comboBox_stage)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButton_3 = QRadioButton(self.widget_shot)
        self.radioButton_3.setObjectName(u"radioButton_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.radioButton_3.sizePolicy().hasHeightForWidth())
        self.radioButton_3.setSizePolicy(sizePolicy2)
        self.radioButton_3.setFont(font2)

        self.verticalLayout_2.addWidget(self.radioButton_3)

        self.comboBox_eps = QComboBox(self.widget_shot)
        self.comboBox_eps.setObjectName(u"comboBox_eps")
        sizePolicy1.setHeightForWidth(self.comboBox_eps.sizePolicy().hasHeightForWidth())
        self.comboBox_eps.setSizePolicy(sizePolicy1)
        self.comboBox_eps.setFont(font2)

        self.verticalLayout_2.addWidget(self.comboBox_eps)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.radioButton = QRadioButton(self.widget_shot)
        self.radioButton.setObjectName(u"radioButton")
        sizePolicy2.setHeightForWidth(self.radioButton.sizePolicy().hasHeightForWidth())
        self.radioButton.setSizePolicy(sizePolicy2)
        self.radioButton.setFont(font2)

        self.verticalLayout_3.addWidget(self.radioButton)

        self.comboBox_sc = QComboBox(self.widget_shot)
        self.comboBox_sc.setObjectName(u"comboBox_sc")
        sizePolicy1.setHeightForWidth(self.comboBox_sc.sizePolicy().hasHeightForWidth())
        self.comboBox_sc.setSizePolicy(sizePolicy1)
        self.comboBox_sc.setFont(font2)

        self.verticalLayout_3.addWidget(self.comboBox_sc)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radioButton_2 = QRadioButton(self.widget_shot)
        self.radioButton_2.setObjectName(u"radioButton_2")
        sizePolicy2.setHeightForWidth(self.radioButton_2.sizePolicy().hasHeightForWidth())
        self.radioButton_2.setSizePolicy(sizePolicy2)
        self.radioButton_2.setFont(font2)
        self.radioButton_2.setChecked(True)

        self.verticalLayout_4.addWidget(self.radioButton_2)

        self.comboBox_shot = QComboBox(self.widget_shot)
        self.comboBox_shot.setObjectName(u"comboBox_shot")
        sizePolicy1.setHeightForWidth(self.comboBox_shot.sizePolicy().hasHeightForWidth())
        self.comboBox_shot.setSizePolicy(sizePolicy1)
        self.comboBox_shot.setFont(font2)

        self.verticalLayout_4.addWidget(self.comboBox_shot)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.horizontalLayout_13.addLayout(self.horizontalLayout)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalSpacer = QSpacerItem(30, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer)

        self.checkBox_mytask = QCheckBox(self.widget_shot)
        self.checkBox_mytask.setObjectName(u"checkBox_mytask")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkBox_mytask.sizePolicy().hasHeightForWidth())
        self.checkBox_mytask.setSizePolicy(sizePolicy3)
        self.checkBox_mytask.setMinimumSize(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font3.setPointSize(12)
        self.checkBox_mytask.setFont(font3)
        self.checkBox_mytask.setTristate(False)

        self.horizontalLayout_28.addWidget(self.checkBox_mytask)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_2)


        self.verticalLayout_11.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_frame_rate = QLabel(self.widget_shot)
        self.label_frame_rate.setObjectName(u"label_frame_rate")
        self.label_frame_rate.setMaximumSize(QSize(80, 16777215))
        self.label_frame_rate.setFont(font2)
        self.label_frame_rate.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.label_frame_rate.setMargin(8)

        self.horizontalLayout_2.addWidget(self.label_frame_rate)

        self.label_start_frame = QLabel(self.widget_shot)
        self.label_start_frame.setObjectName(u"label_start_frame")
        self.label_start_frame.setFont(font2)
        self.label_start_frame.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.label_start_frame.setMargin(8)

        self.horizontalLayout_2.addWidget(self.label_start_frame)

        self.label_end_frame = QLabel(self.widget_shot)
        self.label_end_frame.setObjectName(u"label_end_frame")
        self.label_end_frame.setFont(font2)
        self.label_end_frame.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.label_end_frame.setMargin(8)

        self.horizontalLayout_2.addWidget(self.label_end_frame)


        self.verticalLayout_11.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_13.addLayout(self.verticalLayout_11)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_user = QLabel(self.widget_shot)
        self.label_user.setObjectName(u"label_user")
        self.label_user.setFont(font2)
        self.label_user.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_user)

        self.label_department = QLabel(self.widget_shot)
        self.label_department.setObjectName(u"label_department")
        self.label_department.setFont(font2)
        self.label_department.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_department)


        self.horizontalLayout_13.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_13.setStretch(0, 7)
        self.horizontalLayout_13.setStretch(1, 3)
        self.horizontalLayout_13.setStretch(2, 2)

        self.verticalLayout_12.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(8, 8, 8, 10)
        self.label_proj_settings = QLabel(self.widget_shot)
        self.label_proj_settings.setObjectName(u"label_proj_settings")
        self.label_proj_settings.setFont(font2)
        self.label_proj_settings.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_proj_settings)

        self.textBrowser_proj_settings_info = QTextBrowser(self.widget_shot)
        self.textBrowser_proj_settings_info.setObjectName(u"textBrowser_proj_settings_info")
        self.textBrowser_proj_settings_info.setFont(font2)

        self.horizontalLayout_4.addWidget(self.textBrowser_proj_settings_info)


        self.horizontalLayout_12.addLayout(self.horizontalLayout_4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.pushButton_submit_work_file = QPushButton(self.widget_shot)
        self.pushButton_submit_work_file.setObjectName(u"pushButton_submit_work_file")
        self.pushButton_submit_work_file.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_submit_work_file, 2, 0, 1, 1)

        self.pushButton_submit_version_file = QPushButton(self.widget_shot)
        self.pushButton_submit_version_file.setObjectName(u"pushButton_submit_version_file")
        self.pushButton_submit_version_file.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_submit_version_file, 2, 1, 1, 1)

        self.pushButton_assemble = QPushButton(self.widget_shot)
        self.pushButton_assemble.setObjectName(u"pushButton_assemble")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_assemble.sizePolicy().hasHeightForWidth())
        self.pushButton_assemble.setSizePolicy(sizePolicy4)
        self.pushButton_assemble.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_assemble, 0, 0, 1, 1)

        self.pushButton_history = QPushButton(self.widget_shot)
        self.pushButton_history.setObjectName(u"pushButton_history")
        self.pushButton_history.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_history, 0, 1, 1, 1)

        self.pushButton_refresh = QPushButton(self.widget_shot)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_refresh, 2, 2, 1, 1)

        self.pushButton_backup = QPushButton(self.widget_shot)
        self.pushButton_backup.setObjectName(u"pushButton_backup")
        self.pushButton_backup.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_backup, 0, 2, 1, 1)


        self.horizontalLayout_12.addLayout(self.gridLayout)

        self.horizontalLayout_12.setStretch(0, 3)
        self.horizontalLayout_12.setStretch(1, 1)

        self.verticalLayout_12.addLayout(self.horizontalLayout_12)


        self.horizontalLayout_14.addLayout(self.verticalLayout_12)

        self.horizontalLayout_14.setStretch(0, 1)
        self.horizontalLayout_14.setStretch(1, 9)

        self.verticalLayout_13.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.tabWidget_filebox = QTabWidget(self.widget_shot)
        self.tabWidget_filebox.setObjectName(u"tabWidget_filebox")
        self.tabWidget_filebox.setFont(font3)
        self.tab_Storyboard_or_design = QWidget()
        self.tab_Storyboard_or_design.setObjectName(u"tab_Storyboard_or_design")
        self.horizontalLayout_30 = QHBoxLayout(self.tab_Storyboard_or_design)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.tabWidget_filebox.addTab(self.tab_Storyboard_or_design, "")

        self.verticalLayout_19.addWidget(self.tabWidget_filebox)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEdit_path = QLineEdit(self.widget_shot)
        self.lineEdit_path.setObjectName(u"lineEdit_path")
        font4 = QFont()
        font4.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font4.setPointSize(10)
        self.lineEdit_path.setFont(font4)

        self.horizontalLayout_5.addWidget(self.lineEdit_path)

        self.pushButton_open_path = QPushButton(self.widget_shot)
        self.pushButton_open_path.setObjectName(u"pushButton_open_path")
        self.pushButton_open_path.setFont(font2)

        self.horizontalLayout_5.addWidget(self.pushButton_open_path)

        self.pushButton_open_selected_file = QPushButton(self.widget_shot)
        self.pushButton_open_selected_file.setObjectName(u"pushButton_open_selected_file")
        self.pushButton_open_selected_file.setFont(font2)

        self.horizontalLayout_5.addWidget(self.pushButton_open_selected_file)

        self.pushButton_copy_path = QPushButton(self.widget_shot)
        self.pushButton_copy_path.setObjectName(u"pushButton_copy_path")
        self.pushButton_copy_path.setFont(font2)

        self.horizontalLayout_5.addWidget(self.pushButton_copy_path)


        self.verticalLayout_19.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_11.addLayout(self.verticalLayout_19)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.tabWidget_info = QTabWidget(self.widget_shot)
        self.tabWidget_info.setObjectName(u"tabWidget_info")
        self.tabWidget_info.setFont(font3)
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout_20 = QHBoxLayout(self.tab_4)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_task_produce_content = QTextBrowser(self.tab_4)
        self.textBrowser_task_produce_content.setObjectName(u"textBrowser_task_produce_content")
        font5 = QFont()
        font5.setPointSize(11)
        self.textBrowser_task_produce_content.setFont(font5)

        self.horizontalLayout_20.addWidget(self.textBrowser_task_produce_content)

        self.tabWidget_info.addTab(self.tab_4, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget_info.addTab(self.tab_3, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.horizontalLayout_21 = QHBoxLayout(self.tab_5)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_version_file_description = QTextBrowser(self.tab_5)
        self.textBrowser_version_file_description.setObjectName(u"textBrowser_version_file_description")
        self.textBrowser_version_file_description.setFont(font5)

        self.horizontalLayout_21.addWidget(self.textBrowser_version_file_description)

        self.tabWidget_info.addTab(self.tab_5, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_22 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.listView_reference_assets = QListView(self.tab_2)
        self.listView_reference_assets.setObjectName(u"listView_reference_assets")
        self.listView_reference_assets.setFont(font2)

        self.horizontalLayout_22.addWidget(self.listView_reference_assets)

        self.tabWidget_info.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_23 = QHBoxLayout(self.tab)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_local_software = QTextBrowser(self.tab)
        self.textBrowser_local_software.setObjectName(u"textBrowser_local_software")
        self.textBrowser_local_software.setFont(font5)

        self.horizontalLayout_23.addWidget(self.textBrowser_local_software)

        self.tabWidget_info.addTab(self.tab, "")

        self.verticalLayout_14.addWidget(self.tabWidget_info)

        self.tabWidget_task = QTabWidget(self.widget_shot)
        self.tabWidget_task.setObjectName(u"tabWidget_task")
        self.tabWidget_task.setFont(font3)
        self.tabWidget_task.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget_task.setTabPosition(QTabWidget.North)
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.tabWidget_task.addTab(self.widget, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.tabWidget_task.addTab(self.tab_12, "")

        self.verticalLayout_14.addWidget(self.tabWidget_task)

        self.verticalLayout_14.setStretch(0, 1)
        self.verticalLayout_14.setStretch(1, 1)

        self.horizontalLayout_11.addLayout(self.verticalLayout_14)

        self.horizontalLayout_11.setStretch(0, 5)
        self.horizontalLayout_11.setStretch(1, 3)

        self.verticalLayout_13.addLayout(self.horizontalLayout_11)

        self.verticalLayout_13.setStretch(0, 1)
        self.verticalLayout_13.setStretch(1, 9)

        self.horizontalLayout_29.addWidget(self.widget_shot)

        self.tabWidget_main.addTab(self.tab_shot, "")
        self.tab_asset = QWidget()
        self.tab_asset.setObjectName(u"tab_asset")
        self.verticalLayout_18 = QVBoxLayout(self.tab_asset)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.widget_asset = QWidget(self.tab_asset)
        self.widget_asset.setObjectName(u"widget_asset")
        self.verticalLayout_15 = QVBoxLayout(self.widget_asset)
        self.verticalLayout_15.setSpacing(6)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_logo_2 = QLabel(self.widget_asset)
        self.label_logo_2.setObjectName(u"label_logo_2")
        self.label_logo_2.setMaximumSize(QSize(256, 256))
        self.label_logo_2.setTextFormat(Qt.AutoText)

        self.horizontalLayout_15.addWidget(self.label_logo_2)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_proj_2 = QLabel(self.widget_asset)
        self.label_proj_2.setObjectName(u"label_proj_2")
        self.label_proj_2.setFont(font2)
        self.label_proj_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_proj_2)

        self.comboBox_proj_2 = QComboBox(self.widget_asset)
        self.comboBox_proj_2.setObjectName(u"comboBox_proj_2")
        sizePolicy1.setHeightForWidth(self.comboBox_proj_2.sizePolicy().hasHeightForWidth())
        self.comboBox_proj_2.setSizePolicy(sizePolicy1)
        self.comboBox_proj_2.setFont(font2)

        self.verticalLayout_6.addWidget(self.comboBox_proj_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_asset_type = QLabel(self.widget_asset)
        self.label_asset_type.setObjectName(u"label_asset_type")
        self.label_asset_type.setFont(font2)
        self.label_asset_type.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_asset_type)

        self.comboBox_eps_2 = QComboBox(self.widget_asset)
        self.comboBox_eps_2.setObjectName(u"comboBox_eps_2")
        sizePolicy1.setHeightForWidth(self.comboBox_eps_2.sizePolicy().hasHeightForWidth())
        self.comboBox_eps_2.setSizePolicy(sizePolicy1)
        self.comboBox_eps_2.setFont(font2)

        self.verticalLayout_7.addWidget(self.comboBox_eps_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_asset_name = QLabel(self.widget_asset)
        self.label_asset_name.setObjectName(u"label_asset_name")
        self.label_asset_name.setFont(font2)
        self.label_asset_name.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_asset_name)

        self.comboBox_sc_2 = QComboBox(self.widget_asset)
        self.comboBox_sc_2.setObjectName(u"comboBox_sc_2")
        sizePolicy1.setHeightForWidth(self.comboBox_sc_2.sizePolicy().hasHeightForWidth())
        self.comboBox_sc_2.setSizePolicy(sizePolicy1)
        self.comboBox_sc_2.setFont(font2)

        self.verticalLayout_8.addWidget(self.comboBox_sc_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_shot_2 = QLabel(self.widget_asset)
        self.label_shot_2.setObjectName(u"label_shot_2")
        self.label_shot_2.setFont(font2)
        self.label_shot_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_shot_2)

        self.comboBox_shot_2 = QComboBox(self.widget_asset)
        self.comboBox_shot_2.setObjectName(u"comboBox_shot_2")
        sizePolicy1.setHeightForWidth(self.comboBox_shot_2.sizePolicy().hasHeightForWidth())
        self.comboBox_shot_2.setSizePolicy(sizePolicy1)
        self.comboBox_shot_2.setFont(font2)

        self.verticalLayout_9.addWidget(self.comboBox_shot_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_stage_2 = QLabel(self.widget_asset)
        self.label_stage_2.setObjectName(u"label_stage_2")
        self.label_stage_2.setFont(font2)
        self.label_stage_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_stage_2)

        self.comboBox_stage_2 = QComboBox(self.widget_asset)
        self.comboBox_stage_2.setObjectName(u"comboBox_stage_2")
        sizePolicy1.setHeightForWidth(self.comboBox_stage_2.sizePolicy().hasHeightForWidth())
        self.comboBox_stage_2.setSizePolicy(sizePolicy1)
        self.comboBox_stage_2.setFont(font2)

        self.verticalLayout_10.addWidget(self.comboBox_stage_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_10)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_6)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.checkBox_mytask_2 = QCheckBox(self.widget_asset)
        self.checkBox_mytask_2.setObjectName(u"checkBox_mytask_2")
        self.checkBox_mytask_2.setFont(font3)

        self.verticalLayout_17.addWidget(self.checkBox_mytask_2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_frame_rate_2 = QLabel(self.widget_asset)
        self.label_frame_rate_2.setObjectName(u"label_frame_rate_2")
        self.label_frame_rate_2.setMaximumSize(QSize(80, 16777215))
        self.label_frame_rate_2.setFont(font2)
        self.label_frame_rate_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.label_frame_rate_2.setMargin(8)

        self.horizontalLayout_7.addWidget(self.label_frame_rate_2)

        self.label_start_frame_2 = QLabel(self.widget_asset)
        self.label_start_frame_2.setObjectName(u"label_start_frame_2")
        self.label_start_frame_2.setFont(font2)
        self.label_start_frame_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.label_start_frame_2.setMargin(8)

        self.horizontalLayout_7.addWidget(self.label_start_frame_2)

        self.label_end_frame_2 = QLabel(self.widget_asset)
        self.label_end_frame_2.setObjectName(u"label_end_frame_2")
        self.label_end_frame_2.setFont(font2)
        self.label_end_frame_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.label_end_frame_2.setMargin(8)

        self.horizontalLayout_7.addWidget(self.label_end_frame_2)


        self.verticalLayout_17.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_16.addLayout(self.verticalLayout_17)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_user_2 = QLabel(self.widget_asset)
        self.label_user_2.setObjectName(u"label_user_2")
        self.label_user_2.setFont(font2)
        self.label_user_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_user_2)

        self.label_department_2 = QLabel(self.widget_asset)
        self.label_department_2.setObjectName(u"label_department_2")
        self.label_department_2.setFont(font2)
        self.label_department_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_department_2)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_16.setStretch(0, 7)
        self.horizontalLayout_16.setStretch(1, 4)
        self.horizontalLayout_16.setStretch(2, 2)

        self.verticalLayout_16.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_proj_settings_2 = QLabel(self.widget_asset)
        self.label_proj_settings_2.setObjectName(u"label_proj_settings_2")
        self.label_proj_settings_2.setFont(font2)
        self.label_proj_settings_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_10.addWidget(self.label_proj_settings_2)

        self.textBrowser_proj_settings_info_2 = QTextBrowser(self.widget_asset)
        self.textBrowser_proj_settings_info_2.setObjectName(u"textBrowser_proj_settings_info_2")
        self.textBrowser_proj_settings_info_2.setFont(font2)

        self.horizontalLayout_10.addWidget(self.textBrowser_proj_settings_info_2)


        self.horizontalLayout_17.addLayout(self.horizontalLayout_10)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(0)
        self.pushButton_submit_work_file_2 = QPushButton(self.widget_asset)
        self.pushButton_submit_work_file_2.setObjectName(u"pushButton_submit_work_file_2")
        self.pushButton_submit_work_file_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_submit_work_file_2, 2, 0, 1, 1)

        self.pushButton_submit_version_file_2 = QPushButton(self.widget_asset)
        self.pushButton_submit_version_file_2.setObjectName(u"pushButton_submit_version_file_2")
        self.pushButton_submit_version_file_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_submit_version_file_2, 2, 1, 1, 1)

        self.pushButton_refresh_2 = QPushButton(self.widget_asset)
        self.pushButton_refresh_2.setObjectName(u"pushButton_refresh_2")
        self.pushButton_refresh_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_refresh_2, 2, 2, 1, 1)

        self.pushButton_assemble_2 = QPushButton(self.widget_asset)
        self.pushButton_assemble_2.setObjectName(u"pushButton_assemble_2")
        sizePolicy4.setHeightForWidth(self.pushButton_assemble_2.sizePolicy().hasHeightForWidth())
        self.pushButton_assemble_2.setSizePolicy(sizePolicy4)
        self.pushButton_assemble_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_assemble_2, 0, 0, 1, 1)

        self.pushButton_assemble_hip_2 = QPushButton(self.widget_asset)
        self.pushButton_assemble_hip_2.setObjectName(u"pushButton_assemble_hip_2")
        self.pushButton_assemble_hip_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_assemble_hip_2, 0, 1, 1, 1)

        self.pushButton_history_2 = QPushButton(self.widget_asset)
        self.pushButton_history_2.setObjectName(u"pushButton_history_2")
        self.pushButton_history_2.setFont(font2)

        self.gridLayout_2.addWidget(self.pushButton_history_2, 0, 2, 1, 1)


        self.horizontalLayout_17.addLayout(self.gridLayout_2)

        self.horizontalLayout_17.setStretch(0, 4)
        self.horizontalLayout_17.setStretch(1, 2)

        self.verticalLayout_16.addLayout(self.horizontalLayout_17)


        self.horizontalLayout_15.addLayout(self.verticalLayout_16)

        self.horizontalLayout_15.setStretch(0, 1)
        self.horizontalLayout_15.setStretch(1, 7)

        self.verticalLayout_15.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.tabWidget_filebox_2 = QTabWidget(self.widget_asset)
        self.tabWidget_filebox_2.setObjectName(u"tabWidget_filebox_2")
        self.tabWidget_filebox_2.setFont(font3)
        self.tab_Storyboard_or_design_2 = QWidget()
        self.tab_Storyboard_or_design_2.setObjectName(u"tab_Storyboard_or_design_2")
        self.tabWidget_filebox_2.addTab(self.tab_Storyboard_or_design_2, "")

        self.horizontalLayout_18.addWidget(self.tabWidget_filebox_2)

        self.tabWidget_info_2 = QTabWidget(self.widget_asset)
        self.tabWidget_info_2.setObjectName(u"tabWidget_info_2")
        self.tabWidget_info_2.setFont(font3)
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.horizontalLayout_24 = QHBoxLayout(self.tab_6)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.textBrowser_task_produce_content_2 = QTextBrowser(self.tab_6)
        self.textBrowser_task_produce_content_2.setObjectName(u"textBrowser_task_produce_content_2")
        self.textBrowser_task_produce_content_2.setFont(font5)

        self.horizontalLayout_24.addWidget(self.textBrowser_task_produce_content_2)

        self.tabWidget_info_2.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.tabWidget_info_2.addTab(self.tab_7, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.horizontalLayout_25 = QHBoxLayout(self.tab_8)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.textBrowser_version_file_description_2 = QTextBrowser(self.tab_8)
        self.textBrowser_version_file_description_2.setObjectName(u"textBrowser_version_file_description_2")
        self.textBrowser_version_file_description_2.setFont(font5)

        self.horizontalLayout_25.addWidget(self.textBrowser_version_file_description_2)

        self.tabWidget_info_2.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.horizontalLayout_26 = QHBoxLayout(self.tab_9)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.listView_reference_assets_2 = QListView(self.tab_9)
        self.listView_reference_assets_2.setObjectName(u"listView_reference_assets_2")
        self.listView_reference_assets_2.setFont(font2)

        self.horizontalLayout_26.addWidget(self.listView_reference_assets_2)

        self.tabWidget_info_2.addTab(self.tab_9, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.horizontalLayout_27 = QHBoxLayout(self.tab_10)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.textBrowser_local_software_2 = QTextBrowser(self.tab_10)
        self.textBrowser_local_software_2.setObjectName(u"textBrowser_local_software_2")
        self.textBrowser_local_software_2.setFont(font5)

        self.horizontalLayout_27.addWidget(self.textBrowser_local_software_2)

        self.tabWidget_info_2.addTab(self.tab_10, "")

        self.horizontalLayout_18.addWidget(self.tabWidget_info_2)

        self.horizontalLayout_18.setStretch(0, 5)
        self.horizontalLayout_18.setStretch(1, 3)

        self.verticalLayout_15.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.lineEdit_path_2 = QLineEdit(self.widget_asset)
        self.lineEdit_path_2.setObjectName(u"lineEdit_path_2")
        self.lineEdit_path_2.setFont(font4)

        self.horizontalLayout_19.addWidget(self.lineEdit_path_2)

        self.pushButton_open_path_2 = QPushButton(self.widget_asset)
        self.pushButton_open_path_2.setObjectName(u"pushButton_open_path_2")
        self.pushButton_open_path_2.setFont(font2)

        self.horizontalLayout_19.addWidget(self.pushButton_open_path_2)

        self.pushButton_open_selected_file_2 = QPushButton(self.widget_asset)
        self.pushButton_open_selected_file_2.setObjectName(u"pushButton_open_selected_file_2")
        self.pushButton_open_selected_file_2.setFont(font2)

        self.horizontalLayout_19.addWidget(self.pushButton_open_selected_file_2)

        self.pushButton_copy_path_2 = QPushButton(self.widget_asset)
        self.pushButton_copy_path_2.setObjectName(u"pushButton_copy_path_2")
        self.pushButton_copy_path_2.setFont(font2)

        self.horizontalLayout_19.addWidget(self.pushButton_copy_path_2)


        self.verticalLayout_15.addLayout(self.horizontalLayout_19)

        self.verticalLayout_15.setStretch(0, 3)
        self.verticalLayout_15.setStretch(1, 9)
        self.verticalLayout_15.setStretch(2, 1)

        self.verticalLayout_18.addWidget(self.widget_asset)

        self.tabWidget_main.addTab(self.tab_asset, "")

        self.horizontalLayout_8.addWidget(self.tabWidget_main)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        sizePolicy1.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy1)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_filebox.setCurrentIndex(0)
        self.tabWidget_info.setCurrentIndex(0)
        self.tabWidget_task.setCurrentIndex(0)
        self.tabWidget_filebox_2.setCurrentIndex(0)
        self.tabWidget_info_2.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionshot.setText(QCoreApplication.translate("MainWindow", u"shot", None))
        self.actionasset.setText(QCoreApplication.translate("MainWindow", u"asset", None))
        self.label_logo.setText("")
        self.label_proj.setText(QCoreApplication.translate("MainWindow", u"\u9879\u76ee", None))
        self.label_stage.setText(QCoreApplication.translate("MainWindow", u"\u9636\u6bb5", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"\u96c6\uff08\u4efb\u52a1\uff09", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"\u573a\uff08\u4efb\u52a1\uff09", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"\u955c\uff08\u4efb\u52a1\uff09", None))
        self.checkBox_mytask.setText(QCoreApplication.translate("MainWindow", u"\u6211\u7684\u4efb\u52a1", None))
        self.label_frame_rate.setText(QCoreApplication.translate("MainWindow", u"\u5e27\u7387", None))
        self.label_start_frame.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5e27", None))
        self.label_end_frame.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u5e27", None))
        self.label_user.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237", None))
        self.label_department.setText(QCoreApplication.translate("MainWindow", u"\u90e8\u95e8", None))
        self.label_proj_settings.setText(QCoreApplication.translate("MainWindow", u"\u9879\u76ee\u8bbe\u7f6e\u4fe1\u606f", None))
        self.pushButton_submit_work_file.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4\u5230\u5de5\u4f5c\u4e2d", None))
        self.pushButton_submit_version_file.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4\u5230\u5ba1\u6838", None))
        self.pushButton_assemble.setText(QCoreApplication.translate("MainWindow", u"\u7ec4\u88c5ma\u6587\u4ef6", None))
        self.pushButton_history.setText(QCoreApplication.translate("MainWindow", u"\u5386\u53f2\u8bb0\u5f55", None))
        self.pushButton_refresh.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0", None))
        self.pushButton_backup.setText(QCoreApplication.translate("MainWindow", u"\u5907\u7528", None))
        self.tabWidget_filebox.setTabText(self.tabWidget_filebox.indexOf(self.tab_Storyboard_or_design), QCoreApplication.translate("MainWindow", u"\u5206\u955c\u6216\u8bbe\u5b9a\u56fe", None))
        self.pushButton_open_path.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6\u5939", None))
        self.pushButton_open_selected_file.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u9009\u4e2d\u6587\u4ef6", None))
        self.pushButton_copy_path.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236\u5b8c\u6574\u8def\u5f84", None))
        self.tabWidget_info.setTabText(self.tabWidget_info.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u5236\u4f5c\u5185\u5bb9", None))
        self.tabWidget_info.setTabText(self.tabWidget_info.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u6279\u6ce8", None))
        self.tabWidget_info.setTabText(self.tabWidget_info.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"\u7248\u672c\u6587\u4ef6\u63cf\u8ff0", None))
        self.tabWidget_info.setTabText(self.tabWidget_info.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u5173\u8054\u8d44\u4ea7", None))
        self.tabWidget_info.setTabText(self.tabWidget_info.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u672c\u5730\u8f6f\u4ef6", None))
        self.tabWidget_task.setTabText(self.tabWidget_task.indexOf(self.widget), QCoreApplication.translate("MainWindow", u"\u6700\u8fd1\u4efb\u52a1", None))
        self.tabWidget_task.setTabText(self.tabWidget_task.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"\u95ee\u9898\u53cd\u9988", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_shot), QCoreApplication.translate("MainWindow", u"\u955c\u5934", None))
        self.label_logo_2.setText(QCoreApplication.translate("MainWindow", u"TextLabelLogo", None))
        self.label_proj_2.setText(QCoreApplication.translate("MainWindow", u"\u9879\u76eeproj", None))
        self.label_asset_type.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578btype", None))
        self.label_asset_name.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u4ea7\u540dname", None))
        self.label_shot_2.setText(QCoreApplication.translate("MainWindow", u"\u955cshot", None))
        self.label_stage_2.setText(QCoreApplication.translate("MainWindow", u"\u9636\u6bb5stage", None))
        self.checkBox_mytask_2.setText(QCoreApplication.translate("MainWindow", u"\u6211\u7684\u4efb\u52a1", None))
        self.label_frame_rate_2.setText(QCoreApplication.translate("MainWindow", u"\u5e27\u7387", None))
        self.label_start_frame_2.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5e27", None))
        self.label_end_frame_2.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u5e27", None))
        self.label_user_2.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237", None))
        self.label_department_2.setText(QCoreApplication.translate("MainWindow", u"\u90e8\u95e8", None))
        self.label_proj_settings_2.setText(QCoreApplication.translate("MainWindow", u"\u9879\u76ee\u8bbe\u7f6e\u4fe1\u606f", None))
        self.pushButton_submit_work_file_2.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4\u5230\u5de5\u4f5c\u4e2d", None))
        self.pushButton_submit_version_file_2.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4\u5230\u5ba1\u6838", None))
        self.pushButton_refresh_2.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0", None))
        self.pushButton_assemble_2.setText(QCoreApplication.translate("MainWindow", u"\u7ec4\u88c5ma\u6587\u4ef6", None))
        self.pushButton_assemble_hip_2.setText(QCoreApplication.translate("MainWindow", u"\u7ec4\u88c5hip\u6587\u4ef6", None))
        self.pushButton_history_2.setText(QCoreApplication.translate("MainWindow", u"\u5386\u53f2\u8bb0\u5f55", None))
        self.tabWidget_filebox_2.setTabText(self.tabWidget_filebox_2.indexOf(self.tab_Storyboard_or_design_2), QCoreApplication.translate("MainWindow", u"\u5206\u955c\u6216\u8bbe\u5b9a\u56fe", None))
        self.tabWidget_info_2.setTabText(self.tabWidget_info_2.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u5236\u4f5c\u5185\u5bb9", None))
        self.tabWidget_info_2.setTabText(self.tabWidget_info_2.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"\u6279\u6ce8", None))
        self.tabWidget_info_2.setTabText(self.tabWidget_info_2.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"\u7248\u672c\u6587\u4ef6\u63cf\u8ff0", None))
        self.tabWidget_info_2.setTabText(self.tabWidget_info_2.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"\u5173\u8054\u8d44\u4ea7", None))
        self.tabWidget_info_2.setTabText(self.tabWidget_info_2.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"\u672c\u5730\u8f6f\u4ef6", None))
        self.pushButton_open_path_2.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6\u5939", None))
        self.pushButton_open_selected_file_2.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u9009\u4e2d\u6587\u4ef6", None))
        self.pushButton_copy_path_2.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236\u5b8c\u6574\u8def\u5f84", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_asset), QCoreApplication.translate("MainWindow", u"\u8d44\u4ea7", None))
    # retranslateUi

