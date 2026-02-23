from PySide6.QtCore import QObject, Signal, Slot
import time

class Worker(QObject):
    # 定义一个信号，用于发送当前计数给主线程
    current_count = Signal(int)
    # 定义一个信号，表示任务完成
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True # 控制任务运行的标志

    def stop(self):
        self._running = False

    @Slot() # 这是一个槽，可以被线程的 started 信号连接
    def do_work(self):
        print("Worker: 任务开始...")
        count = 0
        while self._running and count < 10: # 假设我们计数到10
            time.sleep(1) # 模拟耗时操作
            count += 1
            self.current_count.emit(count) # 发送信号
            print(f"Worker: Current count is {count}")
        print("Worker: 任务完成.")
        self.finished.emit() # 发送任务完成信号