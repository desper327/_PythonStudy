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
from models.data_models import TaskStatus, SignalData, Task

class MainView(QMainWindow):
    """主窗口视图 - 使用手动UI更新方式"""
    
    # 视图信号 - 用于与控制器通信
    # add_task_requested = Signal(dict)  # 请求添加任务
    # delete_task_requested = Signal(int)  # 请求删除任务 (传递索引)
    # update_task_status_requested = Signal(int, TaskStatus)  # 请求更新任务状态
    # clear_all_requested = Signal()  # 请求清空所有任务
    view_signal = Signal(SignalData)  # 视图更新完成信号
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("自定义信号槽架构 - 任务管理器")
        self.setGeometry(100, 100, 900, 700)
        
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
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
    
    def create_task_list_widget(self) -> QWidget:
        """创建任务列表widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        layout.addWidget(QLabel("任务列表 (手动UI更新)"))
        
        # 任务列表 - 使用QListWidget而不是QListView
        self.task_list_widget = QListWidget()
        layout.addWidget(self.task_list_widget)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("删除选中")
        self.mark_progress_button = QPushButton("标记进行中")
        self.mark_completed_button = QPushButton("标记完成")
        self.mark_pending_button = QPushButton("标记待处理")
        
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.mark_progress_button)
        button_layout.addWidget(self.mark_completed_button)
        button_layout.addWidget(self.mark_pending_button)
        
        layout.addLayout(button_layout)
        
        # 清空按钮
        self.clear_all_button = QPushButton("清空所有任务")
        layout.addWidget(self.clear_all_button)
        
        # 连接信号
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.mark_progress_button.clicked.connect(self.on_mark_progress_clicked)
        self.mark_completed_button.clicked.connect(self.on_mark_completed_clicked)
        self.mark_pending_button.clicked.connect(self.on_mark_pending_clicked)
        self.clear_all_button.clicked.connect(self.on_clear_all_clicked)
        
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
        self.status_combo.addItem("已完成", TaskStatus.COMPLETED)
        layout.addWidget(self.status_combo)
        
        # 添加按钮
        self.add_button = QPushButton("添加任务")
        self.add_button.clicked.connect(self.on_add_clicked)
        layout.addWidget(self.add_button)
        
        # 统计信息
        layout.addWidget(QLabel("任务统计:"))
        self.stats_label = QLabel("总计: 0 | 待处理: 0 | 进行中: 0 | 已完成: 0")
        layout.addWidget(self.stats_label)
        
        # 添加弹性空间
        layout.addStretch()
        
        return widget
    
    # ========== 手动UI操作方法 - 供控制器调用 ==========
    
    def add_task_item(self, task_text: str, task_id: int):
        """
        控制器调用的方法：向列表中添加一个新任务项
        
        Args:
            task_text: 显示的任务文本
            task_id: 任务ID，存储在item的data中
        """
        item = QListWidgetItem(task_text)
        item.setData(Qt.UserRole, task_id)  # 存储任务ID
        self.task_list_widget.addItem(item)
    
    def remove_task_item(self, index: int):
        """
        控制器调用的方法：从列表中移除指定索引的任务项
        
        Args:
            index: 要移除的任务索引
        """
        if 0 <= index < self.task_list_widget.count():
            self.task_list_widget.takeItem(index)
    
    def update_task_item(self, index: int, task_text: str):
        """
        控制器调用的方法：更新列表中指定索引的任务项
        
        Args:
            index: 要更新的任务索引
            task_text: 新的任务文本
        """
        if 0 <= index < self.task_list_widget.count():
            item = self.task_list_widget.item(index)
            if item:
                item.setText(task_text)
    
    def clear_task_list(self):
        """控制器调用的方法：清空整个任务列表"""
        self.task_list_widget.clear()
    
    def update_statistics(self, total: int, pending: int, in_progress: int, completed: int):
        """
        控制器调用的方法：更新统计信息
        
        Args:
            total: 总任务数
            pending: 待处理任务数
            in_progress: 进行中任务数
            completed: 已完成任务数
        """
        self.stats_label.setText(
            f"总计: {total} | 待处理: {pending} | 进行中: {in_progress} | 已完成: {completed}"
        )
    
    # ========== 事件处理方法 ==========
    
    def on_add_clicked(self):
        """添加按钮点击事件"""
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        status = self.status_combo.currentData()
        
        if not name:
            QMessageBox.warning(self, "输入错误", "任务名称不能为空！")
            return
        
        task = Task(name=name, description=description, status=status)
        
        # 发射信号请求添加任务
        #self.add_task_requested.emit(task_data)
        self.view_signal.emit(SignalData(signal_type="on_add_clicked", params=[task]))
        
        # 清空输入框
        self.name_input.clear()
        self.description_input.clear()
        self.status_combo.setCurrentIndex(0)
    
    def on_delete_clicked(self):
        """删除按钮点击事件"""
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "确认删除", 
                "确定要删除选中的任务吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # 发射信号请求删除任务
                #self.delete_task_requested.emit(current_row)
                self.view_signal.emit(SignalData(signal_type="on_delete_clicked", params=[current_row]))
        else:
            QMessageBox.information(self, "提示", "请先选择要删除的任务！")
    
    def on_mark_progress_clicked(self):
        """标记进行中按钮点击事件"""
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            #self.update_task_status_requested.emit(current_row, TaskStatus.IN_PROGRESS)
            self.view_signal.emit(SignalData(signal_type="on_mark_progress_clicked", params=[current_row, TaskStatus.IN_PROGRESS]))
        else:
            QMessageBox.information(self, "提示", "请先选择要更新的任务！")
    
    def on_mark_completed_clicked(self):
        """标记完成按钮点击事件"""
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            #self.update_task_status_requested.emit(current_row, TaskStatus.COMPLETED)
            self.view_signal.emit(SignalData(signal_type="on_mark_completed_clicked", params=[current_row, TaskStatus.COMPLETED]))
        else:
            QMessageBox.information(self, "提示", "请先选择要更新的任务！")
    
    def on_mark_pending_clicked(self):
        """标记待处理按钮点击事件"""
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            #self.update_task_status_requested.emit(current_row, TaskStatus.PENDING)
            self.view_signal.emit(SignalData(signal_type="on_mark_pending_clicked", params=[current_row, TaskStatus.PENDING]))
        else:
            QMessageBox.information(self, "提示", "请先选择要更新的任务！")
    
    def on_clear_all_clicked(self):
        """清空所有任务按钮点击事件"""
        if self.task_list_widget.count() > 0:
            reply = QMessageBox.question(
                self, "确认清空", 
                "确定要清空所有任务吗？此操作不可撤销！",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                #self.clear_all_requested.emit()
                self.view_signal.emit(SignalData(signal_type="on_clear_all_clicked", params=[]))
        else:
            QMessageBox.information(self, "提示", "任务列表已经为空！")
    
    def show_message(self, title: str, message: str, msg_type: str = "info"):
        """显示消息框"""
        if msg_type == "error":
            QMessageBox.critical(self, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.information(self, title, message)