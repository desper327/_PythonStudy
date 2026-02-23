#coding:utf-8
import sys
import time
from PySide6.QtWidgets import QApplication, QWidget

if __name__ == "__main__":
    # 1.创建一个QApplication类的实例
    app = QApplication(sys.argv)
    # 2.创建一个窗口
    window = QWidget()
    # 3.设置窗口的尺寸
    window.resize(300, 150)
    # 4.移动窗口
    window.move(300, 300)
    # 5.设置窗口标题
    window.setWindowTitle("基于PySide的桌面应用程序")
    # 6.展示窗口
    window.show()
    # 7.执行exec()方法，进入事件循环，若遇到窗口退出命名，返回整数n
    n = app.exec_()
    # 8.进入程序的主循环并通过exit()函数确保主循环安全结束
    time.sleep(3)
    sys.exit(n)
