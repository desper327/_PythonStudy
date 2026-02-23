"""
异步任务管理器 - 使用QThreadPool和QRunnable实现线程池
提供简洁的异步任务执行接口，避免UI阻塞
"""
import time
import requests
from typing import Callable, Any, Optional
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication


class TaskSignals(QObject):
    """
    任务信号类 - 用于QRunnable与主线程通信
    因为QRunnable不能直接发射信号，需要单独的QObject
    """
    # 任务完成信号 (任务ID, 结果数据)
    finished = pyqtSignal(str, object)
    
    # 任务出错信号 (任务ID, 错误信息)
    error = pyqtSignal(str, str)
    
    # 任务进度信号 (任务ID, 进度百分比, 状态消息)
    progress = pyqtSignal(str, int, str)
    
    # 任务开始信号 (任务ID)
    started = pyqtSignal(str)


class AsyncTask(QRunnable):
    """
    异步任务类 - 在线程池中执行的任务
    """
    
    def __init__(self, task_id: str, func: Callable, *args, **kwargs):
        """
        初始化异步任务
        
        Args:
            task_id: 任务唯一标识
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        """
        super().__init__()
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignals()
        
        # 设置任务可以自动删除
        self.setAutoDelete(True)
    
    def run(self):
        """
        执行任务 - 在工作线程中运行
        """
        try:
            # 发射任务开始信号
            self.signals.started.emit(self.task_id)
            
            # 执行实际的任务函数
            result = self.func(*self.args, **self.kwargs)
            
            # 发射任务完成信号
            self.signals.finished.emit(self.task_id, result)
            
        except Exception as e:
            # 发射错误信号
            self.signals.error.emit(self.task_id, str(e))


class NetworkTask(QRunnable):
    """
    网络请求任务类 - 专门处理网络操作的异步任务
    """
    
    def __init__(self, task_id: str, url: str, method: str = "GET", 
                 data: Optional[dict] = None, headers: Optional[dict] = None,
                 timeout: int = 30):
        """
        初始化网络任务
        
        Args:
            task_id: 任务唯一标识
            url: 请求URL
            method: HTTP方法 (GET, POST, PUT, DELETE)
            data: 请求数据
            headers: 请求头
            timeout: 超时时间(秒)
        """
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.method = method.upper()
        self.data = data or {}
        self.headers = headers or {}
        self.timeout = timeout
        self.signals = TaskSignals()
        self.setAutoDelete(True)
    
    def run(self):
        """
        执行网络请求 - 在工作线程中运行
        """
        try:
            # 发射任务开始信号
            self.signals.started.emit(self.task_id)
            self.signals.progress.emit(self.task_id, 10, "正在建立连接...")
            
            # 根据HTTP方法执行请求
            if self.method == "GET":
                response = requests.get(
                    self.url, 
                    params=self.data, 
                    headers=self.headers, 
                    timeout=self.timeout
                )
            elif self.method == "POST":
                response = requests.post(
                    self.url, 
                    json=self.data, 
                    headers=self.headers, 
                    timeout=self.timeout
                )
            elif self.method == "PUT":
                response = requests.put(
                    self.url, 
                    json=self.data, 
                    headers=self.headers, 
                    timeout=self.timeout
                )
            elif self.method == "DELETE":
                response = requests.delete(
                    self.url, 
                    headers=self.headers, 
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"不支持的HTTP方法: {self.method}")
            
            self.signals.progress.emit(self.task_id, 80, "正在处理响应...")
            
            # 检查响应状态
            response.raise_for_status()
            
            # 尝试解析JSON响应
            try:
                result = response.json()
            except ValueError:
                result = response.text
            
            self.signals.progress.emit(self.task_id, 100, "请求完成")
            
            # 发射完成信号
            self.signals.finished.emit(self.task_id, {
                'status_code': response.status_code,
                'data': result,
                'headers': dict(response.headers)
            })
            
        except requests.exceptions.Timeout:
            self.signals.error.emit(self.task_id, f"请求超时 ({self.timeout}秒)")
        except requests.exceptions.ConnectionError:
            self.signals.error.emit(self.task_id, "网络连接错误")
        except requests.exceptions.HTTPError as e:
            self.signals.error.emit(self.task_id, f"HTTP错误: {e}")
        except Exception as e:
            self.signals.error.emit(self.task_id, f"网络请求失败: {str(e)}")


class AsyncTaskManager(QObject):
    """
    异步任务管理器 - 统一管理所有异步任务
    """
    
    # 管理器级别的信号
    task_started = pyqtSignal(str)  # 任务开始
    task_finished = pyqtSignal(str, object)  # 任务完成
    task_failed = pyqtSignal(str, str)  # 任务失败
    task_progress = pyqtSignal(str, int, str)  # 任务进度
    
    def __init__(self, max_thread_count: int = None):
        """
        初始化任务管理器
        
        Args:
            max_thread_count: 最大线程数，默认为CPU核心数
        """
        super().__init__()
        
        # 获取全局线程池
        self.thread_pool = QThreadPool.globalInstance()
        
        # 设置最大线程数
        if max_thread_count:
            self.thread_pool.setMaxThreadCount(max_thread_count)
        
        # 任务计数器
        self._task_counter = 0
        
        # 活跃任务字典 {task_id: task_info}
        self._active_tasks = {}
        
        print(f"[AsyncTaskManager] 初始化完成，最大线程数: {self.thread_pool.maxThreadCount()}")
    
    def generate_task_id(self, prefix: str = "task") -> str:
        """
        生成唯一的任务ID
        
        Args:
            prefix: 任务ID前缀
            
        Returns:
            str: 唯一的任务ID
        """
        self._task_counter += 1
        return f"{prefix}_{self._task_counter}_{int(time.time() * 1000)}"
    
    def run_async(self, func: Callable, *args, task_id: str = None, 
                  on_finished: Callable = None, on_error: Callable = None,
                  on_progress: Callable = None, **kwargs) -> str:
        """
        异步执行函数
        
        Args:
            func: 要执行的函数
            *args: 函数参数
            task_id: 任务ID，如果不提供会自动生成
            on_finished: 完成回调函数
            on_error: 错误回调函数
            on_progress: 进度回调函数
            **kwargs: 函数关键字参数
            
        Returns:
            str: 任务ID
        """
        if task_id is None:
            task_id = self.generate_task_id("async")
        
        # 创建异步任务
        task = AsyncTask(task_id, func, *args, **kwargs)
        
        # 连接信号
        task.signals.started.connect(self._on_task_started)
        task.signals.finished.connect(self._on_task_finished)
        task.signals.error.connect(self._on_task_error)
        task.signals.progress.connect(self._on_task_progress)
        
        # 连接用户回调
        if on_finished:
            task.signals.finished.connect(lambda tid, result: on_finished(result) if tid == task_id else None)
        if on_error:
            task.signals.error.connect(lambda tid, error: on_error(error) if tid == task_id else None)
        if on_progress:
            task.signals.progress.connect(lambda tid, progress, msg: on_progress(progress, msg) if tid == task_id else None)
        
        # 记录任务信息
        self._active_tasks[task_id] = {
            'task': task,
            'start_time': time.time(),
            'status': 'pending'
        }
        
        # 提交到线程池
        self.thread_pool.start(task)
        
        print(f"[AsyncTaskManager] 提交任务: {task_id}")
        return task_id
    
    def run_network_request(self, url: str, method: str = "GET", 
                           data: Optional[dict] = None, headers: Optional[dict] = None,
                           timeout: int = 30, task_id: str = None,
                           on_finished: Callable = None, on_error: Callable = None,
                           on_progress: Callable = None) -> str:
        """
        异步执行网络请求
        
        Args:
            url: 请求URL
            method: HTTP方法
            data: 请求数据
            headers: 请求头
            timeout: 超时时间
            task_id: 任务ID
            on_finished: 完成回调
            on_error: 错误回调
            on_progress: 进度回调
            
        Returns:
            str: 任务ID
        """
        if task_id is None:
            task_id = self.generate_task_id("network")
        
        # 创建网络任务
        task = NetworkTask(task_id, url, method, data, headers, timeout)
        
        # 连接信号
        task.signals.started.connect(self._on_task_started)
        task.signals.finished.connect(self._on_task_finished)
        task.signals.error.connect(self._on_task_error)
        task.signals.progress.connect(self._on_task_progress)
        
        # 连接用户回调
        if on_finished:
            task.signals.finished.connect(lambda tid, result: on_finished(result) if tid == task_id else None)
        if on_error:
            task.signals.error.connect(lambda tid, error: on_error(error) if tid == task_id else None)
        if on_progress:
            task.signals.progress.connect(lambda tid, progress, msg: on_progress(progress, msg) if tid == task_id else None)
        
        # 记录任务信息
        self._active_tasks[task_id] = {
            'task': task,
            'start_time': time.time(),
            'status': 'pending',
            'type': 'network',
            'url': url
        }
        
        # 提交到线程池
        self.thread_pool.start(task)
        
        print(f"[AsyncTaskManager] 提交网络请求: {task_id} -> {url}")
        return task_id
    
    def _on_task_started(self, task_id: str):
        """任务开始处理"""
        if task_id in self._active_tasks:
            self._active_tasks[task_id]['status'] = 'running'
        
        print(f"[AsyncTaskManager] 任务开始: {task_id}")
        self.task_started.emit(task_id)
    
    def _on_task_finished(self, task_id: str, result: Any):
        """任务完成处理"""
        if task_id in self._active_tasks:
            task_info = self._active_tasks[task_id]
            task_info['status'] = 'completed'
            task_info['end_time'] = time.time()
            task_info['duration'] = task_info['end_time'] - task_info['start_time']
            
            print(f"[AsyncTaskManager] 任务完成: {task_id} (耗时: {task_info['duration']:.2f}秒)")
            
            # 清理任务记录
            del self._active_tasks[task_id]
        
        self.task_finished.emit(task_id, result)
    
    def _on_task_error(self, task_id: str, error: str):
        """任务错误处理"""
        if task_id in self._active_tasks:
            task_info = self._active_tasks[task_id]
            task_info['status'] = 'failed'
            task_info['end_time'] = time.time()
            task_info['duration'] = task_info['end_time'] - task_info['start_time']
            task_info['error'] = error
            
            print(f"[AsyncTaskManager] 任务失败: {task_id} (耗时: {task_info['duration']:.2f}秒) - {error}")
            
            # 清理任务记录
            del self._active_tasks[task_id]
        
        self.task_failed.emit(task_id, error)
    
    def _on_task_progress(self, task_id: str, progress: int, message: str):
        """任务进度处理"""
        print(f"[AsyncTaskManager] 任务进度: {task_id} - {progress}% - {message}")
        self.task_progress.emit(task_id, progress, message)
    
    def get_active_task_count(self) -> int:
        """获取活跃任务数量"""
        return len(self._active_tasks)
    
    def get_active_tasks(self) -> dict:
        """获取活跃任务信息"""
        return self._active_tasks.copy()
    
    def wait_for_done(self, timeout: int = 30000):
        """
        等待所有任务完成
        
        Args:
            timeout: 超时时间(毫秒)
        """
        self.thread_pool.waitForDone(timeout)
    
    def clear_all_tasks(self):
        """清除所有任务"""
        self.thread_pool.clear()
        self._active_tasks.clear()
        print("[AsyncTaskManager] 已清除所有任务")


# 全局任务管理器实例
_global_task_manager = None

def get_task_manager() -> AsyncTaskManager:
    """
    获取全局任务管理器实例 (单例模式)
    
    Returns:
        AsyncTaskManager: 全局任务管理器
    """
    global _global_task_manager
    if _global_task_manager is None:
        _global_task_manager = AsyncTaskManager()
    return _global_task_manager
