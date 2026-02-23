"""
对话框控制器
专门处理各种对话框的交互逻辑
"""
from typing import Dict, Any, Optional
from beartype import beartype
from .base_controller import BaseController
from views.dialogs.feature_dialog import FeatureDialog
from services.user_service import UserService
from services.data_service import DataService
from workers.async_worker import AsyncTaskManager
from workers.thread_worker import ThreadPool


class DialogController(BaseController):
    """
    对话框控制器类
    负责管理所有对话框的创建、显示和交互
    """
    
    @beartype
    def __init__(self, 
                 user_service: UserService,
                 data_service: DataService,
                 async_task_manager: AsyncTaskManager,
                 thread_pool: ThreadPool,
                 parent=None):
        """
        初始化对话框控制器
        
        Args:
            user_service: 用户服务
            data_service: 数据服务
            async_task_manager: 异步任务管理器
            thread_pool: 线程池
            parent: 父对象
        """
        super().__init__(parent)
        
        # 服务层引用
        self.user_service = user_service
        self.data_service = data_service
        self.async_task_manager = async_task_manager
        self.thread_pool = thread_pool
        
        # 对话框实例
        self.feature_dialog: Optional[FeatureDialog] = None
        
        # 活动对话框跟踪
        self.active_dialogs: Dict[str, Any] = {}
    
    @beartype
    async def initialize(self) -> None:
        """
        异步初始化对话框控制器
        """
        try:
            # 这里可以进行一些异步初始化操作
            self.log_message("对话框控制器初始化完成")
        except Exception as e:
            self.log_message(f"对话框控制器初始化失败: {e}", is_error=True)
            raise
    
    @beartype
    def setup_connections(self) -> None:
        """
        设置信号连接
        """
        # 对话框的信号连接会在创建时进行
        pass
    
    @beartype
    def show_feature_dialog(self, parent_window=None, data: Optional[Dict[str, Any]] = None) -> FeatureDialog:
        """
        显示功能对话框
        
        Args:
            parent_window: 父窗口
            data: 对话框数据
            
        Returns:
            FeatureDialog: 功能对话框实例
        """
        try:
            # 如果对话框不存在，创建新的
            if self.feature_dialog is None:
                self.feature_dialog = FeatureDialog(parent_window)
                self._connect_feature_dialog_signals()
                self.active_dialogs["feature"] = self.feature_dialog
            
            # 设置对话框属性
            if data:
                title = data.get("title", "功能对话框")
                modal = data.get("modal", True)
                
                self.feature_dialog.setWindowTitle(title)
                self.feature_dialog.setModal(modal)
            
            # 显示对话框
            self.feature_dialog.show()
            self.feature_dialog.raise_()
            self.feature_dialog.activateWindow()
            
            self.log_message("功能对话框已显示")
            return self.feature_dialog
            
        except Exception as e:
            self.log_message(f"显示功能对话框失败: {e}", is_error=True)
            raise
    
    @beartype
    def _connect_feature_dialog_signals(self) -> None:
        """
        连接功能对话框信号
        """
        if not self.feature_dialog:
            return
        
        # 连接功能操作信号
        self.feature_dialog.feature_action_triggered.connect(self._handle_feature_action)
        self.feature_dialog.async_task_requested.connect(self._handle_async_task_request)
        self.feature_dialog.thread_task_requested.connect(self._handle_thread_task_request)
        
        # 连接对话框关闭信号
        self.feature_dialog.finished.connect(self._on_feature_dialog_closed)
    
    @beartype
    def _handle_feature_action(self, action_name: str, data: Dict[str, Any]) -> None:
        """
        处理功能对话框的操作
        
        Args:
            action_name: 操作名称
            data: 操作数据
        """
        try:
            if action_name == "create_user":
                self._handle_create_user(data)
            elif action_name == "load_users":
                self._handle_load_users(data)
            elif action_name == "save_settings":
                self._handle_save_settings(data)
            elif action_name == "import_data":
                self._handle_import_data(data)
            else:
                self.log_message(f"未知功能操作: {action_name}")
                
        except Exception as e:
            self.log_message(f"处理功能操作失败: {e}", is_error=True)
            if self.feature_dialog:
                self.feature_dialog.show_result_message("错误", f"操作失败: {str(e)}", is_error=True)
    
    @beartype
    def _handle_async_task_request(self, task_id: str, data: Dict[str, Any]) -> None:
        """
        处理异步任务请求
        
        Args:
            task_id: 任务ID
            data: 任务数据
        """
        try:
            # 根据任务类型创建协程
            if "generate_user_report" in task_id:
                coroutine = self.user_service.generate_user_report()
            elif "batch_process_users" in task_id:
                user_ids = data.get("user_ids", [])
                operation = data.get("operation", "activate")
                coroutine = self.user_service.process_user_batch(user_ids, operation)
            elif "process_large_dataset" in task_id:
                coroutine = self.data_service.process_large_dataset(
                    data_size=data.get("data_size", 1000),
                    processing_delay=data.get("processing_delay", 0.01)
                )
            elif "analyze_trends" in task_id:
                coroutine = self.data_service.analyze_trends([])
            elif "export_data" in task_id:
                format_type = data.get("format", "json")
                coroutine = self.data_service.export_data([], format_type)
            else:
                self.log_message(f"未知异步任务类型: {task_id}")
                return
            
            # 提交异步任务
            self.async_task_manager.queue_task(
                task_id=task_id,
                coroutine=coroutine,
                priority=1,
                progress_callback=self._on_task_progress
            )
            
            self.log_message(f"异步任务已提交: {task_id}")
            
        except Exception as e:
            self.log_message(f"提交异步任务失败: {e}", is_error=True)
    
    @beartype
    def _handle_thread_task_request(self, task_id: str, data: Dict[str, Any]) -> None:
        """
        处理线程任务请求
        
        Args:
            task_id: 任务ID
            data: 任务数据
        """
        try:
            from workers.thread_worker import example_long_running_task, example_data_processing_task
            
            # 根据任务类型选择目标函数
            if "long_running" in task_id:
                target_function = example_long_running_task
                kwargs = {
                    "duration": data.get("duration", 5.0),
                    "steps": data.get("steps", 10)
                }
            elif "data_processing" in task_id:
                target_function = example_data_processing_task
                kwargs = {
                    "data_size": data.get("data_size", 1000),
                    "processing_delay": data.get("processing_delay", 0.001)
                }
            else:
                self.log_message(f"未知线程任务类型: {task_id}")
                return
            
            # 提交线程任务
            success = self.thread_pool.submit_task(
                task_id=task_id,
                target_function=target_function,
                kwargs=kwargs,
                priority=1,
                progress_callback=self._on_task_progress
            )
            
            if success:
                self.log_message(f"线程任务已提交: {task_id}")
            else:
                self.log_message(f"线程任务提交失败: {task_id}", is_error=True)
                
        except Exception as e:
            self.log_message(f"提交线程任务失败: {e}", is_error=True)
    
    @beartype
    def _handle_create_user(self, data: Dict[str, Any]) -> None:
        """
        处理创建用户操作
        
        Args:
            data: 用户数据
        """
        try:
            # 启动异步创建用户任务
            task_id = f"create_user_{id(self)}"
            coroutine = self.user_service.create_user(data)
            
            self.async_task_manager.queue_task(
                task_id=task_id,
                coroutine=coroutine,
                priority=2,
                progress_callback=self._on_task_progress
            )
            
            self.log_message("创建用户任务已启动")
            
        except Exception as e:
            self.log_message(f"创建用户失败: {e}", is_error=True)
            if self.feature_dialog:
                self.feature_dialog.show_result_message("错误", f"创建用户失败: {str(e)}", is_error=True)
    
    @beartype
    def _handle_load_users(self, data: Dict[str, Any]) -> None:
        """
        处理加载用户操作
        
        Args:
            data: 加载参数
        """
        try:
            sync_remote = data.get("sync_remote", False)
            
            # 启动异步加载用户任务
            task_id = f"load_users_{id(self)}"
            coroutine = self.user_service.get_all_users(sync_remote=sync_remote)
            
            self.async_task_manager.queue_task(
                task_id=task_id,
                coroutine=coroutine,
                priority=2,
                progress_callback=self._on_task_progress
            )
            
            self.log_message("加载用户任务已启动")
            
        except Exception as e:
            self.log_message(f"加载用户失败: {e}", is_error=True)
    
    @beartype
    def _handle_save_settings(self, data: Dict[str, Any]) -> None:
        """
        处理保存设置操作
        
        Args:
            data: 设置数据
        """
        try:
            # 这里可以实现设置保存逻辑
            self.log_message(f"设置已保存: {data}")
            
            if self.feature_dialog:
                self.feature_dialog.show_result_message("成功", "设置已保存")
                
        except Exception as e:
            self.log_message(f"保存设置失败: {e}", is_error=True)
            if self.feature_dialog:
                self.feature_dialog.show_result_message("错误", f"保存设置失败: {str(e)}", is_error=True)
    
    @beartype
    def _handle_import_data(self, data: Dict[str, Any]) -> None:
        """
        处理数据导入操作
        
        Args:
            data: 导入数据
        """
        try:
            file_path = data.get("file_path")
            if not file_path:
                return
            
            # 这里可以实现数据导入逻辑
            self.log_message(f"数据导入: {file_path}")
            
            if self.feature_dialog:
                self.feature_dialog.show_result_message("成功", f"数据导入完成: {file_path}")
                
        except Exception as e:
            self.log_message(f"数据导入失败: {e}", is_error=True)
            if self.feature_dialog:
                self.feature_dialog.show_result_message("错误", f"数据导入失败: {str(e)}", is_error=True)
    
    @beartype
    def _on_task_progress(self, progress: float, message: str) -> None:
        """
        任务进度回调
        
        Args:
            progress: 进度百分比
            message: 进度消息
        """
        if self.feature_dialog:
            self.feature_dialog.update_task_progress(progress, message)
    
    @beartype
    def _on_feature_dialog_closed(self, result: int) -> None:
        """
        功能对话框关闭处理
        
        Args:
            result: 对话框结果
        """
        self.log_message("功能对话框已关闭")
        
        # 从活动对话框中移除
        if "feature" in self.active_dialogs:
            del self.active_dialogs["feature"]
    
    @beartype
    def close_all_dialogs(self) -> None:
        """
        关闭所有对话框
        """
        try:
            for dialog_name, dialog in list(self.active_dialogs.items()):
                if dialog and hasattr(dialog, 'close'):
                    dialog.close()
            
            self.active_dialogs.clear()
            self.log_message("所有对话框已关闭")
            
        except Exception as e:
            self.log_message(f"关闭对话框失败: {e}", is_error=True)
    
    @beartype
    def get_active_dialog_count(self) -> int:
        """
        获取活动对话框数量
        
        Returns:
            int: 活动对话框数量
        """
        return len(self.active_dialogs)
    
    @beartype
    async def cleanup(self) -> None:
        """
        清理对话框控制器资源
        """
        try:
            # 关闭所有对话框
            self.close_all_dialogs()
            
            # 清理引用
            self.feature_dialog = None
            
            # 调用基类清理
            await super().cleanup()
            
            self.log_message("对话框控制器清理完成")
            
        except Exception as e:
            self.log_message(f"对话框控制器清理失败: {e}", is_error=True)
