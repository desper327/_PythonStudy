"""
登录窗口
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from config import Config
from network import APIClient
from utils import Storage


class LoginWindow(QWidget):
    """登录窗口类"""
    
    # 登录成功信号（传递token和用户信息）
    login_success = Signal(str, dict)
    
    def __init__(self):
        """初始化登录窗口"""
        super().__init__()
        
        # API客户端
        self.api_client = APIClient()
        
        # 初始化UI
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('登录 - ' + Config.APP_NAME)
        self.setFixedSize(400, 500)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # 顶部空白
        main_layout.addStretch(1)
        
        # 标题
        title_label = QLabel(Config.APP_NAME)
        title_label.setObjectName('titleLabel')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel('欢迎回来！')
        subtitle_label.setObjectName('secondaryLabel')
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(20)
        
        # 用户名标签
        username_label = QLabel('用户名')
        main_layout.addWidget(username_label)
        
        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        self.username_input.setFixedHeight(40)
        main_layout.addWidget(self.username_input)
        
        # 密码标签
        password_label = QLabel('密码')
        main_layout.addWidget(password_label)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.returnPressed.connect(self.on_login_clicked)  # 回车登录
        main_layout.addWidget(self.password_input)
        
        main_layout.addSpacing(10)
        
        # 登录按钮
        self.login_button = QPushButton('登录')
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.on_login_clicked)
        main_layout.addWidget(self.login_button)
        
        # 注册按钮
        self.register_button = QPushButton('还没有账号？立即注册')
        self.register_button.setObjectName('secondaryButton')
        self.register_button.setFixedHeight(40)
        self.register_button.clicked.connect(self.on_register_clicked)
        main_layout.addWidget(self.register_button)
        
        # 底部空白
        main_layout.addStretch(2)
        
        # 版本信息
        version_label = QLabel(f'版本 {Config.APP_VERSION}')
        version_label.setObjectName('secondaryLabel')
        version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(version_label)
        
        self.setLayout(main_layout)
    
    def on_login_clicked(self):
        """处理登录按钮点击事件"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # 验证输入
        if not username:
            QMessageBox.warning(self, '错误', '请输入用户名')
            return
        
        if not password:
            QMessageBox.warning(self, '错误', '请输入密码')
            return
        
        # 禁用按钮
        self.login_button.setEnabled(False)
        self.login_button.setText('登录中...')
        
        # 调用API登录
        response = self.api_client.login(username, password)
        
        # 恢复按钮
        self.login_button.setEnabled(True)
        self.login_button.setText('登录')
        
        # 处理响应
        if response['code'] == 200:
            # 登录成功
            token = response['data']['token']
            user = response['data']['user']
            
            # 保存Token到本地
            Storage.save_token(token)
            
            # 发送登录成功信号
            self.login_success.emit(token, user)
            
            # 关闭窗口
            self.close()
        else:
            # 登录失败
            QMessageBox.critical(self, '登录失败', response['message'])
    
    def on_register_clicked(self):
        """处理注册按钮点击事件"""
        # 导入注册窗口
        from .register_window import RegisterWindow
        
        # 创建注册窗口
        self.register_window = RegisterWindow()
        self.register_window.register_success.connect(self.on_register_success)
        self.register_window.show()
    
    def on_register_success(self, username: str):
        """
        处理注册成功事件
        
        Args:
            username: 注册的用户名
        """
        # 自动填充用户名
        self.username_input.setText(username)
        self.password_input.setFocus()
        
        QMessageBox.information(self, '注册成功', f'欢迎 {username}！请登录。')
