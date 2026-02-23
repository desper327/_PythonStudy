"""
异步工作器
使用asyncio处理异步任务，与Qt事件循环集成
"""
import asyncio
from typing import Any, Callable, Optional, Dict, Coroutine
from PySide6.QtCore import QObject, Signal, QTimer
from beartype import beartype
from models.base_model import TaskStatus


class AsyncWorker(QObject):
    """
    异步工作器类
    将asyncio协程包装为Qt信号槽机制，实现异步操作与UI的集成
    """
    
    # Qt信号定义
    started = Signal(str)  # 任务开始信号，参数：task_id
    progress = Signal(str, float, str)  # 进度更新信号，参数：task_id, progress, message
    finished = Signal(str, object)  # 任务完成信号，参数：task_id, result
    error = Signal(str, str)  # 错误信号，参数：task_id, error_message
    
    @beartype
    def __init__(self, parent: Optional[QObject] = None):
        """
        初始化异步工作器
        
        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self._tasks: Dict[str, TaskStatus] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
        self._loop_timer = QTimer()
        self._loop_timer.timeout.connect(self._process_async_events)
        self._loop_timer.start(10)  # 每10ms检查一次异步事件
    
    @beartype
    def start_event_loop(self) -> None:
        """
        启动异步事件循环
        """
        if self._event_loop is None or self._event_loop.is_closed():
            self._event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._event_loop)
    
    @beartype
    def stop_event_loop(self) -> None:
        """
        停止异步事件循环
        """
        if self._event_loop and not self._event_loop.is_closed():
            # 取消所有运行中的任务
            for task in self._running_tasks.values():
                if not task.done():
                    task.cancel()
            
            # 关闭事件循环
            self._event_loop.close()
            self._event_loop = None
        
        self._loop_timer.stop()
    
    @beartype
    def _process_async_events(self) -> None:
        """
        处理异步事件（在Qt主线程中调用）
        """
        if self._event_loop and not self._event_loop.is_closed():
            # 运行一次事件循环迭代
            try:
                self._event_loop.stop()
                self._event_loop.run_forever()
            except RuntimeError:
                pass  # 事件循环可能已经停止
    
    @beartype
    def run_async_task(
        self, 
        task_id: str, 
        coroutine: Coroutine,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> None:
        """
        运行异步任务
        
        Args:
            task_id: 任务ID
            coroutine: 要执行的协程
            progress_callback: 进度回调函数
        """
        if not self._event_loop:
            self.start_event_loop()
        
        # 创建任务状态
        task_status = TaskStatus(task_id=task_id)
        self._tasks[task_id] = task_status
        
        # 包装协程以处理信号发射
        wrapped_coroutine = self._wrap_coroutine(
            task_id, 
            coroutine, 
            progress_callback
        )
        
        # 在事件循环中创建任务
        task = self._event_loop.create_task(wrapped_coroutine)
        self._running_tasks[task_id] = task
        
        # 发射开始信号
        self.started.emit(task_id)
    
    @beartype
    async def _wrap_coroutine(
        self, 
        task_id: str, 
        coroutine: Coroutine,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Any:
        """
        包装协程以处理信号发射和错误处理
        
        Args:
            task_id: 任务ID
            coroutine: 原始协程
            progress_callback: 进度回调函数
            
        Returns:
            Any: 协程执行结果
        """
        task_status = self._tasks[task_id]
        
        try:
            # 标记任务开始
            task_status.mark_started()
            
            # 如果有进度回调，设置进度更新函数
            if progress_callback:
                def update_progress(progress: float, message: str) -> None:
                    task_status.update_progress(progress, message)
                    self.progress.emit(task_id, progress, message)
                
                # 将进度回调传递给协程（如果协程支持）
                if hasattr(coroutine, 'cr_frame') and coroutine.cr_frame:
                    # 尝试将进度回调注入到协程的局部变量中
                    coroutine.cr_frame.f_locals['progress_callback'] = update_progress
            
            # 执行协程
            result = await coroutine
            
            # 标记任务完成
            task_status.mark_completed(result)
            self.finished.emit(task_id, result)
            
            return result
            
        except asyncio.CancelledError:
            # 任务被取消
            task_status.mark_failed("任务被取消")
            self.error.emit(task_id, "任务被取消")
            raise
            
        except Exception as e:
            # 任务执行出错
            error_message = f"任务执行失败: {str(e)}"
            task_status.mark_failed(error_message)
            self.error.emit(task_id, error_message)
            raise
            
        finally:
            # 清理任务
            if task_id in self._running_tasks:
                del self._running_tasks[task_id]
    
    @beartype
    def cancel_task(self, task_id: str) -> bool:
        """
        取消异步任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功取消
        """
        if task_id in self._running_tasks:
            task = self._running_tasks[task_id]
            if not task.done():
                task.cancel()
                return True
        return False
    
    @beartype
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[TaskStatus]: 任务状态或None
        """
        return self._tasks.get(task_id)
    
    @beartype
    def get_running_tasks(self) -> Dict[str, TaskStatus]:
        """
        获取所有运行中的任务
        
        Returns:
            Dict[str, TaskStatus]: 运行中的任务字典
        """
        return {
            task_id: status 
            for task_id, status in self._tasks.items() 
            if status.status == "running"
        }
    
    @beartype
    def clear_completed_tasks(self) -> None:
        """
        清理已完成的任务
        """
        completed_tasks = [
            task_id for task_id, status in self._tasks.items()
            if status.status in ["completed", "failed"]
        ]
        
        for task_id in completed_tasks:
            del self._tasks[task_id]


class AsyncTaskManager(QObject):
    """
    异步任务管理器
    提供更高级的异步任务管理功能
    """
    
    # 信号定义
    task_queue_changed = Signal(int)  # 任务队列变化信号，参数：队列长度
    all_tasks_completed = Signal()  # 所有任务完成信号
    
    @beartype
    def __init__(self, max_concurrent_tasks: int = 5, parent: Optional[QObject] = None):
        """
        初始化异步任务管理器
        
        Args:
            max_concurrent_tasks: 最大并发任务数
            parent: 父对象
        """
        super().__init__(parent)
        self.max_concurrent_tasks = max_concurrent_tasks
        self.worker = AsyncWorker(self)
        self._task_queue: list = []
        self._active_tasks: Dict[str, Any] = {}
        
        # 连接工作器信号
        self.worker.started.connect(self._on_task_started)
        self.worker.finished.connect(self._on_task_finished)
        self.worker.error.connect(self._on_task_error)
    
    @beartype
    def queue_task(
        self, 
        task_id: str, 
        coroutine: Coroutine,
        priority: int = 0,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> None:
        """
        将任务加入队列
        
        Args:
            task_id: 任务ID
            coroutine: 要执行的协程
            priority: 任务优先级（数值越大优先级越高）
            progress_callback: 进度回调函数
        """
        task_info = {
            "task_id": task_id,
            "coroutine": coroutine,
            "priority": priority,
            "progress_callback": progress_callback
        }
        
        # 按优先级插入队列
        inserted = False
        for i, queued_task in enumerate(self._task_queue):
            if priority > queued_task["priority"]:
                self._task_queue.insert(i, task_info)
                inserted = True
                break
        
        if not inserted:
            self._task_queue.append(task_info)
        
        self.task_queue_changed.emit(len(self._task_queue))
        self._process_queue()
    
    @beartype
    def _process_queue(self) -> None:
        """
        处理任务队列
        """
        # 检查是否可以启动新任务
        while (len(self._active_tasks) < self.max_concurrent_tasks and 
               self._task_queue):
            
            task_info = self._task_queue.pop(0)
            task_id = task_info["task_id"]
            
            # 启动任务
            self._active_tasks[task_id] = task_info
            self.worker.run_async_task(
                task_id,
                task_info["coroutine"],
                task_info["progress_callback"]
            )
            
            self.task_queue_changed.emit(len(self._task_queue))
    
    @beartype
    def _on_task_started(self, task_id: str) -> None:
        """
        任务开始处理
        
        Args:
            task_id: 任务ID
        """
        pass  # 可以在这里添加额外的处理逻辑
    
    @beartype
    def _on_task_finished(self, task_id: str, result: Any) -> None:
        """
        任务完成处理
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        if task_id in self._active_tasks:
            del self._active_tasks[task_id]
        
        # 处理队列中的下一个任务
        self._process_queue()
        
        # 检查是否所有任务都已完成
        if not self._active_tasks and not self._task_queue:
            self.all_tasks_completed.emit()
    
    @beartype
    def _on_task_error(self, task_id: str, error_message: str) -> None:
        """
        任务错误处理
        
        Args:
            task_id: 任务ID
            error_message: 错误消息
        """
        if task_id in self._active_tasks:
            del self._active_tasks[task_id]
        
        # 处理队列中的下一个任务
        self._process_queue()
        
        # 检查是否所有任务都已完成
        if not self._active_tasks and not self._task_queue:
            self.all_tasks_completed.emit()
    
    @beartype
    def cancel_all_tasks(self) -> None:
        """
        取消所有任务
        """
        # 取消活跃任务
        for task_id in list(self._active_tasks.keys()):
            self.worker.cancel_task(task_id)
        
        # 清空队列
        self._task_queue.clear()
        self._active_tasks.clear()
        
        self.task_queue_changed.emit(0)
    
    @beartype
    def get_queue_status(self) -> Dict[str, Any]:
        """
        获取队列状态
        
        Returns:
            Dict[str, Any]: 队列状态信息
        """
        return {
            "queued_tasks": len(self._task_queue),
            "active_tasks": len(self._active_tasks),
            "max_concurrent": self.max_concurrent_tasks,
            "queue_details": [
                {
                    "task_id": task["task_id"],
                    "priority": task["priority"]
                }
                for task in self._task_queue
            ],
            "active_details": [
                {
                    "task_id": task_id,
                    "status": self.worker.get_task_status(task_id)
                }
                for task_id in self._active_tasks.keys()
            ]
        }
    
    def cleanup(self) -> None:
        """
        清理资源
        """
        self.cancel_all_tasks()
        self.worker.stop_event_loop()
