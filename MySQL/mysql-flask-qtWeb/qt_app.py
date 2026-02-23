import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from threading import Thread
import subprocess

# 启动 Flask 应用
def run_flask_app():
    subprocess.run(["python", r"MyStudy\MySQL\mysql-flask-qtWeb\app.py"])

# 创建 PyQt5 主窗口
class MainWindow(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flask in QtWebEngine")
        self.resize(800, 600)

        # 加载 Flask 应用的 URL
        self.load(QUrl("http://127.0.0.1:5000"))

# 启动 PyQt5 应用
if __name__ == '__main__':
    # 在单独的线程中启动 Flask 应用
    flask_thread = Thread(target=run_flask_app)
    flask_thread.daemon = True  # 设置为守护线程，主程序退出时 Flask 也会退出
    flask_thread.start()

    # 启动 PyQt5 应用
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())