"""
主视图 - 负责UI界面的显示和用户交互
使用QListWidget而不是QListView，支持手动操作UI元素
"""
from Qt.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QPushButton, QLineEdit, QTextEdit,
    QLabel, QComboBox, QMessageBox, QSplitter, QListWidgetItem
)
# from Qt.QtCore import Qt, Signal
from views.ui_main_view import Ui_MainWindow
from models.data_models import SignalData, TextData
from Qt.QtCore import Signal

class MainView(Ui_MainWindow, QMainWindow):
    """主窗口视图 - 使用手动UI更新方式"""
    view_signal = Signal(SignalData)  # 视图信号
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_signals()
    
    def connect_signals(self):
        self.button.clicked.connect(self.on_show_text)
    
    # ======= 手动UI操作方法 - 供控制器调用 ==========
    def on_show_text(self):
        text_data=TextData(text=self.line_edit.text())
        self.view_signal.emit(SignalData(signal_type='on_show_text', params={"text_data": text_data}))
        
        
    def show_error(self, error: str):
        """显示错误信息"""
        QMessageBox.critical(self, "错误", error)
