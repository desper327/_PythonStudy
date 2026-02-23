"""
主控制器
负责协调视图和模型之间的交互，处理业务逻辑
"""
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QApplication

from film_production_manager.models.api_client import APIClient
from film_production_manager.models.data_models import Project, Task, ProductionStage, TaskStatus
from film_production_manager.utils.thread_workers import ThreadManager
from film_production_manager.utils.common_widgets import ProgressWidget, ReportGenerator
from film_production_manager.views.main_window import MainWindow


class MainController(QObject):
    """主控制器类"""
    
    # 信号
    project_loaded = Signal(object)  # 项目加载完成
    tasks_loaded = Signal(list)  # 任务加载完成
    error_occurred = Signal(str)  # 错误发生
    status_changed = Signal(str)  # 状态变化
    
    def __init__(self, api_base_url: str = "http://localhost:8000/api"):
        super().__init__()
        
        # 初始化组件
        self.api_client = APIClient(api_base_url)
        self.thread_manager = ThreadManager()
        self.thread_manager.set_api_client(self.api_client)
        
        # 数据存储
        self.current_project = None
        self.projects_list = []
        self.current_tasks = []
        
        # UI组件
        self.main_window = None
        self.progress_widget = None
        
        # 当前选择的层级信息
        self.selected_project_id = None
        self.selected_episode_id = None
        self.selected_scene_id = None
        self.selected_shot_id = None
        self.selected_stage = None
    
    def initialize(self):
        """初始化控制器"""
        # 创建主窗口
        self.main_window = MainWindow()
        
        # 连接信号
        self._connect_signals()
        
        # 初始化数据
        self.load_projects()
        
        return self.main_window
    
    def _connect_signals(self):
        """连接信号和槽"""
        if not self.main_window:
            return
        
        # 连接主窗口信号
        self.main_window.project_tree.item_selected.connect(self._on_tree_item_selected)
        self.main_window.task_table.task_selected.connect(self._on_task_selected)
        self.main_window.filter_widget.filter_changed.connect(self._on_filter_changed)
        
        # 连接控制器信号到主窗口
        self.project_loaded.connect(self.main_window.load_project)
        self.tasks_loaded.connect(self.main_window.load_tasks)
        self.status_changed.connect(self.main_window.set_status_message)
        self.error_occurred.connect(self._show_error_message)
    
    def set_api_auth_token(self, token: str):
        """设置API认证令牌"""
        self.api_client.set_auth_token(token)
    
    def load_projects(self):
        """加载项目列表"""
        self.status_changed.emit("正在加载项目列表...")
        
        # 启动项目数据工作器
        worker = self.thread_manager.start_project_data_worker("load_projects")
        
        # 连接工作器信号
        worker.projects_loaded.connect(self._on_projects_loaded)
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        worker.status_changed.connect(self.status_changed.emit)
        
        # 设置加载任务
        worker.load_projects()
    
    def load_project_details(self, project_id: str):
        """加载项目详情"""
        self.status_changed.emit(f"正在加载项目详情...")
        
        # 启动项目详情工作器
        worker = self.thread_manager.start_project_data_worker("load_project_details")
        
        # 连接工作器信号
        worker.project_details_loaded.connect(self._on_project_details_loaded)
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        worker.status_changed.connect(self.status_changed.emit)
        
        # 设置加载任务
        worker.load_project_details(project_id)
    
    def load_tasks(self, project_id: str = None, episode_id: str = None, 
                   scene_id: str = None, shot_id: str = None, 
                   stage: ProductionStage = None):
        """加载任务列表"""
        # 使用当前选择的层级信息
        project_id = project_id or self.selected_project_id
        episode_id = episode_id or self.selected_episode_id
        scene_id = scene_id or self.selected_scene_id
        shot_id = shot_id or self.selected_shot_id
        stage = stage or self.selected_stage
        
        if not project_id:
            self.error_occurred.emit("请先选择一个项目")
            return
        
        self.status_changed.emit("正在加载任务列表...")
        
        # 启动任务数据工作器
        worker = self.thread_manager.start_task_data_worker("load_tasks")
        
        # 连接工作器信号
        worker.tasks_loaded.connect(self._on_tasks_loaded)
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        worker.status_changed.connect(self.status_changed.emit)
        
        # 设置加载参数
        worker.load_tasks(project_id, episode_id, scene_id, shot_id, stage)
    
    def update_task_status(self, task_id: str, status: TaskStatus, progress: float = None):
        """更新任务状态"""
        self.status_changed.emit(f"正在更新任务状态...")
        
        # 启动批量任务工作器
        worker = self.thread_manager.start_batch_task_worker("update_task_status")
        
        # 连接工作器信号
        worker.task_completed.connect(self._on_task_update_completed)
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        worker.status_changed.connect(self.status_changed.emit)
        
        # 设置更新任务
        task_updates = [{
            'task_id': task_id,
            'status': status,
            'progress': progress
        }]
        worker.update_task_statuses(task_updates)
    
    def batch_update_tasks(self, task_updates: List[Dict[str, Any]]):
        """批量更新任务"""
        if not task_updates:
            return
        
        self.status_changed.emit(f"正在批量更新 {len(task_updates)} 个任务...")
        
        # 启动批量任务工作器
        worker = self.thread_manager.start_batch_task_worker("batch_update_tasks")
        
        # 连接工作器信号
        worker.batch_completed.connect(self._on_batch_update_completed)
        worker.task_completed.connect(self._on_task_update_completed)
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        worker.status_changed.connect(self.status_changed.emit)
        
        # 设置批量更新任务
        worker.update_task_statuses(task_updates)
    
    def process_files(self, file_ids: List[str], process_function=None):
        """处理文件"""
        if not file_ids:
            return
        
        self.status_changed.emit(f"正在处理 {len(file_ids)} 个文件...")
        
        # 启动文件处理工作器
        worker = self.thread_manager.start_file_process_worker("process_files")
        
        # 连接工作器信号
        worker.all_files_processed.connect(self._on_files_processed)
        worker.file_processed.connect(self._on_file_processed)
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        worker.status_changed.connect(self.status_changed.emit)
        
        # 设置文件处理任务
        worker.process_files(file_ids, process_function)
    
    def generate_project_report(self):
        """生成项目报告"""
        if not self.current_project:
            self.error_occurred.emit("请先选择一个项目")
            return
        
        try:
            report_dialog = ReportGenerator.generate_project_report(self.current_project)
            report_dialog.exec()
        except Exception as e:
            self.error_occurred.emit(f"生成报告失败: {str(e)}")
    
    def generate_task_report(self):
        """生成任务报告"""
        if not self.current_tasks:
            self.error_occurred.emit("没有可用的任务数据")
            return
        
        try:
            report_dialog = ReportGenerator.generate_task_report(self.current_tasks)
            report_dialog.exec()
        except Exception as e:
            self.error_occurred.emit(f"生成任务报告失败: {str(e)}")
    
    def refresh_all_data(self):
        """刷新所有数据"""
        self.load_projects()
        if self.current_project:
            self.load_project_details(self.current_project.project_id)
        if self.selected_project_id:
            self.load_tasks()
    
    def cancel_all_operations(self):
        """取消所有正在进行的操作"""
        self.thread_manager.stop_all_workers()
        self.status_changed.emit("已取消所有操作")
    
    # 事件处理方法
    def _on_projects_loaded(self, projects: List[Project]):
        """项目列表加载完成"""
        self.projects_list = projects
        
        # 更新主窗口的项目下拉框
        if self.main_window:
            self.main_window.project_combo.clear()
            for project in projects:
                self.main_window.project_combo.addItem(
                    project.project_name, 
                    project.project_id
                )
        
        self.status_changed.emit(f"已加载 {len(projects)} 个项目")
    
    def _on_project_details_loaded(self, project: Project):
        """项目详情加载完成"""
        self.current_project = project
        self.selected_project_id = project.project_id if project else None
        
        # 发射信号更新UI
        self.project_loaded.emit(project)
        
        if project:
            self.status_changed.emit(f"项目 '{project.project_name}' 加载完成")
        else:
            self.status_changed.emit("项目加载失败")
    
    def _on_tasks_loaded(self, tasks: List[Task]):
        """任务列表加载完成"""
        self.current_tasks = tasks
        
        # 发射信号更新UI
        self.tasks_loaded.emit(tasks)
        
        self.status_changed.emit(f"已加载 {len(tasks)} 个任务")
    
    def _on_task_update_completed(self, task_id: str, success: bool):
        """单个任务更新完成"""
        if success:
            print(f"任务 {task_id} 更新成功")
        else:
            print(f"任务 {task_id} 更新失败")
    
    def _on_batch_update_completed(self, stats: Dict[str, Any]):
        """批量更新完成"""
        total = stats.get("total", 0)
        success = stats.get("success", 0)
        failed = stats.get("failed", 0)
        
        message = f"批量更新完成: 成功 {success}/{total}, 失败 {failed}"
        self.status_changed.emit(message)
        
        # 刷新任务列表
        if success > 0:
            self.load_tasks()
    
    def _on_file_processed(self, processed_file: Dict[str, Any]):
        """单个文件处理完成"""
        file_name = processed_file.get("file_name", "未知文件")
        print(f"文件 {file_name} 处理完成")
    
    def _on_files_processed(self, processed_files: List[Dict[str, Any]]):
        """所有文件处理完成"""
        self.status_changed.emit(f"已处理 {len(processed_files)} 个文件")
    
    def _on_worker_error(self, error_message: str):
        """工作器错误处理"""
        self.error_occurred.emit(error_message)
    
    def _on_worker_progress(self, progress: int):
        """工作器进度更新"""
        # 这里可以更新进度条
        pass
    
    def _on_tree_item_selected(self, item_type: str, item_id: str):
        """树形项目选择处理"""
        # 重置选择状态
        self.selected_episode_id = None
        self.selected_scene_id = None
        self.selected_shot_id = None
        self.selected_stage = None
        
        if item_type == "project":
            self.selected_project_id = item_id
            # 加载项目详情（如果还没有加载）
            if not self.current_project or self.current_project.project_id != item_id:
                self.load_project_details(item_id)
        
        elif item_type == "episode":
            self.selected_episode_id = item_id
        
        elif item_type == "scene":
            self.selected_scene_id = item_id
        
        elif item_type == "shot":
            self.selected_shot_id = item_id
        
        elif item_type == "stage":
            # 解析阶段信息
            if "_" in item_id:
                shot_id, stage_name = item_id.rsplit("_", 1)
                self.selected_shot_id = shot_id
                try:
                    self.selected_stage = ProductionStage[stage_name]
                except KeyError:
                    pass
        
        # 自动加载对应的任务
        self.load_tasks()
    
    def _on_task_selected(self, task_id: str):
        """任务选择处理"""
        # 查找选中的任务
        selected_task = None
        for task in self.current_tasks:
            if task.task_id == task_id:
                selected_task = task
                break
        
        if selected_task:
            print(f"选中任务: {selected_task.task_name}")
            # 这里可以显示任务详情或执行其他操作
    
    def _on_filter_changed(self, filters: Dict[str, Any]):
        """过滤条件变化处理"""
        # 过滤逻辑已在TaskTableWidget中实现
        # 这里可以添加额外的处理逻辑
        pass
    
    def _show_error_message(self, message: str):
        """显示错误消息"""
        if self.main_window:
            QMessageBox.critical(self.main_window, "错误", message)
    
    def cleanup(self):
        """清理资源"""
        # 停止所有工作器
        self.thread_manager.stop_all_workers()
        
        # 清理数据
        self.current_project = None
        self.projects_list.clear()
        self.current_tasks.clear()