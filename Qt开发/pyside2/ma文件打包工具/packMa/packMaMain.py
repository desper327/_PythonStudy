# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
import PyQt5.QtWidgets  as QtWidgets
#导入designer工具生成的login模块
from ui_maPackTool import Ui_Form
import packMa
import time,os
import threading
import subprocess

class MyMainForm(QMainWindow,Ui_Form):#多继承，可以同时使用两个类的函数
    def __init__(self,parent=None):
        super(MyMainForm, self).__init__(parent)#调用父类QMainWindow的构造函数，没有构造Ui_Form中的属性
        self.setupUi(self)#调用Ui_Form中的setupUi函数，构造窗口,把QMainWindow类型对象this传进去
        self.sourcePaths=[]
        self.destinationPath=''
        self.progress=0


    def pack(self):#类内的函数，这个self没什么含义，只代表一个自身的实例，不是参数
        self.sourcePaths=list(set(self.sourcePaths))
        print(self.sourcePaths,self.destinationPath)
        def run_packing():  
            packMa.main(self.sourcePaths, self.destinationPath) 
        thread=threading.Thread(target=run_packing,daemon=True)#这里只有这样写才能开启线程，不然会报错
        thread.start()
        def update_progress(ui):
            progress=0
            while progress<100:
                if os.path.exists(ui.destinationPath + '/进度.txt'): 
                    with open(ui.destinationPath+'/进度.txt','r') as f:
                        try:
                            progress=int(f.read().strip())
                        except:
                            print('进度文件读取出错',str(f.read()))
                    #self.progressBar.setProperty("value", self.progress)
                    ui.progressBar.setValue(progress)
                    print('UI进度条的值目前是:',progress)
                time.sleep(0.5)
            ui.progressBar.setValue(progress)
            ui.progress=progress
            #ui.showMessage()

        def call_update_progress():
            update_progress(self)
            
        threadProgress=threading.Thread(target=call_update_progress,daemon=True)
        threadProgress.start()
        threadProgress.join()
        self.showMessage()


    def showMessage(self):
        os.remove(self.destinationPath + '/进度.txt')
        if self.progress==100:#改到主线程中调用消息box
            QtWidgets.QMessageBox.information(None,'提示','打包完成')
        else:
            QtWidgets.QMessageBox.warning(None,'警告','打包失败,进度是'+str(self.progress))
        

    def source(self):
        paths=self.plainTextEdit.toPlainText()
        for path in paths.split('\n'):
            path=path.strip()
            if os.path.exists(path):
                self.sourcePaths.append(path)
    def destination(self):
        path=self.lineEdit.text()
        if os.path.exists(path):
            self.destinationPath=path
        else:
            os.makedirs(path)
    def setProgress(self,value=0):
        self.progressBar.setValue(value)


if __name__ == "__main__":
    #固定的，PyQt程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)#sys.argv传入的参数是个列表，第一个是文件名和路径
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #myWin.progressBar.hide()
    #print(myWin.PlainText)因为没有构造Ui_Form中的属性，所以这个属性不存在
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())