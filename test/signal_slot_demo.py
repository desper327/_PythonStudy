import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, QObject


class SimpleSignal(QObject):
    # 自定义信号
    custom_signal = Signal(str)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("信号槽机制示例")
        self.setGeometry(100, 100, 300, 200)
        
        # 创建控件
        self.button = QPushButton("点击我")
        self.label = QLabel("等待点击...")
        
        # 创建信号对象
        self.signal_obj = SimpleSignal()
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
        # 连接信号和槽
        self.button.clicked.connect(self.on_button_clicked)  # 内置信号
        self.signal_obj.custom_signal.connect(self.on_custom_signal)  # 自定义信号
    
    def on_button_clicked(self):
        """按钮点击槽函数"""
        self.label.setText("按钮被点击了！")
        self.signal_obj.custom_signal.emit("来自自定义信号的消息")
    
    def on_custom_signal(self, message):
        """自定义信号槽函数"""
        self.label.setText(f"收到信号: {message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())