# 聊天客户端前端（client.py）
# 使用 python-socketio 作为客户端，PyQt5 作为界面
import sys
import socketio
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, QObject

SERVER_URL = 'http://127.0.0.1:5000'  # 服务器地址

class Communicate(QObject):
    msg_signal = pyqtSignal(str)

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SocketIO 聊天客户端')
        self.setGeometry(100, 100, 400, 500)
        self.comm = Communicate()
        self.comm.msg_signal.connect(self.display_msg)
        self.init_ui()
        # 创建 socketio 客户端对象
        self.sio = socketio.Client()
        # 绑定服务器推送的 'message' 事件到本地 on_message 方法
        self.sio.on('message', self.on_message)
        # 启动后台线程连接服务器
        threading.Thread(target=self.connect_server, daemon=True).start()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel('聊天记录:')
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText('输入消息并回车发送...')
        self.input_line.returnPressed.connect(self.send_msg)
        self.send_btn = QPushButton('发送')
        self.send_btn.clicked.connect(self.send_msg)
        layout.addWidget(self.label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.input_line)
        layout.addWidget(self.send_btn)
        self.setLayout(layout)

    def connect_server(self):
        try:
            self.sio.connect(SERVER_URL)
            self.comm.msg_signal.emit('已连接到服务器')
        except Exception as e:
            self.comm.msg_signal.emit(f'连接服务器失败: {e}')

    def send_msg(self):
        msg = self.input_line.text().strip()
        if msg:
            try:
                # 发送消息到服务器，事件名为 'message'
                self.sio.emit('message', msg)
                self.display_msg(f'我: {msg}')
            except Exception:
                self.display_msg('消息发送失败')
            self.input_line.clear()

    def on_message(self, data):
        # 收到服务器广播的消息时，显示到聊天窗口
        self.comm.msg_signal.emit(str(data))

    def display_msg(self, msg):
        self.text_area.append(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())
