"""
工作线程 - 使用QThread执行耗时任务
直接创建工作线程处理耗时操作，避免UI阻塞
"""
import inspect
from typing import Any, List
from Qt.QtCore import QThread, Signal
from models.data_models import SignalData, TaskSpec

class WorkerThread(QThread):
    """
    工作线程 - 执行耗时任务
    
    """
    
    # 线程信号
    tread_signal = Signal(SignalData)  
    
    def __init__(self, tasks: List[TaskSpec]):
        """
        初始化工作线程
        
        Args:
            tasks: 要执行的任务列表
        """
        super().__init__()
        self.tasks = tasks
        self._is_running = False

    def _emit_progress(self, percent: int):
        if self._is_running:
            self.tread_signal.emit(SignalData(signal_type='on_progress_thread', params={"progress": int(percent)}))

    def _emit_log(self, message: str):
        if self._is_running:
            self.tread_signal.emit(SignalData(signal_type='on_log_thread', params={"message": str(message)}))

    def _is_cancelled(self) -> bool:
        return self.isInterruptionRequested() or (not self._is_running)

    def _call_task(self, task: TaskSpec):
        sig = inspect.signature(task.func)
        kwargs = dict(task.kwargs)

        if 'progress' in sig.parameters:
            kwargs['progress'] = self._emit_progress
        if 'log' in sig.parameters:
            kwargs['log'] = self._emit_log
        if 'is_cancelled' in sig.parameters:
            kwargs['is_cancelled'] = self._is_cancelled

        return task.func(*task.args, **kwargs)
    
    def run(self):
        """
        线程执行方法 - 在子线程中运行
        """
        try:
            self._is_running = True
            
            # 发射开始信号
            self.tread_signal.emit(SignalData(signal_type='on_start_thread', params={}))
            
            if not self.tasks:
                self.tread_signal.emit(SignalData(signal_type='on_finish_thread', params={"result": None}))
                return

            result: Any = None

            for i, task in enumerate(self.tasks):
                if self._is_cancelled():
                    self.tread_signal.emit(SignalData(signal_type='on_cancel_thread', params={}))
                    return

                current = self._call_task(task)
                if task.return_result:
                    result = current

                percent = 100 * (i + 1) // len(self.tasks)
                self._emit_progress(percent)

            self.tread_signal.emit(SignalData(signal_type='on_finish_thread', params={"result": result}))

        except Exception as e:
            # 发射错误信号
            if self._is_running:
                self.tread_signal.emit(SignalData(signal_type='on_error_thread', params={"error": str(e)}))
        finally:
            self._is_running = False
    
    def stop(self):
        """停止线程执行"""
        self._is_running = False
        self.requestInterruption()
        self.quit()
        self.wait()
    
    def is_running_task(self) -> bool:
        """检查任务是否正在运行"""
        return self._is_running