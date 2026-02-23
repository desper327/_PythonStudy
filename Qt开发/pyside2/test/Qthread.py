import sys,time
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, QTimer, Signal
#导入designer工具生成的login模块
from testUI import Ui_Form




class myThread(QThread):
    finished = Signal()  # 将Signal声明为类属性
    
    def __init__(self, parent=None):
        super(myThread, self).__init__(parent)
        self.flag = True

    def run(self):
        #while self.flag:
        print("running")
        time.sleep(3)
        print("running2")
        self.flag = False
        self.finished.emit()





class MyMainForm(QMainWindow, Ui_Form):#多继承，可以同时使用两个类的函数
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)#调用父类QMainWindow的构造函数
        self.setupUi(self)#调用Ui_Form中的setupUi函数，构造窗口
        self.pushButton.clicked.connect(self.anxia)#连接槽函数

    def anxia(self):
        print("按下了按键")
        #self.lineEdit.clear()
        t1=myThread()
        t1.finished.connect(self.wancheng)
        t1.finished.connect(t1.deleteLater)
        t1.start()



    def wancheng(self):
        self.lineEdit.setText("结束")




if __name__ == "__main__":
    #固定的，PyQt程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)#sys.argv传入的参数是个列表，第一个是文件名和路径
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec())