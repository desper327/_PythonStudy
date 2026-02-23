"""
工作线程 - 使用QThread执行耗时任务
直接创建工作线程处理耗时操作，避免UI阻塞
"""
import time
import requests
from typing import Callable, Any, Optional, Dict
from PyQt5.QtCore import QThread, pyqtSignal, QObject


class WorkerThread(QThread):
    """
    工作线程 - 执行耗时任务
    """
    
    # 线程信号
    started = pyqtSignal()  # 任务开始
    progress = pyqtSignal(int, str)  # 进度更新 (百分比, 消息)
    finished = pyqtSignal(object)  # 任务完成 (结果)
    error = pyqtSignal(str)  # 任务错误 (错误信息)
    
    def __init__(self, task_func: Callable, *args, **kwargs):
        """
        初始化工作线程
        
        Args:
            task_func: 要执行的任务函数
            *args: 任务函数的参数
            **kwargs: 任务函数的关键字参数
        """
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs
        self._is_running = False
    
    def run(self):
        """
        线程执行方法 - 在子线程中运行
        """
        try:
            self._is_running = True
            
            # 发射开始信号
            self.started.emit()
            
            # 执行任务函数
            result = self.task_func(*self.args, **self.kwargs)
            
            # 发射完成信号
            if self._is_running:  # 检查是否被中断
                self.finished.emit(result)
                
        except Exception as e:
            # 发射错误信号
            if self._is_running:
                self.error.emit(str(e))
        finally:
            self._is_running = False
    
    def stop(self):
        """停止线程执行"""
        self._is_running = False
        self.quit()
        self.wait()  # 等待线程结束
    
    def is_running_task(self) -> bool:
        """检查任务是否正在运行"""
        return self._is_running


class NetworkWorkerThread(QThread):
    """
    网络请求工作线程 - 专门处理网络操作
    """
    
    # 网络请求信号
    started = pyqtSignal()
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)  # 返回 {status_code, data, headers}
    error = pyqtSignal(str)
    
    def __init__(self, url: str, method: str = "GET", 
                 data: Optional[Dict] = None, headers: Optional[Dict] = None,
                 timeout: int = 30):
        """
        初始化网络工作线程
        
        Args:
            url: 请求URL
            method: HTTP方法
            data: 请求数据
            headers: 请求头
            timeout: 超时时间
        """
        super().__init__()
        self.url = url
        self.method = method.upper()
        self.data = data or {}
        self.headers = headers or {}
        self.timeout = timeout
        self._is_running = False
    
    def run(self):
        """执行网络请求"""
        try:
            self._is_running = True
            
            # 发射开始信号
            self.started.emit()
            self.progress.emit(10, "正在建立连接...")
            
            # 执行网络请求
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
            
            if not self._is_running:
                return
            
            self.progress.emit(80, "正在处理响应...")
            
            # 检查响应状态
            response.raise_for_status()
            
            # 解析响应数据
            try:
                data = response.json()
            except ValueError:
                data = response.text
            
            if not self._is_running:
                return
            
            self.progress.emit(100, "请求完成")
            
            # 发射完成信号
            result = {
                'status_code': response.status_code,
                'data': data,
                'headers': dict(response.headers)
            }
            
            self.finished.emit(result)
            
        except requests.exceptions.Timeout:
            if self._is_running:
                self.error.emit(f"请求超时 ({self.timeout}秒)")
        except requests.exceptions.ConnectionError:
            if self._is_running:
                self.error.emit("网络连接错误")
        except requests.exceptions.HTTPError as e:
            if self._is_running:
                self.error.emit(f"HTTP错误: {e}")
        except Exception as e:
            if self._is_running:
                self.error.emit(f"网络请求失败: {str(e)}")
        finally:
            self._is_running = False
    
    def stop(self):
        """停止网络请求"""
        self._is_running = False
        self.quit()
        self.wait()


class SimpleTaskManager(QObject):
    """
    任务管理器 - 管理工作线程
    """
    
    # 管理器信号
    task_started = pyqtSignal(str)  # 任务开始
    task_finished = pyqtSignal(str, object)  # 任务完成
    task_failed = pyqtSignal(str, str)  # 任务失败
    task_progress = pyqtSignal(str, int, str)  # 任务进度
    
    def __init__(self):
        super().__init__()
        self._active_threads = {}  # 活跃线程字典 {task_id: thread}
        self._task_counter = 0
    
    def generate_task_id(self, prefix: str = "task") -> str:
        """生成任务ID"""
        self._task_counter += 1
        return f"{prefix}_{self._task_counter}_{int(time.time() * 1000)}"
    
    def run_task(self, task_func: Callable, *args, task_id: str = None, 
                 on_finished: Callable = None, on_error: Callable = None,
                 on_progress: Callable = None, **kwargs) -> str:
        """
        运行任务
        
        Args:
            task_func: 任务函数
            *args: 函数参数
            task_id: 任务ID
            on_finished: 完成回调
            on_error: 错误回调
            on_progress: 进度回调
            **kwargs: 函数关键字参数
            
        Returns:
            str: 任务ID
        """
        if task_id is None:
            task_id = self.generate_task_id("task")
        
        # 创建工作线程
        thread = WorkerThread(task_func, *args, **kwargs)
        
        # 连接信号
        thread.started.connect(lambda: self._on_task_started(task_id))
        thread.finished.connect(lambda result: self._on_task_finished(task_id, result))
        thread.error.connect(lambda error: self._on_task_error(task_id, error))
        thread.progress.connect(lambda progress, msg: self._on_task_progress(task_id, progress, msg))
        
        # 连接用户回调
        if on_finished:
            thread.finished.connect(on_finished)
        if on_error:
            thread.error.connect(on_error)
        if on_progress:
            thread.progress.connect(lambda progress, msg: on_progress(progress, msg))
        
        # 线程结束时自动清理
        thread.finished.connect(lambda: self._cleanup_thread(task_id))
        thread.error.connect(lambda: self._cleanup_thread(task_id))
        
        # 记录线程
        self._active_threads[task_id] = thread
        
        # 启动线程
        thread.start()
        
        print(f"[SimpleTaskManager] 启动任务: {task_id}")
        return task_id
    
    def run_network_request(self, url: str, method: str = "GET",
                           data: Optional[Dict] = None, headers: Optional[Dict] = None,
                           timeout: int = 30, task_id: str = None,
                           on_finished: Callable = None, on_error: Callable = None,
                           on_progress: Callable = None) -> str:
        """
        运行网络请求
        
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
        
        # 创建网络工作线程
        thread = NetworkWorkerThread(url, method, data, headers, timeout)
        
        # 连接信号
        thread.started.connect(lambda: self._on_task_started(task_id))
        thread.finished.connect(lambda result: self._on_task_finished(task_id, result))
        thread.error.connect(lambda error: self._on_task_error(task_id, error))
        thread.progress.connect(lambda progress, msg: self._on_task_progress(task_id, progress, msg))
        
        # 连接用户回调
        if on_finished:
            thread.finished.connect(on_finished)
        if on_error:
            thread.error.connect(on_error)
        if on_progress:
            thread.progress.connect(lambda progress, msg: on_progress(progress, msg))
        
        # 线程结束时自动清理
        thread.finished.connect(lambda: self._cleanup_thread(task_id))
        thread.error.connect(lambda: self._cleanup_thread(task_id))
        
        # 记录线程
        self._active_threads[task_id] = thread
        
        # 启动线程
        thread.start()
        
        print(f"[SimpleTaskManager] 启动网络请求: {task_id} -> {url}")
        return task_id
    
    def stop_task(self, task_id: str) -> bool:
        """
        停止指定任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功停止
        """
        if task_id in self._active_threads:
            thread = self._active_threads[task_id]
            thread.stop()
            del self._active_threads[task_id]
            print(f"[SimpleTaskManager] 停止任务: {task_id}")
            return True
        return False
    
    def stop_all_tasks(self):
        """停止所有任务"""
        for task_id in list(self._active_threads.keys()):
            self.stop_task(task_id)
        print("[SimpleTaskManager] 已停止所有任务")
    
    def get_active_task_count(self) -> int:
        """获取活跃任务数量"""
        return len(self._active_threads)
    
    def get_active_task_ids(self) -> list:
        """获取活跃任务ID列表"""
        return list(self._active_threads.keys())
    
    def _on_task_started(self, task_id: str):
        """任务开始处理"""
        print(f"[SimpleTaskManager] 任务开始: {task_id}")
        self.task_started.emit(task_id)
    
    def _on_task_finished(self, task_id: str, result: Any):
        """任务完成处理"""
        print(f"[SimpleTaskManager] 任务完成: {task_id}")
        self.task_finished.emit(task_id, result)
    
    def _on_task_error(self, task_id: str, error: str):
        """任务错误处理"""
        print(f"[SimpleTaskManager] 任务失败: {task_id} - {error}")
        self.task_failed.emit(task_id, error)
    
    def _on_task_progress(self, task_id: str, progress: int, message: str):
        """任务进度处理"""
        print(f"[SimpleTaskManager] 任务进度: {task_id} - {progress}% - {message}")
        self.task_progress.emit(task_id, progress, message)
    
    def _cleanup_thread(self, task_id: str):
        """清理线程"""
        if task_id in self._active_threads:
            thread = self._active_threads[task_id]
            thread.quit()
            thread.wait()  # 等待线程结束
            del self._active_threads[task_id]
            print(f"[SimpleTaskManager] 清理线程: {task_id}")


# 全局任务管理器实例
_global_simple_manager = None

def get_simple_task_manager() -> SimpleTaskManager:
    """
    获取全局任务管理器实例
    
    Returns:
        SimpleTaskManager: 全局任务管理器
    """
    global _global_simple_manager
    if _global_simple_manager is None:
        _global_simple_manager = SimpleTaskManager()
    return _global_simple_manager
