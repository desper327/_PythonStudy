# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PySide6.QtWidgets import QApplication, QMainWindow
#导入designer工具生成的login模块
from testUI import Ui_Form
 
class MyMainForm(QMainWindow, Ui_Form):#多继承，可以同时使用两个类的函数
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)#调用父类QMainWindow的构造函数
        self.setupUi(self)#调用Ui_Form中的setupUi函数，构造窗口
 
if __name__ == "__main__":
    #固定的，PyQt程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)#sys.argv传入的参数是个列表，第一个是文件名和路径
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())