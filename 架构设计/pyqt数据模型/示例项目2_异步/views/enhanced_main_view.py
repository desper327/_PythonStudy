"""
增强版主视图 - 支持异步任务处理和进度反馈
集成了线程池任务管理器，提供非阻塞的用户体验
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QPushButton, QLineEdit, QTextEdit,
    QLabel, QComboBox, QMessageBox, QSplitter, QListWidgetItem,
    QProgressBar, QStatusBar, QGroupBox, QSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from models.data_models import TaskStatus
from utils.async_task_manager import get_task_manager
import time


class EnhancedMainView(QMainWindow):
    """增强版主窗口视图 - 支持异步任务处理"""
    
    # 视图信号 - 用于与控制器通信
    add_task_requested = pyqtSignal(dict)  # 请求添加任务
    delete_task_requested = pyqtSignal(int)  # 请求删除任务
    update_task_status_requested = pyqtSignal(int, TaskStatus)  # 请求更新任务状态
    clear_all_requested = pyqtSignal()  # 请求清空所有任务
    
    # 异步操作信号
    fetch_remote_tasks_requested = pyqtSignal()  # 请求获取远程任务
    sync_tasks_requested = pyqtSignal()  # 请求同步任务
    export_tasks_requested = pyqtSignal(str)  # 请求导出任务
    
    def __init__(self):
        super().__init__()
        
        # 获取任务管理器
        self.task_manager = get_task_manager()
        
        # 连接任务管理器信号
        self.connect_task_manager_signals()
        
        # 设置UI
        self.setup_ui()
        
        # 活跃任务计数
        self.active_tasks = {}
    
    def connect_task_manager_signals(self):
        """连接任务管理器的信号"""
        self.task_manager.task_started.connect(self.on_async_task_started)
        self.task_manager.task_finished.connect(self.on_async_task_finished)
        self.task_manager.task_failed.connect(self.on_async_task_failed)
        self.task_manager.task_progress.connect(self.on_async_task_progress)
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("增强版任务管理器 - 支持异步操作")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 状态栏中的进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 状态栏中的任务计数标签
        self.task_count_label = QLabel("活跃任务: 0")
        self.status_bar.addPermanentWidget(self.task_count_label)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 添加异步操作控制面板
        async_panel = self.create_async_operations_panel()
        main_layout.addWidget(async_panel)
        
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
        
        # 设置初始状态消息
        self.status_bar.showMessage("就绪 - 支持异步任务处理")
    
    def create_async_operations_panel(self) -> QWidget:
        """创建异步操作控制面板"""
        group_box = QGroupBox("异步操作演示")
        layout = QHBoxLayout(group_box)
        
        # 模拟网络延迟控制
        layout.addWidget(QLabel("模拟延迟(秒):"))
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 10)
        self.delay_spinbox.setValue(3)
        layout.addWidget(self.delay_spinbox)
        
        # 异步操作按钮
        self.fetch_remote_button = QPushButton("获取远程任务")
        self.sync_tasks_button = QPushButton("同步任务到服务器")
        self.export_tasks_button = QPushButton("导出任务数据")
        self.heavy_computation_button = QPushButton("执行重计算")
        
        layout.addWidget(self.fetch_remote_button)
        layout.addWidget(self.sync_tasks_button)
        layout.addWidget(self.export_tasks_button)
        layout.addWidget(self.heavy_computation_button)
        
        # 连接信号
        self.fetch_remote_button.clicked.connect(self.on_fetch_remote_clicked)
        self.sync_tasks_button.clicked.connect(self.on_sync_tasks_clicked)
        self.export_tasks_button.clicked.connect(self.on_export_tasks_clicked)
        self.heavy_computation_button.clicked.connect(self.on_heavy_computation_clicked)
        
        layout.addStretch()
        return group_box
    
    def create_task_list_widget(self) -> QWidget:
        """创建任务列表widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title_label = QLabel("任务列表 (异步UI更新)")
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 任务列表
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
        title_label = QLabel("添加新任务")
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
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
        
        # 异步任务状态
        layout.addWidget(QLabel("异步任务状态:"))
        self.async_status_label = QLabel("无活跃任务")
        layout.addWidget(self.async_status_label)
        
        # 添加弹性空间
        layout.addStretch()
        
        return widget
    
    # ========== 异步操作处理方法 ==========
    
    def on_fetch_remote_clicked(self):
        """获取远程任务按钮点击事件"""
        delay = self.delay_spinbox.value()
        
        def simulate_fetch_remote_tasks():
            """模拟从远程服务器获取任务"""
            time.sleep(delay)  # 模拟网络延迟
            
            # 模拟返回的远程任务数据
            remote_tasks = [
                {
                    'name': f'远程任务 {int(time.time()) % 1000}',
                    'description': '从服务器获取的任务',
                    'status': TaskStatus.PENDING
                },
                {
                    'name': f'同步任务 {int(time.time()) % 1000}',
                    'description': '需要同步的重要任务',
                    'status': TaskStatus.IN_PROGRESS
                }
            ]
            return remote_tasks
        
        # 异步执行获取任务
        task_id = self.task_manager.run_async(
            simulate_fetch_remote_tasks,
            task_id="fetch_remote",
            on_finished=self.on_remote_tasks_fetched,
            on_error=self.on_remote_fetch_error
        )
        
        self.show_message("信息", "正在获取远程任务，请稍候...")
    
    def on_sync_tasks_clicked(self):
        """同步任务按钮点击事件"""
        delay = self.delay_spinbox.value()
        
        def simulate_sync_tasks():
            """模拟同步任务到服务器"""
            time.sleep(delay)  # 模拟网络延迟
            return {"synced_count": 5, "server_response": "同步成功"}
        
        # 异步执行同步
        task_id = self.task_manager.run_async(
            simulate_sync_tasks,
            task_id="sync_tasks",
            on_finished=self.on_tasks_synced,
            on_error=self.on_sync_error
        )
        
        self.show_message("信息", "正在同步任务到服务器，请稍候...")
    
    def on_export_tasks_clicked(self):
        """导出任务按钮点击事件"""
        delay = self.delay_spinbox.value()
        
        def simulate_export_tasks():
            """模拟导出任务数据"""
            time.sleep(delay)  # 模拟文件I/O延迟
            return {"exported_file": "tasks_export.json", "task_count": 10}
        
        # 异步执行导出
        task_id = self.task_manager.run_async(
            simulate_export_tasks,
            task_id="export_tasks",
            on_finished=self.on_tasks_exported,
            on_error=self.on_export_error
        )
        
        self.show_message("信息", "正在导出任务数据，请稍候...")
    
    def on_heavy_computation_clicked(self):
        """重计算按钮点击事件"""
        def heavy_computation():
            """模拟CPU密集型计算"""
            result = 0
            for i in range(10000000):  # 大量计算
                result += i * i
            return {"computation_result": result, "iterations": 10000000}
        
        # 异步执行重计算
        task_id = self.task_manager.run_async(
            heavy_computation,
            task_id="heavy_computation",
            on_finished=self.on_computation_finished,
            on_error=self.on_computation_error
        )
        
        self.show_message("信息", "正在执行重计算，请稍候...")
    
    # ========== 异步任务回调方法 ==========
    
    def on_remote_tasks_fetched(self, tasks_data):
        """远程任务获取完成回调"""
        self.show_message("成功", f"成功获取 {len(tasks_data)} 个远程任务！")
        
        # 这里可以发射信号给控制器来添加这些任务
        for task_data in tasks_data:
            self.add_task_requested.emit(task_data)
    
    def on_remote_fetch_error(self, error):
        """远程任务获取错误回调"""
        self.show_message("错误", f"获取远程任务失败: {error}", "error")
    
    def on_tasks_synced(self, result):
        """任务同步完成回调"""
        synced_count = result.get('synced_count', 0)
        self.show_message("成功", f"成功同步 {synced_count} 个任务到服务器！")
    
    def on_sync_error(self, error):
        """任务同步错误回调"""
        self.show_message("错误", f"同步任务失败: {error}", "error")
    
    def on_tasks_exported(self, result):
        """任务导出完成回调"""
        file_name = result.get('exported_file', 'unknown')
        task_count = result.get('task_count', 0)
        self.show_message("成功", f"成功导出 {task_count} 个任务到文件: {file_name}")
    
    def on_export_error(self, error):
        """任务导出错误回调"""
        self.show_message("错误", f"导出任务失败: {error}", "error")
    
    def on_computation_finished(self, result):
        """重计算完成回调"""
        iterations = result.get('iterations', 0)
        self.show_message("成功", f"重计算完成！处理了 {iterations:,} 次迭代")
    
    def on_computation_error(self, error):
        """重计算错误回调"""
        self.show_message("错误", f"重计算失败: {error}", "error")
    
    # ========== 异步任务管理器信号处理 ==========
    
    def on_async_task_started(self, task_id: str):
        """异步任务开始处理"""
        self.active_tasks[task_id] = time.time()
        self.update_async_status()
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度的进度条
        
        self.status_bar.showMessage(f"任务 {task_id} 开始执行...")
    
    def on_async_task_finished(self, task_id: str, result):
        """异步任务完成处理"""
        if task_id in self.active_tasks:
            start_time = self.active_tasks[task_id]
            duration = time.time() - start_time
            del self.active_tasks[task_id]
            
            self.status_bar.showMessage(f"任务 {task_id} 完成 (耗时: {duration:.2f}秒)", 3000)
        
        self.update_async_status()
        
        # 如果没有活跃任务，隐藏进度条
        if not self.active_tasks:
            self.progress_bar.setVisible(False)
    
    def on_async_task_failed(self, task_id: str, error: str):
        """异步任务失败处理"""
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
        
        self.update_async_status()
        
        # 如果没有活跃任务，隐藏进度条
        if not self.active_tasks:
            self.progress_bar.setVisible(False)
        
        self.status_bar.showMessage(f"任务 {task_id} 失败: {error}", 5000)
    
    def on_async_task_progress(self, task_id: str, progress: int, message: str):
        """异步任务进度处理"""
        if progress >= 0:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(progress)
        
        self.status_bar.showMessage(f"{task_id}: {message}")
    
    def update_async_status(self):
        """更新异步任务状态显示"""
        active_count = len(self.active_tasks)
        self.task_count_label.setText(f"活跃任务: {active_count}")
        
        if active_count == 0:
            self.async_status_label.setText("无活跃任务")
        else:
            task_list = ", ".join(self.active_tasks.keys())
            self.async_status_label.setText(f"活跃任务: {task_list}")
    
    # ========== 原有的UI操作方法 ==========
    
    def add_task_item(self, task_text: str, task_id: int):
        """向列表中添加一个新任务项"""
        item = QListWidgetItem(task_text)
        item.setData(Qt.UserRole, task_id)
        self.task_list_widget.addItem(item)
    
    def remove_task_item(self, index: int):
        """从列表中移除指定索引的任务项"""
        if 0 <= index < self.task_list_widget.count():
            self.task_list_widget.takeItem(index)
    
    def update_task_item(self, index: int, task_text: str):
        """更新列表中指定索引的任务项"""
        if 0 <= index < self.task_list_widget.count():
            item = self.task_list_widget.item(index)
            if item:
                item.setText(task_text)
    
    def clear_task_list(self):
        """清空整个任务列表"""
        self.task_list_widget.clear()
    
    def update_statistics(self, total: int, pending: int, in_progress: int, completed: int):
        """更新统计信息"""
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
        
        task_data = {
            'name': name,
            'description': description if description else None,
            'status': status
        }
        
        self.add_task_requested.emit(task_data)
        
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
                self.delete_task_requested.emit(current_row)
        else:
            QMessageBox.information(self, "提示", "请先选择要删除的任务！")
    
    def on_mark_progress_clicked(self):
        """标记进行中按钮点击事件"""
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            self.update_task_status_requested.emit(current_row, TaskStatus.IN_PROGRESS)
        else:
            QMessageBox.information(self, "提示", "请先选择要更新的任务！")
    
    def on_mark_completed_clicked(self):
        """标记完成按钮点击事件"""
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            self.update_task_status_requested.emit(current_row, TaskStatus.COMPLETED)
        else:
            QMessageBox.information(self, "提示", "请先选择要更新的任务！")
    
    def on_mark_pending_clicked(self):
        """标记待处理按钮点击事件"""
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            self.update_task_status_requested.emit(current_row, TaskStatus.PENDING)
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
                self.clear_all_requested.emit()
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
