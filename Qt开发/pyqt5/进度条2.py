import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressDialog, QVBoxLayout, QWidget

class WorkerThread(QThread):
    # 定义一个信号，用于更新进度条
    update_label = pyqtSignal(str)

    def __init__(self, tasks, parent=None):
        super().__init__(parent)
        self.tasks = tasks

    def run(self):
        for task in self.tasks:
            # 模拟任务执行时间
            time.sleep(2)  # 这里只是模拟，实际应用中避免使用time.sleep
            
            # 发射信号更新进度条的消息
            self.update_label.emit(f"正在处理任务: {task}")
        
        # 任务完成后关闭进度对话框
        self.update_label.emit("所有任务已完成")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("进度条示例")
        self.setGeometry(100, 100, 300, 200)

        # 创建一个按钮来启动任务
        self.start_button = QPushButton("开始任务", self)
        self.start_button.clicked.connect(self.start_tasks)

        # 创建一个布局并将按钮添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)

        # 创建一个中心窗口部件并将布局添加到其中
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 初始化进度对话框，不显示进度百分比
        self.progress_dialog = QProgressDialog("正在处理任务...", "取消", 0, 0, self)
        self.progress_dialog.setWindowTitle("进度条")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)  # 确保进度对话框立即显示
        self.progress_dialog.setCancelButton(None)  # 去掉取消按钮，因为不需要用户取消操作

    def start_tasks(self):
        # 定义要执行的任务列表
        tasks = ["任务1", "任务2", "任务3", "任务4"]
        
        # 创建并启动工作线程
        self.worker_thread = WorkerThread(tasks, self)
        self.worker_thread.update_label.connect(self.update_progress_dialog)
        self.worker_thread.finished.connect(self.progress_dialog.close)
        self.worker_thread.start()

        # 显示进度对话框
        self.progress_dialog.show()

    def update_progress_dialog(self, message):
        # 更新进度条的消息
        self.progress_dialog.setLabelText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
