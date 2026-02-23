"""
任务控制器
专门处理异步任务和线程任务的管理
"""
from typing import Dict, Any, Optional, Callable
from beartype import beartype
from .base_controller import BaseController
from services.user_service import UserService
from services.data_service import DataService
from workers.async_worker import AsyncTaskManager
from workers.thread_worker import ThreadPool, example_long_running_task, example_data_processing_task


class TaskController(BaseController):
    """
    任务控制器类
    负责管理所有异步任务和线程任务的执行
    """
    
    @beartype
    def __init__(self, 
                 user_service: UserService,
                 data_service: DataService,
                 async_task_manager: AsyncTaskManager,
                 thread_pool: ThreadPool,
                 parent=None):
        """
        初始化任务控制器
        
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
        
        # 任务状态跟踪
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.task_callbacks: Dict[str, Callable] = {}
        
        # 任务计数器
        self.task_counter = 0
    
    @beartype
    async def initialize(self) -> None:
        """
        异步初始化任务控制器
        """
        try:
            # 连接工作器信号
            self._connect_worker_signals()
            
            self.log_message("任务控制器初始化完成")
        except Exception as e:
            self.log_message(f"任务控制器初始化失败: {e}", is_error=True)
            raise
    
    @beartype
    def setup_connections(self) -> None:
        """
        设置信号连接
        """
        # 工作器信号连接在initialize中处理
        pass
    
    @beartype
    def _connect_worker_signals(self) -> None:
        """
        连接工作器信号
        """
        # 异步任务管理器信号
        if self.async_task_manager:
            self.async_task_manager.worker.started.connect(self._on_async_task_started)
            self.async_task_manager.worker.progress.connect(self._on_async_task_progress)
            self.async_task_manager.worker.finished.connect(self._on_async_task_finished)
            self.async_task_manager.worker.error.connect(self._on_async_task_error)
        
        # 线程池信号
        if self.thread_pool:
            self.thread_pool.worker_started.connect(self._on_thread_task_started)
            self.thread_pool.worker_progress.connect(self._on_thread_task_progress)
            self.thread_pool.worker_finished.connect(self._on_thread_task_finished)
            self.thread_pool.worker_error.connect(self._on_thread_task_error)
    
    @beartype
    def submit_async_task(self, 
                         task_type: str, 
                         data: Dict[str, Any], 
                         priority: int = 1,
                         callback: Optional[Callable] = None) -> str:
        """
        提交异步任务
        
        Args:
            task_type: 任务类型
            data: 任务数据
            priority: 任务优先级
            callback: 完成回调函数
            
        Returns:
            str: 任务ID
        """
        try:
            # 生成任务ID
            self.task_counter += 1
            task_id = f"{task_type}_{self.task_counter}"
            
            # 根据任务类型创建协程
            coroutine = self._create_async_coroutine(task_type, data)
            if not coroutine:
                raise ValueError(f"未知的异步任务类型: {task_type}")
            
            # 记录任务信息
            self.active_tasks[task_id] = {
                "type": "async",
                "task_type": task_type,
                "data": data,
                "priority": priority,
                "status": "pending"
            }
            
            # 保存回调函数
            if callback:
                self.task_callbacks[task_id] = callback
            
            # 提交任务
            self.async_task_manager.queue_task(
                task_id=task_id,
                coroutine=coroutine,
                priority=priority,
                progress_callback=lambda p, m: self._on_task_progress(task_id, p, m)
            )
            
            self.log_message(f"异步任务已提交: {task_id}")
            return task_id
            
        except Exception as e:
            self.log_message(f"提交异步任务失败: {e}", is_error=True)
            raise
    
    @beartype
    def submit_thread_task(self, 
                          task_type: str, 
                          data: Dict[str, Any], 
                          priority: int = 1,
                          callback: Optional[Callable] = None) -> str:
        """
        提交线程任务
        
        Args:
            task_type: 任务类型
            data: 任务数据
            priority: 任务优先级
            callback: 完成回调函数
            
        Returns:
            str: 任务ID
        """
        try:
            # 生成任务ID
            self.task_counter += 1
            task_id = f"{task_type}_{self.task_counter}"
            
            # 根据任务类型获取目标函数和参数
            target_function, kwargs = self._create_thread_task(task_type, data)
            if not target_function:
                raise ValueError(f"未知的线程任务类型: {task_type}")
            
            # 记录任务信息
            self.active_tasks[task_id] = {
                "type": "thread",
                "task_type": task_type,
                "data": data,
                "priority": priority,
                "status": "pending"
            }
            
            # 保存回调函数
            if callback:
                self.task_callbacks[task_id] = callback
            
            # 提交任务
            success = self.thread_pool.submit_task(
                task_id=task_id,
                target_function=target_function,
                kwargs=kwargs,
                priority=priority,
                progress_callback=lambda p, m: self._on_task_progress(task_id, p, m)
            )
            
            if success:
                self.log_message(f"线程任务已提交: {task_id}")
                return task_id
            else:
                raise RuntimeError("线程任务提交失败")
                
        except Exception as e:
            self.log_message(f"提交线程任务失败: {e}", is_error=True)
            raise
    
    @beartype
    def _create_async_coroutine(self, task_type: str, data: Dict[str, Any]):
        """
        根据任务类型创建异步协程
        
        Args:
            task_type: 任务类型
            data: 任务数据
            
        Returns:
            协程对象或None
        """
        if task_type == "data_processing":
            return self.data_service.process_large_dataset(
                data_size=data.get("data_size", 1000),
                processing_delay=data.get("processing_delay", 0.01)
            )
        elif task_type == "user_report":
            return self.user_service.generate_user_report()
        elif task_type == "trend_analysis":
            return self.data_service.analyze_trends([])
        elif task_type == "export_data":
            return self.data_service.export_data(
                data.get("data", []),
                data.get("format", "json")
            )
        elif task_type == "create_user":
            return self.user_service.create_user(data)
        elif task_type == "load_users":
            return self.user_service.get_all_users(
                sync_remote=data.get("sync_remote", False)
            )
        elif task_type == "batch_process_users":
            return self.user_service.process_user_batch(
                data.get("user_ids", []),
                data.get("operation", "activate")
            )
        else:
            return None
    
    @beartype
    def _create_thread_task(self, task_type: str, data: Dict[str, Any]):
        """
        根据任务类型创建线程任务
        
        Args:
            task_type: 任务类型
            data: 任务数据
            
        Returns:
            tuple: (目标函数, 参数字典) 或 (None, None)
        """
        if task_type == "long_running":
            return example_long_running_task, {
                "duration": data.get("duration", 5.0),
                "steps": data.get("steps", 10)
            }
        elif task_type == "data_processing":
            return example_data_processing_task, {
                "data_size": data.get("data_size", 1000),
                "processing_delay": data.get("processing_delay", 0.001)
            }
        else:
            return None, None
    
    @beartype
    def cancel_task(self, task_id: str) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功取消
        """
        try:
            if task_id not in self.active_tasks:
                return False
            
            task_info = self.active_tasks[task_id]
            task_type = task_info["type"]
            
            success = False
            if task_type == "async":
                success = self.async_task_manager.worker.cancel_task(task_id)
            elif task_type == "thread":
                success = self.thread_pool.cancel_task(task_id)
            
            if success:
                # 更新任务状态
                task_info["status"] = "cancelled"
                self.log_message(f"任务已取消: {task_id}")
            
            return success
            
        except Exception as e:
            self.log_message(f"取消任务失败: {e}", is_error=True)
            return False
    
    @beartype
    def cancel_all_tasks(self) -> None:
        """
        取消所有任务
        """
        try:
            # 取消异步任务
            if self.async_task_manager:
                self.async_task_manager.cancel_all_tasks()
            
            # 取消线程任务
            if self.thread_pool:
                self.thread_pool.cancel_all_tasks()
            
            # 更新所有任务状态
            for task_id, task_info in self.active_tasks.items():
                if task_info["status"] in ["pending", "running"]:
                    task_info["status"] = "cancelled"
            
            self.log_message("所有任务已取消")
            
        except Exception as e:
            self.log_message(f"取消所有任务失败: {e}", is_error=True)
    
    @beartype
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[Dict[str, Any]]: 任务状态信息或None
        """
        return self.active_tasks.get(task_id)
    
    @beartype
    def get_active_task_count(self) -> int:
        """
        获取活动任务数量
        
        Returns:
            int: 活动任务数量
        """
        return len([
            task for task in self.active_tasks.values()
            if task["status"] in ["pending", "running"]
        ])
    
    @beartype
    def get_task_summary(self) -> Dict[str, Any]:
        """
        获取任务摘要
        
        Returns:
            Dict[str, Any]: 任务摘要信息
        """
        summary = {
            "total_tasks": len(self.active_tasks),
            "pending_tasks": 0,
            "running_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "cancelled_tasks": 0,
            "async_tasks": 0,
            "thread_tasks": 0
        }
        
        for task_info in self.active_tasks.values():
            status = task_info["status"]
            task_type = task_info["type"]
            
            summary[f"{status}_tasks"] += 1
            summary[f"{task_type}_tasks"] += 1
        
        return summary
    
    # 任务事件处理方法
    
    @beartype
    def _on_async_task_started(self, task_id: str) -> None:
        """异步任务开始处理"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "running"
        self.log_message(f"异步任务开始: {task_id}")
    
    @beartype
    def _on_async_task_progress(self, task_id: str, progress: float, message: str) -> None:
        """异步任务进度更新"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["progress"] = progress
            self.active_tasks[task_id]["message"] = message
    
    @beartype
    def _on_async_task_finished(self, task_id: str, result: Any) -> None:
        """异步任务完成处理"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "completed"
            self.active_tasks[task_id]["result"] = result
        
        # 执行回调函数
        if task_id in self.task_callbacks:
            try:
                callback = self.task_callbacks[task_id]
                callback(task_id, result, None)
                del self.task_callbacks[task_id]
            except Exception as e:
                self.log_message(f"任务回调执行失败: {e}", is_error=True)
        
        self.log_message(f"异步任务完成: {task_id}")
    
    @beartype
    def _on_async_task_error(self, task_id: str, error_message: str) -> None:
        """异步任务错误处理"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "failed"
            self.active_tasks[task_id]["error"] = error_message
        
        # 执行回调函数
        if task_id in self.task_callbacks:
            try:
                callback = self.task_callbacks[task_id]
                callback(task_id, None, error_message)
                del self.task_callbacks[task_id]
            except Exception as e:
                self.log_message(f"任务回调执行失败: {e}", is_error=True)
        
        self.log_message(f"异步任务失败: {task_id} - {error_message}", is_error=True)
    
    @beartype
    def _on_thread_task_started(self, task_id: str) -> None:
        """线程任务开始处理"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "running"
        self.log_message(f"线程任务开始: {task_id}")
    
    @beartype
    def _on_thread_task_progress(self, task_id: str, progress: float, message: str) -> None:
        """线程任务进度更新"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["progress"] = progress
            self.active_tasks[task_id]["message"] = message
    
    @beartype
    def _on_thread_task_finished(self, task_id: str, result: Any) -> None:
        """线程任务完成处理"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "completed"
            self.active_tasks[task_id]["result"] = result
        
        # 执行回调函数
        if task_id in self.task_callbacks:
            try:
                callback = self.task_callbacks[task_id]
                callback(task_id, result, None)
                del self.task_callbacks[task_id]
            except Exception as e:
                self.log_message(f"任务回调执行失败: {e}", is_error=True)
        
        self.log_message(f"线程任务完成: {task_id}")
    
    @beartype
    def _on_thread_task_error(self, task_id: str, error_message: str) -> None:
        """线程任务错误处理"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "failed"
            self.active_tasks[task_id]["error"] = error_message
        
        # 执行回调函数
        if task_id in self.task_callbacks:
            try:
                callback = self.task_callbacks[task_id]
                callback(task_id, None, error_message)
                del self.task_callbacks[task_id]
            except Exception as e:
                self.log_message(f"任务回调执行失败: {e}", is_error=True)
        
        self.log_message(f"线程任务失败: {task_id} - {error_message}", is_error=True)
    
    @beartype
    def _on_task_progress(self, task_id: str, progress: float, message: str) -> None:
        """
        任务进度回调
        
        Args:
            task_id: 任务ID
            progress: 进度百分比
            message: 进度消息
        """
        # 这个方法可以被外部监听，用于更新UI
        pass
    
    @beartype
    def clear_completed_tasks(self) -> None:
        """
        清理已完成的任务
        """
        try:
            completed_tasks = [
                task_id for task_id, task_info in self.active_tasks.items()
                if task_info["status"] in ["completed", "failed", "cancelled"]
            ]
            
            for task_id in completed_tasks:
                del self.active_tasks[task_id]
                if task_id in self.task_callbacks:
                    del self.task_callbacks[task_id]
            
            self.log_message(f"已清理 {len(completed_tasks)} 个完成的任务")
            
        except Exception as e:
            self.log_message(f"清理完成任务失败: {e}", is_error=True)
    
    @beartype
    async def cleanup(self) -> None:
        """
        清理任务控制器资源
        """
        try:
            # 取消所有任务
            self.cancel_all_tasks()
            
            # 清理任务记录
            self.active_tasks.clear()
            self.task_callbacks.clear()
            
            # 调用基类清理
            await super().cleanup()
            
            self.log_message("任务控制器清理完成")
            
        except Exception as e:
            self.log_message(f"任务控制器清理失败: {e}", is_error=True)
