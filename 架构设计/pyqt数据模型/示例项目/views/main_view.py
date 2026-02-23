"""
主视图 - 负责UI界面的显示和用户交互
"""
from Qt.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QPushButton, QLineEdit, QTextEdit,
    QLabel, QComboBox, QMessageBox, QSplitter
)
from Qt.QtCore import Qt, Signal
from models.data_models import TaskStatus
from models.qt_models import TaskListModel
class MainView(QMainWindow):
    """主窗口视图"""
    
    # 视图信号 - 用于与控制器通信
    addTaskRequested = Signal(dict)  # 请求添加任务
    deleteTaskRequested = Signal(int)  # 请求删除任务
    updateTaskStatusRequested = Signal(int, TaskStatus)  # 请求更新任务状态
    
    def __init__(self):
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        """设置用户界面"""
        self.setWindowTitle("标准MVC架构 - 任务管理器")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧：任务列表
        left_widget = self.create_task_list_widget()
        splitter.addWidget(left_widget)
        
        # 右侧：任务详情和操作
        right_widget = self.create_task_detail_widget()
        splitter.addWidget(right_widget)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
    
    def create_task_list_widget(self) -> QWidget:
        """创建任务列表widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        layout.addWidget(QLabel("任务列表"))
        
        # 任务列表视图
        self.task_list_view = QListWidget()
        layout.addWidget(self.task_list_view)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("删除选中")
        self.mark_progress_button = QPushButton("标记进行中")
        self.mark_completed_button = QPushButton("标记完成")
        
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.mark_progress_button)
        button_layout.addWidget(self.mark_completed_button)
        
        layout.addLayout(button_layout)
        
        # 连接信号
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.mark_progress_button.clicked.connect(self.on_mark_progress_clicked)
        self.mark_completed_button.clicked.connect(self.on_mark_completed_clicked)
        
        return widget
    
    def create_task_detail_widget(self) -> QWidget:
        """创建任务详情widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        layout.addWidget(QLabel("添加新任务"))
        
        # 任务名称输入
        layout.addWidget(QLabel("任务名称:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入任务名称")
        layout.addWidget(self.name_input)
        
        # 任务描述输入
        layout.addWidget(QLabel("任务描述:"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("输入任务描述（可选）")
        self.description_input.setMaximumHeight(100)
        layout.addWidget(self.description_input)
        
        # 任务状态选择
        layout.addWidget(QLabel("初始状态:"))
        self.status_combo = QComboBox()
        self.status_combo.addItem("待处理", TaskStatus.PENDING)
        self.status_combo.addItem("进行中", TaskStatus.IN_PROGRESS)
        layout.addWidget(self.status_combo)
        
        # 添加按钮
        self.add_button = QPushButton("添加任务")
        self.add_button.clicked.connect(self.on_add_clicked)
        layout.addWidget(self.add_button)
        
        # 添加弹性空间
        layout.addStretch()
        
        return widget
    
    def set_model(self, model):
        """设置数据模型"""
        # self.task_list_view.setModel(model)
        pass

    def add_task_item(self, text: str):
        """控制器调用的方法：向列表中添加一个新项"""
        self.task_list_view.addItem(text)
    
    def remove_task_item(self, row: int):
        """控制器调用的方法：从列表中移除一个项"""
        self.task_list_view.takeItem(row)

    def update_task_item(self, row: int, text: str):
        """控制器调用的方法：更新列表中的一个项"""
        item = self.task_list_view.item(row)
        if item:
            item.setText(text)

    def clear_task_list(self):
        """控制器调用的方法：清空整个列表"""
        self.task_list_view.clear()
    
    def on_add_clicked(self):
        """添加按钮点击事件"""
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        status = self.status_combo.currentData()
        
        if not name:
            QMessageBox.warning(self, "输入错误", "任务名称不能为空！")
            return
        
        task_data = {
            'name': name,
            'description': description if description else None,
            'status': status
        }
        
        self.addTaskRequested.emit(task_data)
        
        # 清空输入框
        self.name_input.clear()
        self.description_input.clear()
        self.status_combo.setCurrentIndex(0)
    
    def on_delete_clicked(self):
        """删除按钮点击事件"""
        current_row = self.task_list_view.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "确认删除", 
                "确定要删除选中的任务吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.deleteTaskRequested.emit(current_row)
        else:
            QMessageBox.information(self, "提示", "请先选择要删除的任务！")
    
    def on_mark_progress_clicked(self):
        """标记进行中按钮点击事件"""
        current_row = self.task_list_view.currentRow()
        if current_row >= 0:
            self.updateTaskStatusRequested.emit(current_row, TaskStatus.IN_PROGRESS)
        else:
            QMessageBox.information(self, "提示", "请先选择要更新的任务！")
    
    def on_mark_completed_clicked(self):
        """标记完成按钮点击事件"""
        current_row = self.task_list_view.currentRow()
        if current_row >= 0:
            self.updateTaskStatusRequested.emit(current_row, TaskStatus.COMPLETED)
        else:
            QMessageBox.information(self, "提示", "请先选择要更新的任务！")
    
    def show_message(self, title: str, message: str, msg_type: str = "info"):
        """显示消息框"""
        if msg_type == "error":
            QMessageBox.critical(self, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.information(self, title, message)