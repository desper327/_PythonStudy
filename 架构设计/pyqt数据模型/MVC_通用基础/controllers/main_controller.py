"""
主控制器 - 协调模型和视图之间的交互
使用自定义信号和槽机制，手动同步数据和UI
"""
import time
from Qt.QtCore import QObject
from models.data_models import TextData, SignalData, TreadSpec, ProcessSpec
from models.data_center import DataCenter
from views.main_view import MainView
from services.worker_thread import WorkerThread
from services.worker_process import ProcessWorker

class MainController(QObject):
    """主控制器 - 使用自定义信号槽架构"""

    def __init__(self):
        super().__init__()

        self.view_signal_dict={
            "on_show_text":self.handle_show_text,
            "on_start_thread":self.handle_start_thread,
            "on_start_process":self.handle_start_process,
        }
        self.model_signal_dict={
        "text_changed":self.on_text_changed_update_ui,
        "thread_data_changed": self.on_thread_data_changed_update_ui,
        "process_data_changed": self.on_process_data_changed_update_ui,
    }

        self.thread_signal_dict={
            "on_start_thread": self.handle_thread_start,
            "on_finish_thread": self.handle_thread_finish,
            "on_progress_thread": self.handle_thread_progress,
            "on_error_thread": self.handle_thread_error,
            "on_log_thread": self.handle_thread_log,
            "on_cancel_thread": self.handle_thread_cancel,
        }

        self.process_signal_dict = {
            "on_process_starting": self.on_process_starting,
            "on_process_started": self.on_process_started,
            "on_process_stdout": self.on_process_stdout,
            "on_process_stderr": self.on_process_stderr,
            "on_process_finished": self.on_process_finished,
            "on_process_error": self.on_process_error,
            "on_process_state_changed": self.on_process_state_changed,
            "on_process_terminating": self.on_process_terminating,
            "on_process_killing": self.on_process_killing,
            "on_process_detached_started": self.on_process_detached_started,
        }

        self.worker_thread: WorkerThread | None = None

        # 初始化数据仓库
        self.data_center = DataCenter()
        
        # 初始化视图
        self.view = MainView()
        
        # 连接信号和槽
        self.connect_signals()
        
    
    def connect_signals(self):
        """连接视图信号到控制器方法，连接仓库信号到UI更新方法"""
        
        # ========== 视图信号 -> 控制器方法 ==========
        self.view.view_signal.connect(self.handle_view_signal)
        
        # ========== 仓库信号 -> UI更新槽函数 ==========
        self.data_center.model_signal.connect(self.handle_model_signal)
    

    # ========== 处理视图请求的方法 ==========
    def handle_view_signal(self, signal_data: SignalData):
        """
        处理视图信号
        """
        print("[Controller] 收到view信号: ", signal_data.signal_type, signal_data.params)
        if signal_data.signal_type in self.view_signal_dict:
            self.view_signal_dict[signal_data.signal_type](**signal_data.params)
    
    # ========== 响应仓库信号的UI更新槽函数 ==========
    def handle_model_signal(self, signal_data: SignalData):
        """
        槽函数：当仓库发出任务信号后，更新UI
        
        Args:
            signal_data: 信号数据
        """
        print(f"[Controller] 收到model信号: {signal_data.signal_type}, {signal_data.params}")
        
        # 根据信号类型更新UI
        if signal_data.signal_type in self.model_signal_dict:
            self.model_signal_dict[signal_data.signal_type](**signal_data.params)
    
    def handle_show_text(self,text_data: TextData):
        """
        槽函数：处理显示文本按钮点击事件
        """
        print(f"[Controller] handle_show_text: {text_data.text}")
        self.data_center.text = text_data


#======== 处理线程请求的方法 ========
    def handle_start_thread(self):
        """
        槽函数：处理开始子线程按钮点击事件
        """
        print("[Controller] handle_start_thread")

        if self.worker_thread is not None and self.worker_thread.isRunning():
            return

        def fun1():
            print("任务1开始")
            time.sleep(2)
            print("任务1结束")

        def fun2():
            print("任务2开始")
            for i in range(1, 6):
                time.sleep(0.4)
            print("任务2结束")
            return "任务2的返回结果"

        tasks = [
            TreadSpec(func=fun1),
            TreadSpec(func=fun2, return_result=True),
        ]

        self.worker_thread = WorkerThread(tasks)
        self.worker_thread.thread_signal.connect(self.handle_thread_signal)
        self.worker_thread.finished.connect(self._on_worker_thread_finished)
        self.worker_thread.start()

    def _on_worker_thread_finished(self):
        self.worker_thread = None

    def handle_thread_signal(self, signal_data: SignalData):
        """
        槽函数：执行子线程信号
        """
        print(f"[Controller] 收到子线程信号: {signal_data.signal_type}, {signal_data.params}")
        if signal_data.signal_type in self.thread_signal_dict:
            self.thread_signal_dict[signal_data.signal_type](**signal_data.params)
    
    def handle_thread_start(self):
        """开始显示在text"""
        print("handle_thread_start")
        self.data_center.text = TextData(text="开始")
    def handle_thread_finish(self, result: str):
        """结果显示在thread_label"""
        print("handle_thread_finish",result)
        self.data_center.thread_data = TextData(text=f"完成: {result}")
    def handle_thread_progress(self, progress: int): 
        """进度显示在text"""
        print("handle_thread_progress",progress)
        self.data_center.text = TextData(text=f"进度: {progress}")  
    def handle_thread_error(self, error: str): 
        """错误信息显示在thread_label"""
        print("handle_thread_error",error)
        self.cleanup()
        self.show_error(error)
        self.data_center.thread_data = TextData(text=f"错误: {error}")

    def handle_thread_log(self, message: str):
        self.data_center.thread_data = TextData(text=str(message))

    def handle_thread_cancel(self):
        self.data_center.thread_data = TextData(text="已取消")


#======== 处理进程请求的方法 ========
    def handle_start_process(self):
        """
        槽函数：处理开始进程按钮点击事件
        """
        print("[Controller] handle_start_process")
        self.process_worker = ProcessWorker()
        self.process_worker.process_signal.connect(self.handle_process_signal)
        self.process_worker.start(ProcessSpec(program="python", arguments=["-c", "print('hello world')"]))

    def handle_process_signal(self, signal_data: SignalData):
        print("[Controller] 收到进程信号")
        if signal_data.signal_type in self.process_signal_dict:
            self.process_signal_dict[signal_data.signal_type](**signal_data.params)

    def on_process_starting(self):
        print("[Controller] on_process_starting")

    def on_process_started(self):
        print("[Controller] on_process_started")
    
    def on_process_stdout(self):
        print("[Controller] on_process_stdout")
    
    def on_process_stderr(self):
        print("[Controller] on_process_stderr")
    
    def on_process_finished(self):
        print("[Controller] on_process_finished")

    def on_process_state_changed(self):
        print("[Controller] on_process_state_changed")

    def on_process_terminating(self):
        print("[Controller] on_process_terminating")
    
    def on_process_killing(self):
        print("[Controller] on_process_killing")
    
    def on_process_detached_started(self):
        print("[Controller] on_process_detached_started")
    
    def on_process_error(self):
        print("[Controller] on_process_error")


#======== 处理数据中心数据变更的方法 ========
    def on_text_changed_update_ui(self, new_text: TextData):
        """
        槽函数：当数据中心的文本发生变化时，更新UI
        
        Args:
            new_text: 新的文本数据
        """
        print(f"[Controller] on_text_changed_update_ui: {new_text.text}")
        self.view.show_label.setText(new_text.text)
    
    def on_thread_data_changed_update_ui(self, new_thread_data: TextData):
        """线程数据变化时更新UI"""
        print("[Controller] on_thread_data_changed_update_ui")
        self.view.thread_label.setText(new_thread_data.text)
    
    def on_process_data_changed_update_ui(self, new_process_data: TextData):
        """进程数据变化时更新UI"""
        print("[Controller] on_process_data_changed_update_ui")
        self.view.process_label.setText(new_process_data.text)

    def show(self):
        """显示主窗口"""
        self.view.show()
        print("[Controller] 应用程序已启动")

    def show_error(self, error: str):
        """显示错误信息"""
        print(f"[Controller] 错误: {error}")
        self.view.show_error(error)

    def cleanup(self):
        """应用退出前清理资源"""
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.worker_thread.stop()