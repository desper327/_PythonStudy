"""
线程工作器
使用QThread处理耗时任务，避免阻塞UI线程
"""
import time
import threading
from typing import Any, Callable, Optional, Dict
from PySide6.QtCore import QThread, QObject, Signal, QMutex, QWaitCondition
from beartype import beartype
from models.base_model import TaskStatus


class ThreadWorker(QThread):
    """
    线程工作器类
    继承自QThread，用于在后台线程中执行耗时任务
    """
    
    # Qt信号定义
    started = Signal(str)  # 任务开始信号，参数：task_id
    progress = Signal(str, float, str)  # 进度更新信号，参数：task_id, progress, message
    finished = Signal(str, object)  # 任务完成信号，参数：task_id, result
    error = Signal(str, str)  # 错误信号，参数：task_id, error_message
    
    @beartype
    def __init__(self, 
                 task_id: str,
                 target_function: Callable,
                 args: tuple = (),
                 kwargs: Optional[Dict[str, Any]] = None,
                 progress_callback: Optional[Callable[[float, str], None]] = None,
                 parent: Optional[QObject] = None):
        """
        初始化线程工作器
        
        Args:
            task_id: 任务ID
            target_function: 要执行的目标函数
            args: 函数参数
            kwargs: 函数关键字参数
            progress_callback: 进度回调函数
            parent: 父对象
        """
        super().__init__(parent)
        self.task_id = task_id
        self.target_function = target_function
        self.args = args
        self.kwargs = kwargs or {}
        self.progress_callback = progress_callback
        self._is_cancelled = False
        self._mutex = QMutex()
        self.task_status = TaskStatus(task_id=task_id)
    
    @beartype
    def run(self) -> None:
        """
        线程执行函数
        """
        try:
            # 发射开始信号
            self.started.emit(self.task_id)
            self.task_status.mark_started()
            
            # 设置进度回调
            if self.progress_callback:
                def update_progress(progress: float, message: str) -> None:
                    if not self._is_cancelled:
                        self.task_status.update_progress(progress, message)
                        self.progress.emit(self.task_id, progress, message)
                
                # 将进度回调添加到kwargs中
                self.kwargs['progress_callback'] = update_progress
            
            # 执行目标函数
            result = self.target_function(*self.args, **self.kwargs)
            
            # 检查是否被取消
            if self._is_cancelled:
                self.task_status.mark_failed("任务被取消")
                self.error.emit(self.task_id, "任务被取消")
                return
            
            # 标记任务完成
            self.task_status.mark_completed(result)
            self.finished.emit(self.task_id, result)
            
        except Exception as e:
            # 处理异常
            error_message = f"任务执行失败: {str(e)}"
            self.task_status.mark_failed(error_message)
            self.error.emit(self.task_id, error_message)
    
    @beartype
    def cancel(self) -> None:
        """
        取消任务
        """
        with QMutex():
            self._is_cancelled = True
    
    @beartype
    def is_cancelled(self) -> bool:
        """
        检查任务是否被取消
        
        Returns:
            bool: 是否被取消
        """
        return self._is_cancelled
    
    @beartype
    def get_task_status(self) -> TaskStatus:
        """
        获取任务状态
        
        Returns:
            TaskStatus: 任务状态
        """
        return self.task_status


class ThreadPool(QObject):
    """
    线程池管理器
    管理多个线程工作器，提供线程池功能
    """
    
    # 信号定义
    worker_started = Signal(str)  # 工作器开始信号
    worker_finished = Signal(str, object)  # 工作器完成信号
    worker_error = Signal(str, str)  # 工作器错误信号
    worker_progress = Signal(str, float, str)  # 工作器进度信号
    pool_status_changed = Signal(dict)  # 线程池状态变化信号
    
    @beartype
    def __init__(self, max_threads: int = 4, parent: Optional[QObject] = None):
        """
        初始化线程池
        
        Args:
            max_threads: 最大线程数
            parent: 父对象
        """
        super().__init__(parent)
        self.max_threads = max_threads
        self._workers: Dict[str, ThreadWorker] = {}
        self._task_queue: list = []
        self._active_count = 0
        self._mutex = QMutex()
    
    @beartype
    def submit_task(self,
                   task_id: str,
                   target_function: Callable,
                   args: tuple = (),
                   kwargs: Optional[Dict[str, Any]] = None,
                   priority: int = 0,
                   progress_callback: Optional[Callable[[float, str], None]] = None) -> bool:
        """
        提交任务到线程池
        
        Args:
            task_id: 任务ID
            target_function: 目标函数
            args: 函数参数
            kwargs: 函数关键字参数
            priority: 任务优先级
            progress_callback: 进度回调函数
            
        Returns:
            bool: 是否成功提交
        """
        with QMutex():
            # 检查任务ID是否已存在
            if task_id in self._workers:
                return False
            
            task_info = {
                'task_id': task_id,
                'target_function': target_function,
                'args': args,
                'kwargs': kwargs or {},
                'priority': priority,
                'progress_callback': progress_callback
            }
            
            # 按优先级插入队列
            inserted = False
            for i, queued_task in enumerate(self._task_queue):
                if priority > queued_task['priority']:
                    self._task_queue.insert(i, task_info)
                    inserted = True
                    break
            
            if not inserted:
                self._task_queue.append(task_info)
            
            # 尝试启动任务
            self._start_next_task()
            
            return True
    
    @beartype
    def _start_next_task(self) -> None:
        """
        启动下一个任务
        """
        # 检查是否可以启动新任务
        if self._active_count >= self.max_threads or not self._task_queue:
            return
        
        # 获取下一个任务
        task_info = self._task_queue.pop(0)
        
        # 创建工作器
        worker = ThreadWorker(
            task_id=task_info['task_id'],
            target_function=task_info['target_function'],
            args=task_info['args'],
            kwargs=task_info['kwargs'],
            progress_callback=task_info['progress_callback'],
            parent=self
        )
        
        # 连接信号
        worker.started.connect(self._on_worker_started)
        worker.finished.connect(self._on_worker_finished)
        worker.error.connect(self._on_worker_error)
        worker.progress.connect(self._on_worker_progress)
        
        # 启动工作器
        self._workers[task_info['task_id']] = worker
        self._active_count += 1
        worker.start()
        
        # 发射状态变化信号
        self._emit_status_changed()
    
    @beartype
    def _on_worker_started(self, task_id: str) -> None:
        """
        工作器开始处理
        
        Args:
            task_id: 任务ID
        """
        self.worker_started.emit(task_id)
    
    @beartype
    def _on_worker_finished(self, task_id: str, result: Any) -> None:
        """
        工作器完成处理
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        self._cleanup_worker(task_id)
        self.worker_finished.emit(task_id, result)
        
        # 启动下一个任务
        self._start_next_task()
    
    @beartype
    def _on_worker_error(self, task_id: str, error_message: str) -> None:
        """
        工作器错误处理
        
        Args:
            task_id: 任务ID
            error_message: 错误消息
        """
        self._cleanup_worker(task_id)
        self.worker_error.emit(task_id, error_message)
        
        # 启动下一个任务
        self._start_next_task()
    
    @beartype
    def _on_worker_progress(self, task_id: str, progress: float, message: str) -> None:
        """
        工作器进度处理
        
        Args:
            task_id: 任务ID
            progress: 进度百分比
            message: 进度消息
        """
        self.worker_progress.emit(task_id, progress, message)
    
    @beartype
    def _cleanup_worker(self, task_id: str) -> None:
        """
        清理工作器
        
        Args:
            task_id: 任务ID
        """
        with QMutex():
            if task_id in self._workers:
                worker = self._workers[task_id]
                worker.wait()  # 等待线程结束
                del self._workers[task_id]
                self._active_count -= 1
                
                # 发射状态变化信号
                self._emit_status_changed()
    
    @beartype
    def cancel_task(self, task_id: str) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功取消
        """
        with QMutex():
            # 检查是否在运行中的任务
            if task_id in self._workers:
                worker = self._workers[task_id]
                worker.cancel()
                return True
            
            # 检查是否在队列中
            for i, task_info in enumerate(self._task_queue):
                if task_info['task_id'] == task_id:
                    del self._task_queue[i]
                    self._emit_status_changed()
                    return True
            
            return False
    
    @beartype
    def cancel_all_tasks(self) -> None:
        """
        取消所有任务
        """
        with QMutex():
            # 取消运行中的任务
            for worker in self._workers.values():
                worker.cancel()
            
            # 清空队列
            self._task_queue.clear()
            
            self._emit_status_changed()
    
    @beartype
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[TaskStatus]: 任务状态或None
        """
        if task_id in self._workers:
            return self._workers[task_id].get_task_status()
        return None
    
    @beartype
    def get_pool_status(self) -> Dict[str, Any]:
        """
        获取线程池状态
        
        Returns:
            Dict[str, Any]: 线程池状态信息
        """
        return {
            'max_threads': self.max_threads,
            'active_threads': self._active_count,
            'queued_tasks': len(self._task_queue),
            'running_tasks': list(self._workers.keys()),
            'queue_details': [
                {
                    'task_id': task['task_id'],
                    'priority': task['priority']
                }
                for task in self._task_queue
            ]
        }
    
    @beartype
    def _emit_status_changed(self) -> None:
        """
        发射状态变化信号
        """
        status = self.get_pool_status()
        self.pool_status_changed.emit(status)
    
    @beartype
    def wait_for_all_tasks(self, timeout: int = -1) -> bool:
        """
        等待所有任务完成
        
        Args:
            timeout: 超时时间（毫秒），-1表示无限等待
            
        Returns:
            bool: 是否所有任务都完成
        """
        start_time = time.time()
        
        while self._active_count > 0 or self._task_queue:
            if timeout > 0:
                elapsed = (time.time() - start_time) * 1000
                if elapsed >= timeout:
                    return False
            
            time.sleep(0.1)  # 短暂休眠
        
        return True
    
    def cleanup(self) -> None:
        """
        清理线程池资源
        """
        self.cancel_all_tasks()
        
        # 等待所有线程结束
        for worker in list(self._workers.values()):
            worker.wait()
        
        self._workers.clear()
        self._active_count = 0


# 示例耗时任务函数
@beartype
def example_long_running_task(
    duration: float = 5.0,
    steps: int = 10,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> Dict[str, Any]:
    """
    示例耗时任务
    
    Args:
        duration: 总耗时（秒）
        steps: 步骤数
        progress_callback: 进度回调函数
        
    Returns:
        Dict[str, Any]: 任务结果
    """
    step_duration = duration / steps
    
    for i in range(steps):
        # 模拟工作
        time.sleep(step_duration)
        
        # 更新进度
        progress = (i + 1) / steps * 100
        message = f"正在执行步骤 {i + 1}/{steps}"
        
        if progress_callback:
            progress_callback(progress, message)
    
    return {
        "task_completed": True,
        "total_steps": steps,
        "duration": duration,
        "result": "任务执行成功"
    }


@beartype
def example_data_processing_task(
    data_size: int = 1000,
    processing_delay: float = 0.001,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> Dict[str, Any]:
    """
    示例数据处理任务
    
    Args:
        data_size: 数据大小
        processing_delay: 每项处理延迟
        progress_callback: 进度回调函数
        
    Returns:
        Dict[str, Any]: 处理结果
    """
    processed_items = 0
    total_value = 0
    
    for i in range(data_size):
        # 模拟数据处理
        value = i * 2 + 1
        total_value += value
        processed_items += 1
        
        # 模拟处理时间
        if processing_delay > 0:
            time.sleep(processing_delay)
        
        # 更新进度
        if progress_callback and (i % 100 == 0 or i == data_size - 1):
            progress = (i + 1) / data_size * 100
            message = f"已处理 {i + 1}/{data_size} 项数据"
            progress_callback(progress, message)
    
    return {
        "processed_items": processed_items,
        "total_value": total_value,
        "average_value": total_value / processed_items if processed_items > 0 else 0,
        "processing_time": data_size * processing_delay
    }
