"""
主窗口视图
应用程序的主界面，包含菜单栏、工具栏、状态栏和主要内容区域
"""
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit, QGroupBox,
    QMenuBar, QToolBar, QStatusBar, QSplitter, QListWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QIcon, QFont
from beartype import beartype
from models.base_model import UIState


class MainWindow(QMainWindow):
    """
    主窗口类
    应用程序的主界面，提供完整的用户交互界面
    """
    
    # 信号定义
    user_action_triggered = Signal(str, dict)  # 用户操作信号，参数：action_name, data
    async_task_requested = Signal(str, dict)  # 异步任务请求信号
    thread_task_requested = Signal(str, dict)  # 线程任务请求信号
    dialog_requested = Signal(str, dict)  # 对话框请求信号
    
    @beartype
    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化主窗口
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.ui_state = UIState()
        self._setup_ui()
        self._connect_signals()
        self._setup_status_update_timer()
    
    @beartype
    def _setup_ui(self) -> None:
        """
        设置用户界面
        """
        self.setWindowTitle(self.ui_state.window_title)
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # 创建菜单栏
        self._create_menu_bar()
        
        # 创建工具栏
        self._create_tool_bar()
        
        # 创建状态栏
        self._create_status_bar()
        
        # 创建中央窗口部件
        self._create_central_widget()
    
    @beartype
    def _create_menu_bar(self) -> None:
        """
        创建菜单栏
        """
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        new_action = QAction("新建(&N)", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(lambda: self.user_action_triggered.emit("new_file", {}))
        file_menu.addAction(new_action)
        
        open_action = QAction("打开(&O)", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(lambda: self.user_action_triggered.emit("open_file", {}))
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 任务菜单
        task_menu = menubar.addMenu("任务(&T)")
        
        async_task_action = QAction("异步任务(&A)", self)
        async_task_action.triggered.connect(self._request_async_task)
        task_menu.addAction(async_task_action)
        
        thread_task_action = QAction("线程任务(&T)", self)
        thread_task_action.triggered.connect(self._request_thread_task)
        task_menu.addAction(thread_task_action)
        
        task_menu.addSeparator()
        
        batch_task_action = QAction("批量任务(&B)", self)
        batch_task_action.triggered.connect(self._request_batch_task)
        task_menu.addAction(batch_task_action)
        
        # 窗口菜单
        window_menu = menubar.addMenu("窗口(&W)")
        
        feature_dialog_action = QAction("功能对话框(&F)", self)
        feature_dialog_action.triggered.connect(self._open_feature_dialog)
        window_menu.addAction(feature_dialog_action)
        
        data_dialog_action = QAction("数据处理对话框(&D)", self)
        data_dialog_action.triggered.connect(self._open_data_dialog)
        window_menu.addAction(data_dialog_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    @beartype
    def _create_tool_bar(self) -> None:
        """
        创建工具栏
        """
        toolbar = self.addToolBar("主工具栏")
        toolbar.setMovable(False)
        
        # 异步任务按钮
        async_btn = QPushButton("异步任务")
        async_btn.setToolTip("启动异步任务")
        async_btn.clicked.connect(self._request_async_task)
        toolbar.addWidget(async_btn)
        
        # 线程任务按钮
        thread_btn = QPushButton("线程任务")
        thread_btn.setToolTip("启动线程任务")
        thread_btn.clicked.connect(self._request_thread_task)
        toolbar.addWidget(thread_btn)
        
        toolbar.addSeparator()
        
        # 功能对话框按钮
        dialog_btn = QPushButton("功能对话框")
        dialog_btn.setToolTip("打开功能对话框")
        dialog_btn.clicked.connect(self._open_feature_dialog)
        toolbar.addWidget(dialog_btn)
        
        # 数据处理按钮
        data_btn = QPushButton("数据处理")
        data_btn.setToolTip("打开数据处理对话框")
        data_btn.clicked.connect(self._open_data_dialog)
        toolbar.addWidget(data_btn)
    
    @beartype
    def _create_status_bar(self) -> None:
        """
        创建状态栏
        """
        self.status_bar = self.statusBar()
        
        # 状态标签
        self.status_label = QLabel(self.ui_state.status_message)
        self.status_bar.addWidget(self.status_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 任务计数标签
        self.task_count_label = QLabel("任务: 0")
        self.status_bar.addPermanentWidget(self.task_count_label)
    
    @beartype
    def _create_central_widget(self) -> None:
        """
        创建中央窗口部件
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧面板
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧面板
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
    
    @beartype
    def _create_left_panel(self) -> QWidget:
        """
        创建左侧面板
        
        Returns:
            QWidget: 左侧面板窗口部件
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 操作按钮组
        button_group = QGroupBox("操作面板")
        button_layout = QGridLayout(button_group)
        
        # 用户管理按钮
        user_mgmt_btn = QPushButton("用户管理")
        user_mgmt_btn.clicked.connect(lambda: self.user_action_triggered.emit("user_management", {}))
        button_layout.addWidget(user_mgmt_btn, 0, 0)
        
        # 数据分析按钮
        data_analysis_btn = QPushButton("数据分析")
        data_analysis_btn.clicked.connect(lambda: self.user_action_triggered.emit("data_analysis", {}))
        button_layout.addWidget(data_analysis_btn, 0, 1)
        
        # 报告生成按钮
        report_btn = QPushButton("生成报告")
        report_btn.clicked.connect(lambda: self.user_action_triggered.emit("generate_report", {}))
        button_layout.addWidget(report_btn, 1, 0)
        
        # 数据导出按钮
        export_btn = QPushButton("数据导出")
        export_btn.clicked.connect(lambda: self.user_action_triggered.emit("export_data", {}))
        button_layout.addWidget(export_btn, 1, 1)
        
        layout.addWidget(button_group)
        
        # 任务列表
        task_group = QGroupBox("任务列表")
        task_layout = QVBoxLayout(task_group)
        
        self.task_list = QListWidget()
        task_layout.addWidget(self.task_list)
        
        # 任务控制按钮
        task_control_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("取消选中")
        cancel_btn.clicked.connect(self._cancel_selected_task)
        task_control_layout.addWidget(cancel_btn)
        
        clear_btn = QPushButton("清空完成")
        clear_btn.clicked.connect(self._clear_completed_tasks)
        task_control_layout.addWidget(clear_btn)
        
        task_layout.addLayout(task_control_layout)
        layout.addWidget(task_group)
        
        return panel
    
    @beartype
    def _create_right_panel(self) -> QWidget:
        """
        创建右侧面板
        
        Returns:
            QWidget: 右侧面板窗口部件
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 数据显示表格
        data_group = QGroupBox("数据显示")
        data_layout = QVBoxLayout(data_group)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["ID", "名称", "状态", "时间"])
        
        # 设置表格属性
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        data_layout.addWidget(self.data_table)
        layout.addWidget(data_group)
        
        # 日志显示区域
        log_group = QGroupBox("系统日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        
        # 设置日志字体
        font = QFont("Consolas", 9)
        self.log_text.setFont(font)
        
        log_layout.addWidget(self.log_text)
        
        # 日志控制按钮
        log_control_layout = QHBoxLayout()
        
        clear_log_btn = QPushButton("清空日志")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_control_layout.addWidget(clear_log_btn)
        
        log_control_layout.addStretch()
        log_layout.addLayout(log_control_layout)
        
        layout.addWidget(log_group)
        
        return panel
    
    @beartype
    def _connect_signals(self) -> None:
        """
        连接信号槽
        """
        pass  # 信号连接将在控制器中处理
    
    @beartype
    def _setup_status_update_timer(self) -> None:
        """
        设置状态更新定时器
        """
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status_display)
        self.status_timer.start(1000)  # 每秒更新一次
    
    @beartype
    def _request_async_task(self) -> None:
        """
        请求异步任务
        """
        task_data = {
            "task_type": "data_processing",
            "parameters": {
                "data_size": 1000,
                "processing_delay": 0.01
            }
        }
        self.async_task_requested.emit("async_data_processing", task_data)
    
    @beartype
    def _request_thread_task(self) -> None:
        """
        请求线程任务
        """
        task_data = {
            "task_type": "long_running",
            "parameters": {
                "duration": 5.0,
                "steps": 10
            }
        }
        self.thread_task_requested.emit("thread_long_running", task_data)
    
    @beartype
    def _request_batch_task(self) -> None:
        """
        请求批量任务
        """
        task_data = {
            "task_type": "batch_processing",
            "parameters": {
                "user_ids": [1, 2, 3, 4, 5],
                "operation": "activate"
            }
        }
        self.user_action_triggered.emit("batch_process_users", task_data)
    
    @beartype
    def _open_feature_dialog(self) -> None:
        """
        打开功能对话框
        """
        dialog_data = {
            "dialog_type": "feature",
            "title": "功能对话框",
            "modal": True
        }
        self.dialog_requested.emit("feature_dialog", dialog_data)
    
    @beartype
    def _open_data_dialog(self) -> None:
        """
        打开数据处理对话框
        """
        dialog_data = {
            "dialog_type": "data_processing",
            "title": "数据处理对话框",
            "modal": False
        }
        self.dialog_requested.emit("data_dialog", dialog_data)
    
    @beartype
    def _cancel_selected_task(self) -> None:
        """
        取消选中的任务
        """
        current_item = self.task_list.currentItem()
        if current_item:
            task_id = current_item.data(Qt.UserRole)
            if task_id:
                self.user_action_triggered.emit("cancel_task", {"task_id": task_id})
    
    @beartype
    def _clear_completed_tasks(self) -> None:
        """
        清空已完成的任务
        """
        self.user_action_triggered.emit("clear_completed_tasks", {})
    
    @beartype
    def _show_about(self) -> None:
        """
        显示关于对话框
        """
        QMessageBox.about(
            self,
            "关于 MVC Framework",
            "MVC Framework v1.0\n\n"
            "基于PySide6的MVC架构桌面应用程序框架\n"
            "支持异步任务、多线程处理和数据验证\n\n"
            "技术栈：\n"
            "- PySide6 (Qt界面)\n"
            "- Pydantic (数据验证)\n"
            "- Beartype (类型检查)\n"
            "- asyncio (异步处理)"
        )
    
    @beartype
    def _update_status_display(self) -> None:
        """
        更新状态显示
        """
        # 更新状态标签
        self.status_label.setText(self.ui_state.status_message)
        
        # 更新进度条可见性
        self.progress_bar.setVisible(self.ui_state.is_loading)
    
    # 公共方法 - 供控制器调用
    
    @beartype
    def update_ui_state(self, ui_state: UIState) -> None:
        """
        更新UI状态
        
        Args:
            ui_state: UI状态对象
        """
        self.ui_state = ui_state
        self.setWindowTitle(ui_state.window_title)
    
    @beartype
    def show_loading(self, loading: bool, message: str = "") -> None:
        """
        显示加载状态
        
        Args:
            loading: 是否正在加载
            message: 状态消息
        """
        self.ui_state.set_loading(loading, message)
        self.progress_bar.setVisible(loading)
        if message:
            self.status_label.setText(message)
    
    @beartype
    def update_progress(self, progress: float, message: str = "") -> None:
        """
        更新进度
        
        Args:
            progress: 进度百分比
            message: 进度消息
        """
        self.progress_bar.setValue(int(progress))
        if message:
            self.status_label.setText(message)
    
    @beartype
    def add_task_to_list(self, task_id: str, task_name: str, status: str = "运行中") -> None:
        """
        添加任务到列表
        
        Args:
            task_id: 任务ID
            task_name: 任务名称
            status: 任务状态
        """
        item_text = f"{task_name} - {status}"
        item = self.task_list.addItem(item_text)
        if item:
            item.setData(Qt.UserRole, task_id)
    
    @beartype
    def update_task_in_list(self, task_id: str, status: str, progress: float = 0) -> None:
        """
        更新任务列表中的任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            progress: 进度百分比
        """
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            if item and item.data(Qt.UserRole) == task_id:
                # 更新显示文本
                base_text = item.text().split(" - ")[0]
                if progress > 0:
                    item.setText(f"{base_text} - {status} ({progress:.1f}%)")
                else:
                    item.setText(f"{base_text} - {status}")
                break
    
    @beartype
    def remove_task_from_list(self, task_id: str) -> None:
        """
        从任务列表中移除任务
        
        Args:
            task_id: 任务ID
        """
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            if item and item.data(Qt.UserRole) == task_id:
                self.task_list.takeItem(i)
                break
    
    @beartype
    def update_task_count(self, count: int) -> None:
        """
        更新任务计数显示
        
        Args:
            count: 任务数量
        """
        self.task_count_label.setText(f"任务: {count}")
    
    @beartype
    def add_log_message(self, message: str) -> None:
        """
        添加日志消息
        
        Args:
            message: 日志消息
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_text.append(log_entry)
    
    @beartype
    def update_data_table(self, data: list) -> None:
        """
        更新数据表格
        
        Args:
            data: 数据列表
        """
        self.data_table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(item.get("id", ""))))
            self.data_table.setItem(row, 1, QTableWidgetItem(str(item.get("name", ""))))
            self.data_table.setItem(row, 2, QTableWidgetItem(str(item.get("status", ""))))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(item.get("time", ""))))
    
    def closeEvent(self, event) -> None:
        """
        窗口关闭事件
        """
        # 发射关闭信号，让控制器处理清理工作
        self.user_action_triggered.emit("application_closing", {})
        event.accept()
