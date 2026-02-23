"""
重构后的主控制器
简化的主控制器，将复杂逻辑委托给子控制器
"""
from typing import Dict, Any, Optional
from PySide6.QtCore import QTimer
from beartype import beartype
from .base_controller import BaseController, ControllerManager
from .dialog_controller import DialogController
from .task_controller import TaskController
from views.main_window import MainWindow
from services.user_service import UserService
from services.data_service import DataService
from repositories.api_client import ApiClient
from repositories.database import DatabaseManager
from workers.async_worker import AsyncTaskManager
from workers.thread_worker import ThreadPool
from models.base_model import UIState
from config.settings import settings


class MainController(BaseController):
    """
    重构后的主控制器类
    负责协调整个应用程序，将具体逻辑委托给子控制器
    """
    
    @beartype
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 主窗口
        self.main_window: Optional[MainWindow] = None
        
        # 基础组件
        self.api_client: Optional[ApiClient] = None
        self.db_manager: Optional[DatabaseManager] = None
        self.user_service: Optional[UserService] = None
        self.data_service: Optional[DataService] = None
        self.async_task_manager: Optional[AsyncTaskManager] = None
        self.thread_pool: Optional[ThreadPool] = None
        
        # 子控制器管理
        self.controller_manager = ControllerManager(self)
        self.dialog_controller: Optional[DialogController] = None
        self.task_controller: Optional[TaskController] = None
        
        # UI状态
        self.ui_state = UIState()
        
        # 状态更新定时器
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start(5000)
    
    @beartype
    async def initialize(self) -> None:
        """异步初始化主控制器"""
        try:
            await self._initialize_infrastructure()
            self._initialize_services()
            self._initialize_workers()
            await self._initialize_sub_controllers()
            self.log_message("主控制器初始化完成")
        except Exception as e:
            self.log_message(f"主控制器初始化失败: {e}", is_error=True)
            raise
    
    @beartype
    async def _initialize_infrastructure(self) -> None:
        """初始化基础设施"""
        self.db_manager = DatabaseManager()
        await self.db_manager.initialize()
        await self.db_manager.create_tables()
        
        self.api_client = ApiClient(
            base_url=settings.app.api_base_url,
            timeout=settings.app.api_timeout
        )
        await self.api_client.connect()
    
    @beartype
    def _initialize_services(self) -> None:
        """初始化服务层"""
        self.user_service = UserService(
            self.api_client, self.db_manager, self._on_service_progress
        )
        self.data_service = DataService(self._on_service_progress)
    
    @beartype
    def _initialize_workers(self) -> None:
        """初始化工作器"""
        self.async_task_manager = AsyncTaskManager(
            max_concurrent_tasks=settings.app.max_async_tasks
        )
        self.thread_pool = ThreadPool(
            max_threads=settings.app.max_thread_tasks
        )
    
    @beartype
    async def _initialize_sub_controllers(self) -> None:
        """初始化子控制器"""
        self.dialog_controller = DialogController(
            self.user_service, self.data_service,
            self.async_task_manager, self.thread_pool, self
        )
        
        self.task_controller = TaskController(
            self.user_service, self.data_service,
            self.async_task_manager, self.thread_pool, self
        )
        
        self.controller_manager.register_controller("dialog", self.dialog_controller)
        self.controller_manager.register_controller("task", self.task_controller)
        
        await self.controller_manager.initialize_all()
    
    @beartype
    def setup_connections(self) -> None:
        """设置信号连接"""
        if self.main_window:
            self._connect_main_window_signals()
    
    @beartype
    def set_main_window(self, main_window: MainWindow) -> None:
        """设置主窗口"""
        self.main_window = main_window
        self.setup_connections()
        self.main_window.update_ui_state(self.ui_state)
        self.main_window.add_log_message("应用程序已启动")
    
    @beartype
    def _connect_main_window_signals(self) -> None:
        """连接主窗口信号"""
        if not self.main_window:
            return
        
        self.main_window.user_action_triggered.connect(self._handle_user_action)
        self.main_window.async_task_requested.connect(self._handle_async_task_request)
        self.main_window.thread_task_requested.connect(self._handle_thread_task_request)
        self.main_window.dialog_requested.connect(self._handle_dialog_request)
    
    # 简化的事件处理方法 - 委托给子控制器
    
    @beartype
    def _handle_user_action(self, action_name: str, data: Dict[str, Any]) -> None:
        """处理用户操作 - 委托给相应的子控制器"""
        try:
            if action_name in ["user_management", "data_analysis", "generate_report", "export_data"]:
                # 委托给任务控制器
                if self.task_controller:
                    task_type = self._map_action_to_task_type(action_name)
                    self.task_controller.submit_async_task(task_type, data)
            elif action_name in ["cancel_task", "clear_completed_tasks"]:
                # 任务管理操作
                if self.task_controller:
                    if action_name == "cancel_task":
                        self.task_controller.cancel_task(data.get("task_id", ""))
                    else:
                        self.task_controller.clear_completed_tasks()
            elif action_name == "application_closing":
                self._handle_application_closing()
            else:
                self.log_message(f"未知操作: {action_name}")
        except Exception as e:
            self.log_message(f"处理用户操作失败: {e}", is_error=True)
    
    @beartype
    def _handle_async_task_request(self, task_id: str, data: Dict[str, Any]) -> None:
        """处理异步任务请求 - 委托给任务控制器"""
        if self.task_controller:
            task_type = data.get("task_type", "unknown")
            self.task_controller.submit_async_task(task_type, data.get("parameters", {}))
    
    @beartype
    def _handle_thread_task_request(self, task_id: str, data: Dict[str, Any]) -> None:
        """处理线程任务请求 - 委托给任务控制器"""
        if self.task_controller:
            task_type = data.get("task_type", "unknown")
            self.task_controller.submit_thread_task(task_type, data.get("parameters", {}))
    
    @beartype
    def _handle_dialog_request(self, dialog_type: str, data: Dict[str, Any]) -> None:
        """处理对话框请求 - 委托给对话框控制器"""
        if self.dialog_controller:
            if dialog_type == "feature_dialog":
                self.dialog_controller.show_feature_dialog(self.main_window, data)
    
    @beartype
    def _map_action_to_task_type(self, action_name: str) -> str:
        """将操作名称映射到任务类型"""
        mapping = {
            "user_management": "load_users",
            "data_analysis": "trend_analysis",
            "generate_report": "user_report",
            "export_data": "export_data"
        }
        return mapping.get(action_name, "unknown")
    
    @beartype
    def _handle_application_closing(self) -> None:
        """处理应用程序关闭"""
        self.log_message("应用程序正在关闭...")
        if self.task_controller:
            self.task_controller.cancel_all_tasks()
    
    @beartype
    def _on_service_progress(self, progress: float, message: str) -> None:
        """服务层进度回调"""
        if self.main_window:
            self.main_window.update_progress(progress, message)
            if progress > 0:
                self.main_window.show_loading(True, message)
    
    @beartype
    def _update_status(self) -> None:
        """定期更新状态"""
        if self.main_window and self.task_controller:
            active_count = self.task_controller.get_active_task_count()
            self.main_window.update_task_count(active_count)
            
            if active_count > 0:
                self.ui_state.set_status(f"正在执行 {active_count} 个任务")
            else:
                self.ui_state.set_status("就绪")
            
            self.main_window.update_ui_state(self.ui_state)
    
    @beartype
    async def cleanup(self) -> None:
        """清理主控制器资源"""
        try:
            self.status_timer.stop()
            
            # 清理子控制器
            await self.controller_manager.cleanup_all()
            
            # 清理基础组件
            if self.api_client:
                await self.api_client.disconnect()
            if self.db_manager:
                await self.db_manager.cleanup()
            
            await super().cleanup()
            self.log_message("主控制器清理完成")
        except Exception as e:
            self.log_message(f"主控制器清理失败: {e}", is_error=True)
