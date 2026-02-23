"""
注册窗口
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from config import Config
from network import APIClient


class RegisterWindow(QWidget):
    """注册窗口类"""
    
    # 注册成功信号（传递用户名）
    register_success = Signal(str)
    
    def __init__(self):
        """初始化注册窗口"""
        super().__init__()
        
        # API客户端
        self.api_client = APIClient()
        
        # 初始化UI
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('注册 - ' + Config.APP_NAME)
        self.setFixedSize(400, 600)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # 顶部空白
        main_layout.addStretch(1)
        
        # 标题
        title_label = QLabel('创建账号')
        title_label.setObjectName('titleLabel')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel('加入我们，开始聊天吧！')
        subtitle_label.setObjectName('secondaryLabel')
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(20)
        
        # 用户名
        username_label = QLabel('用户名 *')
        main_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('3-50个字符，只能包含字母和数字')
        self.username_input.setFixedHeight(40)
        main_layout.addWidget(self.username_input)
        
        # 昵称
        nickname_label = QLabel('昵称 *')
        main_layout.addWidget(nickname_label)
        
        self.nickname_input = QLineEdit()
        self.nickname_input.setPlaceholderText('请输入昵称')
        self.nickname_input.setFixedHeight(40)
        main_layout.addWidget(self.nickname_input)
        
        # 邮箱
        email_label = QLabel('邮箱（可选）')
        main_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('请输入邮箱')
        self.email_input.setFixedHeight(40)
        main_layout.addWidget(self.email_input)
        
        # 密码
        password_label = QLabel('密码 *')
        main_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('至少6个字符')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        main_layout.addWidget(self.password_input)
        
        # 确认密码
        confirm_label = QLabel('确认密码 *')
        main_layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('再次输入密码')
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setFixedHeight(40)
        self.confirm_input.returnPressed.connect(self.on_register_clicked)  # 回车注册
        main_layout.addWidget(self.confirm_input)
        
        main_layout.addSpacing(10)
        
        # 注册按钮
        self.register_button = QPushButton('注册')
        self.register_button.setFixedHeight(40)
        self.register_button.clicked.connect(self.on_register_clicked)
        main_layout.addWidget(self.register_button)
        
        # 返回登录按钮
        self.back_button = QPushButton('已有账号？返回登录')
        self.back_button.setObjectName('secondaryButton')
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.close)
        main_layout.addWidget(self.back_button)
        
        # 底部空白
        main_layout.addStretch(2)
        
        self.setLayout(main_layout)
    
    def on_register_clicked(self):
        """处理注册按钮点击事件"""
        username = self.username_input.text().strip()
        nickname = self.nickname_input.text().strip()
        email = self.email_input.text().strip() or None
        password = self.password_input.text()
        confirm_password = self.confirm_input.text()
        
        # 验证输入
        if not username:
            QMessageBox.warning(self, '错误', '请输入用户名')
            return
        
        if not nickname:
            QMessageBox.warning(self, '错误', '请输入昵称')
            return
        
        if not password:
            QMessageBox.warning(self, '错误', '请输入密码')
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, '错误', '两次输入的密码不一致')
            return
        
        # 禁用按钮
        self.register_button.setEnabled(False)
        self.register_button.setText('注册中...')
        
        # 调用API注册
        response = self.api_client.register(username, password, nickname, email)
        
        # 恢复按钮
        self.register_button.setEnabled(True)
        self.register_button.setText('注册')
        
        # 处理响应
        if response['code'] == 201:
            # 注册成功
            self.register_success.emit(username)
            self.close()
        else:
            # 注册失败
            QMessageBox.critical(self, '注册失败', response['message'])
