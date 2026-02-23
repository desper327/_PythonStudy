import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from  mayaToFBX import Ui_Ytool
#import mayaFunction

#创建类，类里面实现了UI窗口
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Ytool()
        self.ui.setupUi(self)
        self.ui.selectMayaFile.clicked.connect(self.showDialog)
    def showDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog  # 如果你想使用 PyQt5 的对话框而不是系统默认对话框

        filter = "Text Files (*.ma);;All Files (*)"
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '', filter, options=options)

        if file_name:
            print('Selected File:', file_name)
            self.ui.mayaPath.setText(file_name[0])
            #self.ui.ref_name.setText(mayaFunction.reference_files[0])




#单独用2020的mayapy来运行mayaStandalone的代码，获得需要的信息，传递给UI，
#然后导出maya文件，最后关闭文件
#+++++++++++++++++++++++++++++++++
import subprocess

# 定义Python2.7解释器的路径
python27_path = "C:/Program Files/Autodesk/Maya2020/bin/mayapy.exe"

# 定义要执行的脚本路径
script_path = "F:/Study/Python/NORMAL_PY/pyqt5/mayaFunction.py"

# 使用subprocess调用Python2.7解释器执行脚本
subprocess.call([python27_path, script_path])

#+++++++++++++++++++++++++++++++++




#如果是主函数则运行
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())