from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import QThread, Slot
from worker import Worker # 导入我们的工作对象

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThread 计数器示例")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.count_label = QLabel("当前计数: 0")
        self.start_button = QPushButton("开始计数")
        self.stop_button = QPushButton("停止计数")
        self.stop_button.setEnabled(False) # 初始禁用停止按钮

        layout.addWidget(self.count_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_counting)
        self.stop_button.clicked.connect(self.stop_counting)

        self.worker_thread = None
        self.worker_object = None

    @Slot()
    def start_counting(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():
            print("主线程: 启动计数...")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            # 1. 创建 QThread 实例
            self.worker_thread = QThread()
            # 2. 创建工作对象
            self.worker_object = Worker()
            # 3. 将工作对象移动到线程
            self.worker_object.moveToThread(self.worker_thread)

            # 4. 连接信号和槽
            # 当线程启动时，调用工作对象的 do_work 方法
            self.worker_thread.started.connect(self.worker_object.do_work)
            # 当工作对象发送 current_count 信号时，更新 UI
            self.worker_object.current_count.connect(self.update_count_label)
            # 当工作对象任务完成时
            self.worker_object.finished.connect(self.worker_thread.quit) # 任务完成，线程退出
            self.worker_object.finished.connect(self.worker_object.deleteLater) # 任务完成，工作对象自清理
            self.worker_thread.finished.connect(self.worker_thread.deleteLater) # 线程退出，线程对象自清理
            self.worker_thread.finished.connect(self.on_counting_finished) # 线程退出，更新 UI 状态

            # 5. 启动线程
            self.worker_thread.start()
        else:
            print("主线程: 计数器已在运行.")

    @Slot(int)
    def update_count_label(self, count):
        self.count_label.setText(f"当前计数: {count}")

    @Slot()
    def stop_counting(self):
        if self.worker_object:
            print("主线程: 请求停止计数...")
            self.worker_object.stop() # 通知工作对象停止

    @Slot()
    def on_counting_finished(self):
        print("主线程: 计数任务已完全结束.")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # 此时 worker_thread 和 worker_object 应该已经被 deleteLater 清理了

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()