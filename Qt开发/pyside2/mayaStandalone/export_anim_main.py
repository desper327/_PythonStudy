'''
import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QFileDialog, QHBoxLayout
from PySide2.QtCore import Qt
from PySide2.QtGui import QClipboard



class FileViewerWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和大小
        self.setWindowTitle("文件内容查看器")
        self.setGeometry(100, 100, 600, 400)
        
        # 主布局
        self.layout = QVBoxLayout()

        # 文件名输入框
        self.filename_input = QLineEdit(self)
        self.filename_input.setPlaceholderText("选择文件后显示文件名")
        self.filename_input.setReadOnly(True)
        self.layout.addWidget(self.filename_input)

        # 选择文件按钮
        self.select_button = QPushButton("选择文件", self)
        self.select_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_button)

        # 显示文件内容的文本框，带滚动条
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)  # 不允许编辑
        self.text_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.layout.addWidget(self.text_area)

        # 复制选中行的按钮
        self.copy_button = QPushButton("复制选中行", self)
        self.copy_button.clicked.connect(self.copy_selected_line)
        self.layout.addWidget(self.copy_button)

        # 设置布局
        self.setLayout(self.layout)

    def select_file(self):


    def copy_selected_line(self):
        # 获取选中的文本
        selected_text = self.text_area.textCursor().selectedText()
        
        if selected_text:
            # 将选中的文本复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_text)
            print(f"已复制: {selected_text}")
        else:
            print("没有选中任何文本")
'''


import sys
import os
import time
import subprocess
import socket
import json
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog,QMessageBox#PySide2. 居然和numpy有关系
from ui_export_anim import Ui_Form



#sys.path.insert(0, r'C:\Program Files\Autodesk\Maya2020\Python\Lib\site-packages')
#sys.path.insert(0, r'C:\Program Files\Autodesk\Maya2024\Python\Lib\site-packages')
#sys.path.insert(0, r'C:\Program Files\Autodesk\Maya2020\Python\Lib\site-packages\maya')
# import maya.cmds as cmds
# import maya.standalone
# maya.standalone.initialize()



class ExportForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ExportForm, self).__init__(parent)
        self.setupUi(self)
        self.export_txt = r'C:\ProgramData\MT_tray\standaloneExport.txt'
        self.mayaexe=''
        self.file_path=''
        self.checkMayaExe()
        self.read_ma_script = r'F:\Study\BaiduSyncdisk\MyStudy\pyside2\mayaStandalone\read_ma_script.py'
        self.export_bone_Anim_script = r'F:\Study\BaiduSyncdisk\MyStudy\pyside2\mayaStandalone\export_bone_anim_script.py'
        self.export_mesh_Anim_script = r'F:\Study\BaiduSyncdisk\MyStudy\pyside2\mayaStandalone\export_mesh_anim_script.py'
        self.standalone_server_path = r'F:\Study\BaiduSyncdisk\MyStudy\pyside2\mayaStandalone\standalone_server.py'
        self.root_bone_node = ''


    def selectMayaExe(self):
        exe_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Maya EXE (*.exe);")
        if exe_path:
            exe_path = exe_path.replace('/', '\\').replace('maya.exe', 'mayapy.exe')
            with open(self.export_txt, 'w', encoding='utf-8') as file:
                file.write(exe_path)
        self.checkMayaExe()

    def checkMayaExe(self):
        if os.path.exists(self.export_txt):
            with open(self.export_txt, 'r', encoding='utf-8') as file:
                file_path = file.readline().strip()
            if os.path.exists(file_path):
                self.mayaexe = file_path
                self.pushButton_2.setText(f"Maya EXE路径已选好")
                self.pushButton_2.setEnabled(False)


    def selectMaFile(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Maya Files (*.ma *.mb)")
        if self.file_path:
            self.textEdit.setText(self.file_path)
            #self.file_path=self.file_path.replace('/', '\\')
            response=self.send_command_to_maya("open_file", {"file_path": self.file_path})
            self.textEdit_2.setText(response)
            #root_nodes=self.send_command_to_maya("get_root_nodes")
            #print(type(root_nodes))
            #self.textEdit_2.setText(root_nodes)


    def ExportAnim(self):
        self.root_bone_node=self.textEdit_2.textCursor().selectedText()
        try:
            response = self.send_command_to_maya("export_bone_anim", {"root_bone_node": self.root_bone_node})
            print('response 是:',response)
        except Exception as e:
            print(f"Error from main: {e}")
        
            QMessageBox.warning(self, "导出结果是：", self.root_bone_node)
    
    
    def ExportAnimWithMesh(self):
        if self.file_path:
            process = subprocess.Popen([self.mayaexe, self.export_mesh_Anim_script, self.file_path],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
            process.wait()
            output, errors = process.communicate()
            if errors:
                QMessageBox.warning(self, "导出错误：", errors)
            else:
                QMessageBox.warning(self, "导出成功！")



    def send_command_to_maya(self, command, data=None):
        try:
            """Send a command to Maya Standalone server and get response."""
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", 12345))
                request = {"command": command}
                if data:
                    request.update(data)
                
                # Send JSON request
                print('json是')
                print(json.dumps(request).encode("utf-8"))
                s.sendall(json.dumps(request).encode("utf-8"))
                print('11111111111111')
                # Receive JSON response
                response_data = s.recv(4096).decode("utf-8")
                print('22222222222222')
                print('response_data:',response_data)
                response = json.loads(response_data)
                print('33333333333333')
                print('response是',response)
        
        except Exception as e:
            print(f"错误了aaa: {e}")
            #QMessageBox.warning(self, "错误", f"请重试")
            response = 'nothing'
        return response








if __name__ == "__main__":


    app = QApplication(sys.argv)
    window = ExportForm()
    window.show()
    subprocess.Popen([window.mayaexe, window.standalone_server_path],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    #time.sleep(2)
    sys.exit(app.exec_())
    