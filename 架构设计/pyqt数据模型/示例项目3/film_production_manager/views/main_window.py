"""
主窗口视图
包含项目选择、层级导航、任务列表等主要界面组件
"""
from typing import List, Dict, Any, Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QComboBox, QLabel, QLineEdit,
    QGroupBox, QFrame, QTabWidget, QStatusBar, QMenuBar,
    QMenu, QToolBar, QMessageBox, QProgressDialog, QDialog
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QIcon, QFont

from ..models.data_models import Project, Episode, Scene, Shot, Task, ProductionStage, TaskStatus
from ..utils.common_widgets import (
    ProgressWidget, ReportDialog, ProjectStatisticsWidget, 
    FilterWidget, ReportGenerator
)


class ProjectTreeWidget(QTreeWidget):
    """项目层级树形组件"""
    
    # 信号
    item_selected = Signal(str, str)  # (item_type, item_id)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_project = None
    
    def setup_ui(self):
        """设置UI"""
        self.setHeaderLabel("项目结构")
        self.setExpandsOnDoubleClick(True)
        self.itemClicked.connect(self._on_item_clicked)
        
        # 设置样式
        self.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QTreeWidget::item {
                padding: 4px;
                border-bottom: 1px solid #eee;
            }
            QTreeWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QTreeWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)
    
    def load_project(self, project: Project):
        """加载项目数据"""
        self.clear()
        self.current_project = project
        
        if not project:
            return
        
        # 创建项目根节点
        project_item = QTreeWidgetItem(self)
        project_item.setText(0, f"📁 {project.project_name}")
        project_item.setData(0, Qt.UserRole, {"type": "project", "id": project.project_id})
        
        # 添加集节点
        for episode in project.episodes:
            episode_item = QTreeWidgetItem(project_item)
            episode_item.setText(0, f"📺 第{episode.episode_number}集 - {episode.episode_name}")
            episode_item.setData(0, Qt.UserRole, {"type": "episode", "id": episode.episode_id})
            
            # 添加场节点
            for scene in episode.scenes:
                scene_item = QTreeWidgetItem(episode_item)
                scene_item.setText(0, f"🎬 场{scene.scene_number} - {scene.scene_name}")
                scene_item.setData(0, Qt.UserRole, {"type": "scene", "id": scene.scene_id})
                
                # 添加镜头节点
                for shot in scene.shots:
                    shot_item = QTreeWidgetItem(scene_item)
                    shot_item.setText(0, f"📹 镜头{shot.shot_number} - {shot.shot_name}")
                    shot_item.setData(0, Qt.UserRole, {"type": "shot", "id": shot.shot_id})
                    
                    # 添加阶段节点
                    stages = {}
                    for task in shot.tasks:
                        stage_name = task.stage.value
                        if stage_name not in stages:
                            stage_item = QTreeWidgetItem(shot_item)
                            stage_item.setText(0, f"⚙️ {stage_name}")
                            stage_item.setData(0, Qt.UserRole, {
                                "type": "stage", 
                                "id": f"{shot.shot_id}_{task.stage.name}",
                                "stage": task.stage
                            })
                            stages[stage_name] = stage_item
        
        # 展开项目根节点
        project_item.setExpanded(True)
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """处理项目点击事件"""
        data = item.data(0, Qt.UserRole)
        if data:
            self.item_selected.emit(data["type"], data["id"])


class TaskTableWidget(QTableWidget):
    """任务表格组件"""
    
    # 信号
    task_selected = Signal(str)  # task_id
    task_status_changed = Signal(str, object)  # (task_id, new_status)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.tasks = []
    
    def setup_ui(self):
        """设置UI"""
        # 设置列
        headers = ["任务名称", "阶段", "状态", "负责人", "优先级", "进度", "创建时间", "截止时间"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # 设置表格属性
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # 调整列宽
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 任务名称列自适应
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        
        # 连接信号
        self.itemClicked.connect(self._on_item_clicked)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # 设置样式
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                gridline-color: #eee;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
    
    def load_tasks(self, tasks: List[Task]):
        """加载任务数据"""
        self.tasks = tasks
        self.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            # 任务名称
            name_item = QTableWidgetItem(task.task_name)
            name_item.setData(Qt.UserRole, task.task_id)
            self.setItem(row, 0, name_item)
            
            # 阶段
            stage_item = QTableWidgetItem(task.stage.value)
            self.setItem(row, 1, stage_item)
            
            # 状态
            status_item = QTableWidgetItem(task.status.value)
            status_item = self._style_status_item(status_item, task.status)
            self.setItem(row, 2, status_item)
            
            # 负责人
            assignee_item = QTableWidgetItem(task.assignee)
            self.setItem(row, 3, assignee_item)
            
            # 优先级
            priority_item = QTableWidgetItem(f"优先级 {task.priority}")
            priority_item = self._style_priority_item(priority_item, task.priority)
            self.setItem(row, 4, priority_item)
            
            # 进度
            progress_item = QTableWidgetItem(f"{task.progress:.1%}")
            self.setItem(row, 5, progress_item)
            
            # 创建时间
            created_item = QTableWidgetItem(task.created_time.strftime("%Y-%m-%d"))
            self.setItem(row, 6, created_item)
            
            # 截止时间
            due_text = task.due_time.strftime("%Y-%m-%d") if task.due_time else "未设置"
            due_item = QTableWidgetItem(due_text)
            self.setItem(row, 7, due_item)
    
    def _style_status_item(self, item: QTableWidgetItem, status: TaskStatus) -> QTableWidgetItem:
        """设置状态项样式"""
        color_map = {
            TaskStatus.PENDING: "#9E9E9E",
            TaskStatus.IN_PROGRESS: "#FF9800",
            TaskStatus.REVIEW: "#2196F3",
            TaskStatus.APPROVED: "#4CAF50",
            TaskStatus.REJECTED: "#F44336",
            TaskStatus.COMPLETED: "#4CAF50"
        }
        
        color = color_map.get(status, "#000000")
        item.setForeground(color)
        return item
    
    def _style_priority_item(self, item: QTableWidgetItem, priority: int) -> QTableWidgetItem:
        """设置优先级项样式"""
        if priority >= 4:
            item.setForeground("#F44336")  # 高优先级红色
        elif priority >= 3:
            item.setForeground("#FF9800")  # 中优先级橙色
        else:
            item.setForeground("#4CAF50")  # 低优先级绿色
        
        return item
    
    def _on_item_clicked(self, item: QTableWidgetItem):
        """处理项目点击事件"""
        if item.column() == 0:  # 点击任务名称列
            task_id = item.data(Qt.UserRole)
            if task_id:
                self.task_selected.emit(task_id)
    
    def _on_item_double_clicked(self, item: QTableWidgetItem):
        """处理项目双击事件"""
        # 双击可以打开任务详情对话框
        if item.column() == 0:
            task_id = item.data(Qt.UserRole)
            if task_id:
                # 这里可以打开任务详情对话框
                print(f"打开任务详情: {task_id}")
    
    def filter_tasks(self, filters: Dict[str, Any]):
        """根据过滤条件筛选任务"""
        filtered_tasks = []
        
        for task in self.tasks:
            # 阶段过滤
            if filters.get("stage") and task.stage != filters["stage"]:
                continue
            
            # 状态过滤
            if filters.get("status") and task.status != filters["status"]:
                continue
            
            # 优先级过滤
            if filters.get("priority") and task.priority != filters["priority"]:
                continue
            
            # 我的任务过滤（这里简化处理，实际应该根据当前用户判断）
            if filters.get("my_tasks_only") and task.assignee != "当前用户":
                continue
            
            filtered_tasks.append(task)
        
        self.load_tasks(filtered_tasks)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.current_project = None
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_tool_bar()
        self.setup_status_bar()
    
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("三维影视制作管理系统")
        self.setMinimumSize(1200, 800)
        
        # 创建中央部件
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
        splitter.setSizes([300, 900])
    
    def _create_left_panel(self) -> QWidget:
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 项目选择区域
        project_group = QGroupBox("项目选择")
        project_layout = QVBoxLayout(project_group)
        
        # 项目下拉框
        self.project_combo = QComboBox()
        self.project_combo.currentTextChanged.connect(self._on_project_changed)
        project_layout.addWidget(self.project_combo)
        
        # 刷新按钮
        refresh_button = QPushButton("刷新项目列表")
        refresh_button.clicked.connect(self._refresh_projects)
        project_layout.addWidget(refresh_button)
        
        layout.addWidget(project_group)
        
        # 项目树
        tree_group = QGroupBox("项目结构")
        tree_layout = QVBoxLayout(tree_group)
        
        self.project_tree = ProjectTreeWidget()
        self.project_tree.item_selected.connect(self._on_tree_item_selected)
        tree_layout.addWidget(self.project_tree)
        
        layout.addWidget(tree_group)
        
        # 过滤器
        self.filter_widget = FilterWidget()
        self.filter_widget.filter_changed.connect(self._on_filter_changed)
        layout.addWidget(self.filter_widget)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """创建右侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # 任务列表选项卡
        task_tab = QWidget()
        task_layout = QVBoxLayout(task_tab)
        
        # 任务操作按钮
        task_buttons_layout = QHBoxLayout()
        
        self.load_tasks_button = QPushButton("加载任务")
        self.load_tasks_button.clicked.connect(self._load_tasks)
        task_buttons_layout.addWidget(self.load_tasks_button)
        
        self.refresh_tasks_button = QPushButton("刷新任务")
        self.refresh_tasks_button.clicked.connect(self._refresh_tasks)
        task_buttons_layout.addWidget(self.refresh_tasks_button)
        
        self.export_tasks_button = QPushButton("导出任务")
        self.export_tasks_button.clicked.connect(self._export_tasks)
        task_buttons_layout.addWidget(self.export_tasks_button)
        
        task_buttons_layout.addStretch()
        task_layout.addLayout(task_buttons_layout)
        
        # 任务表格
        self.task_table = TaskTableWidget()
        self.task_table.task_selected.connect(self._on_task_selected)
        task_layout.addWidget(self.task_table)
        
        tab_widget.addTab(task_tab, "任务列表")
        
        # 统计信息选项卡
        self.statistics_widget = ProjectStatisticsWidget()
        tab_widget.addTab(self.statistics_widget, "项目统计")
        
        return panel
    
    def setup_menu_bar(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        # 打开项目
        open_action = QAction("打开项目", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_project)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图")
        
        # 刷新
        refresh_action = QAction("刷新", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_all)
        view_menu.addAction(refresh_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具")
        
        # 生成报告
        report_action = QAction("生成项目报告", self)
        report_action.triggered.connect(self._generate_project_report)
        tools_menu.addAction(report_action)
        
        # 批量更新任务
        batch_update_action = QAction("批量更新任务", self)
        batch_update_action.triggered.connect(self._batch_update_tasks)
        tools_menu.addAction(batch_update_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def setup_tool_bar(self):
        """设置工具栏"""
        toolbar = self.addToolBar("主工具栏")
        
        # 刷新按钮
        refresh_action = QAction("🔄 刷新", self)
        refresh_action.triggered.connect(self._refresh_all)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # 加载任务按钮
        load_tasks_action = QAction("📋 加载任务", self)
        load_tasks_action.triggered.connect(self._load_tasks)
        toolbar.addAction(load_tasks_action)
        
        # 生成报告按钮
        report_action = QAction("📊 生成报告", self)
        report_action.triggered.connect(self._generate_project_report)
        toolbar.addAction(report_action)
    
    def setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)
        
        # 项目信息标签
        self.project_info_label = QLabel("未选择项目")
        self.status_bar.addPermanentWidget(self.project_info_label)
    
    def set_status_message(self, message: str):
        """设置状态消息"""
        self.status_label.setText(message)
        self.status_bar.showMessage(message, 3000)
    
    def load_project(self, project: Project):
        """加载项目"""
        self.current_project = project
        self.project_tree.load_project(project)
        
        # 更新项目信息
        if project:
            self.project_info_label.setText(f"项目: {project.project_name}")
            self.statistics_widget.update_statistics(project.get_project_statistics())
        else:
            self.project_info_label.setText("未选择项目")
    
    def load_tasks(self, tasks: List[Task]):
        """加载任务列表"""
        self.task_table.load_tasks(tasks)
        self.set_status_message(f"已加载 {len(tasks)} 个任务")
    
    # 事件处理方法
    def _on_project_changed(self, project_name: str):
        """项目选择变化"""
        # 这里应该通过控制器加载项目详情
        print(f"选择项目: {project_name}")
    
    def _on_tree_item_selected(self, item_type: str, item_id: str):
        """树形项目选择"""
        print(f"选择了 {item_type}: {item_id}")
        # 这里应该通过控制器加载对应的任务
    
    def _on_task_selected(self, task_id: str):
        """任务选择"""
        print(f"选择任务: {task_id}")
        # 这里可以显示任务详情
    
    def _on_filter_changed(self, filters: Dict[str, Any]):
        """过滤条件变化"""
        self.task_table.filter_tasks(filters)
    
    def _refresh_projects(self):
        """刷新项目列表"""
        self.set_status_message("正在刷新项目列表...")
        # 这里应该通过控制器刷新项目列表
    
    def _load_tasks(self):
        """加载任务"""
        self.set_status_message("正在加载任务...")
        # 这里应该通过控制器加载任务
    
    def _refresh_tasks(self):
        """刷新任务"""
        self.set_status_message("正在刷新任务...")
        # 这里应该通过控制器刷新任务
    
    def _export_tasks(self):
        """导出任务"""
        self.set_status_message("正在导出任务...")
        # 这里可以实现任务导出功能
    
    def _refresh_all(self):
        """刷新所有数据"""
        self.set_status_message("正在刷新所有数据...")
        # 这里应该通过控制器刷新所有数据
    
    def _open_project(self):
        """打开项目"""
        # 这里可以实现项目选择对话框
        print("打开项目对话框")
    
    def _generate_project_report(self):
        """生成项目报告"""
        if not self.current_project:
            QMessageBox.warning(self, "警告", "请先选择一个项目")
            return
        
        report_dialog = ReportGenerator.generate_project_report(self.current_project)
        report_dialog.exec()
    
    def _batch_update_tasks(self):
        """批量更新任务"""
        # 这里可以实现批量更新任务的对话框
        print("批量更新任务")
    
    def _show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于", 
                         "三维影视制作管理系统 v1.0\n\n"
                         "基于PySide6的MVC架构桌面应用程序\n"
                         "用于管理三维影视制作流程中的项目、任务和文件")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 这里可以添加关闭前的清理工作
        event.accept()