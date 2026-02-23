"""
工作线程 - 使用QThread执行耗时任务
直接创建工作线程处理耗时操作，避免UI阻塞
"""
import time
from typing import Callable, Any, Optional, Dict, List
from Qt.QtCore import QThread, Signal, QObject
from models.data_models import TextData, SignalData

class WorkerThread(QThread):
    """
    工作线程 - 执行耗时任务
    """
    
    # 线程信号
    tread_signal = Signal(SignalData)  
    
    def __init__(self, task_funcs: List[Callable]):
        """
        初始化工作线程
        
        Args:
            task_funcs: 要执行的任务函数列表
        """
        super().__init__()
        self.task_funcs = task_funcs
        self._is_running = False
    
    def run(self):
        """
        线程执行方法 - 在子线程中运行
        """
        try:
            self._is_running = True
            
            # 发射开始信号
            self.tread_signal.emit(SignalData(signal_type='on_start_thread', params=[]))
            
            # 执行任务函数
            for i, task_func in enumerate(self.task_funcs):
                if i == len(self.task_funcs) - 1:
                    result=task_func()
                    self.tread_signal.emit(SignalData(signal_type='on_finish_thread', params=[result]))
                else:
                    task_func()
                percent = 100 * (i + 1) // len(self.task_funcs)
                self.tread_signal.emit(SignalData(signal_type='on_progress_thread', params=[percent]))

        except Exception as e:
            # 发射错误信号
            if self._is_running:
                self.tread_signal.emit(SignalData(signal_type='on_error_thread', params=[str(e)]))
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