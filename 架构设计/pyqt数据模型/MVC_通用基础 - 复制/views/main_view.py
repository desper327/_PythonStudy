"""
主视图 - 负责UI界面的显示和用户交互
使用QListWidget而不是QListView，支持手动操作UI元素
"""
from Qt.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QPushButton, QLineEdit, QTextEdit,
    QLabel, QComboBox, QMessageBox, QSplitter, QListWidgetItem
)
from Qt.QtCore import Qt, Signal
from models.data_models import SignalData, TextData

class MainView(QMainWindow):
    """主窗口视图 - 使用手动UI更新方式"""
    view_signal = Signal(SignalData)  # 视图信号
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("MVC通用基础")
        self.setGeometry(100, 100, 400, 400)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建基础
        self.line_edit=QLineEdit()
        self.line_edit.setPlaceholderText("输入一个名称")
        main_layout.addWidget(self.line_edit)
        
        self.button = QPushButton("显示")
        self.button.clicked.connect(self.on_show_text)
        main_layout.addWidget(self.button)
        
        self.show_label = QLabel("未定义")  
        main_layout.addWidget(self.show_label)

        self.button_thread = QPushButton("开始子线程")
        self.button_thread.clicked.connect(self.on_start_thread)
        main_layout.addWidget(self.button_thread)
        
        self.thread_label = QLabel("未定义")  
        main_layout.addWidget(self.thread_label)

    # ======= 手动UI操作方法 - 供控制器调用 ==========
    def on_show_text(self):
        text_data=TextData(text=self.line_edit.text())
        self.view_signal.emit(SignalData(signal_type='on_show_text', params=[text_data]))
        
    def on_start_thread(self):
        self.view_signal.emit(SignalData(signal_type='on_start_thread', params=[]))
        
    def show_error(self, error: str):
        """显示错误信息"""
        QMessageBox.critical(self, "错误", error)
