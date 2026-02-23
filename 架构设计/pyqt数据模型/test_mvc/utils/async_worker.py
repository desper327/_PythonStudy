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

