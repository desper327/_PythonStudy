"""
主窗口（聊天界面）
包含联系人列表、群组列表和聊天界面
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QTabWidget, QInputDialog, QMenu
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QAction
from config import Config
from network import APIClient, SocketClient
from utils import Storage


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, token: str, user_info: dict):
        """
        初始化主窗口
        
        Args:
            token: JWT Token
            user_info: 用户信息
        """
        super().__init__()
        
        # 保存用户信息
        self.token = token
        self.user_info = user_info
        
        # API客户端
        self.api_client = APIClient()
        self.api_client.set_token(token)
        
        # WebSocket客户端
        self.socket_client = SocketClient()
        
        # 当前聊天对象
        self.current_chat_type = None  # 'private' 或 'group'
        self.current_chat_id = None
        self.current_chat_name = None
        
        # 联系人和群组数据
        self.contacts = {}  # {user_id: user_info}
        self.groups = {}    # {group_id: group_info}
        
        # 初始化UI
        self.init_ui()
        
        # 连接WebSocket
        self.connect_websocket()
        
        # 加载数据
        self.load_groups()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(f'{Config.APP_NAME} - {self.user_info["nickname"]}')
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.setMinimumSize(Config.MIN_WINDOW_WIDTH, Config.MIN_WINDOW_HEIGHT)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局（水平分割）
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧面板（联系人和群组）
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧面板（聊天区域）
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        # 状态栏
        self.statusBar().showMessage('准备就绪')
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        logout_action = QAction('退出登录', self)
        logout_action.triggered.connect(self.on_logout)
        file_menu.addAction(logout_action)
        
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 群组菜单
        group_menu = menubar.addMenu('群组')
        
        create_group_action = QAction('创建群组', self)
        create_group_action.triggered.connect(self.on_create_group)
        group_menu.addAction(create_group_action)
        
        join_group_action = QAction('加入群组', self)
        join_group_action.triggered.connect(self.on_join_group)
        group_menu.addAction(join_group_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
    
    def create_left_panel(self) -> QWidget:
        """
        创建左侧面板（联系人和群组列表）
        
        Returns:
            QWidget: 左侧面板
        """
        panel = QWidget()
        panel.setMinimumWidth(250)
        panel.setMaximumWidth(400)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 用户信息区域
        user_info_layout = QHBoxLayout()
        
        user_name_label = QLabel(f'👤 {self.user_info["nickname"]}')
        user_name_label.setStyleSheet('font-weight: bold; font-size: 16px;')
        user_info_layout.addWidget(user_name_label)
        
        user_info_layout.addStretch()
        
        layout.addLayout(user_info_layout)
        
        # 标签页（联系人 / 群组）
        self.tab_widget = QTabWidget()
        
        # 联系人标签页
        contacts_tab = QWidget()
        contacts_layout = QVBoxLayout()
        contacts_layout.setContentsMargins(0, 10, 0, 0)
        
        # 搜索用户
        search_layout = QHBoxLayout()
        self.user_search_input = QLineEdit()
        self.user_search_input.setPlaceholderText('搜索用户...')
        search_layout.addWidget(self.user_search_input)
        
        search_button = QPushButton('搜索')
        search_button.clicked.connect(self.on_search_users)
        search_layout.addWidget(search_button)
        
        contacts_layout.addLayout(search_layout)
        
        # 联系人列表
        self.contacts_list = QListWidget()
        self.contacts_list.itemClicked.connect(self.on_contact_clicked)
        contacts_layout.addWidget(self.contacts_list)
        
        contacts_tab.setLayout(contacts_layout)
        self.tab_widget.addTab(contacts_tab, '联系人')
        
        # 群组标签页
        groups_tab = QWidget()
        groups_layout = QVBoxLayout()
        groups_layout.setContentsMargins(0, 10, 0, 0)
        
        # 群组列表
        self.groups_list = QListWidget()
        self.groups_list.itemClicked.connect(self.on_group_clicked)
        self.groups_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.groups_list.customContextMenuRequested.connect(self.on_group_context_menu)
        groups_layout.addWidget(self.groups_list)
        
        groups_tab.setLayout(groups_layout)
        self.tab_widget.addTab(groups_tab, '群组')
        
        layout.addWidget(self.tab_widget)
        
        panel.setLayout(layout)
        return panel
    
    def create_right_panel(self) -> QWidget:
        """
        创建右侧面板（聊天区域）
        
        Returns:
            QWidget: 右侧面板
        """
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 聊天头部
        header_widget = QWidget()
        header_widget.setStyleSheet(f'background-color: white; border-bottom: 1px solid {Config.BORDER_COLOR};')
        header_widget.setFixedHeight(60)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        self.chat_title_label = QLabel('请选择联系人或群组开始聊天')
        self.chat_title_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        header_layout.addWidget(self.chat_title_label)
        
        header_layout.addStretch()
        
        header_widget.setLayout(header_layout)
        layout.addWidget(header_widget)
        
        # 消息显示区域
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        layout.addWidget(self.message_display, 3)
        
        # 输入区域
        input_widget = QWidget()
        input_widget.setStyleSheet(f'background-color: white; border-top: 1px solid {Config.BORDER_COLOR};')
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(10, 10, 10, 10)
        input_layout.setSpacing(10)
        
        # 消息输入框
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText('输入消息... (Ctrl+Enter 发送)')
        self.message_input.setMaximumHeight(100)
        self.message_input.installEventFilter(self)  # 安装事件过滤器（处理快捷键）
        input_layout.addWidget(self.message_input)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.send_button = QPushButton('发送 (Ctrl+Enter)')
        self.send_button.setMinimumWidth(150)
        self.send_button.clicked.connect(self.on_send_message)
        self.send_button.setEnabled(False)
        button_layout.addWidget(self.send_button)
        
        input_layout.addLayout(button_layout)
        
        input_widget.setLayout(input_layout)
        layout.addWidget(input_widget, 1)
        
        panel.setLayout(layout)
        return panel
    
    def eventFilter(self, obj, event):
        """
        事件过滤器（处理Ctrl+Enter发送消息）
        
        Args:
            obj: 事件对象
            event: 事件
            
        Returns:
            bool: 是否拦截事件
        """
        from PySide6.QtGui import QKeyEvent
        from PySide6.QtCore import QEvent
        
        if obj == self.message_input and event.type() == QEvent.KeyPress:
            key_event = event
            # Ctrl+Enter 发送消息
            if key_event.key() == Qt.Key_Return and key_event.modifiers() == Qt.ControlModifier:
                self.on_send_message()
                return True
        
        return super().eventFilter(obj, event)
    
    def connect_websocket(self):
        """连接WebSocket"""
        # 连接信号
        self.socket_client.connected.connect(self.on_socket_connected)
        self.socket_client.disconnected.connect(self.on_socket_disconnected)
        self.socket_client.authenticated.connect(self.on_socket_authenticated)
        self.socket_client.error_occurred.connect(self.on_socket_error)
        self.socket_client.new_private_message.connect(self.on_new_private_message)
        self.socket_client.new_group_message.connect(self.on_new_group_message)
        self.socket_client.message_sent.connect(self.on_message_sent)
        
        # 连接到服务器
        self.socket_client.connect_to_server()
    
    def on_socket_connected(self):
        """WebSocket连接成功"""
        self.statusBar().showMessage('已连接到服务器，正在认证...')
        # 发送认证请求
        self.socket_client.authenticate(self.token)
    
    def on_socket_disconnected(self):
        """WebSocket断开连接"""
        self.statusBar().showMessage('与服务器断开连接')
        QMessageBox.warning(self, '连接断开', '与服务器的连接已断开')
    
    def on_socket_authenticated(self, data):
        """WebSocket认证成功"""
        self.statusBar().showMessage('在线')
    
    def on_socket_error(self, message):
        """WebSocket错误"""
        self.statusBar().showMessage(f'错误: {message}')
    
    def on_new_private_message(self, data):
        """接收到新私聊消息"""
        # 如果当前正在和发送者聊天，显示消息
        if self.current_chat_type == 'private' and self.current_chat_id == data['sender_id']:
            self.display_message(data)
        else:
            # 显示通知（后续实现）
            pass
    
    def on_new_group_message(self, data):
        """接收到新群组消息"""
        # 如果当前正在群组聊天，显示消息
        if self.current_chat_type == 'group' and self.current_chat_id == data['group_id']:
            self.display_message(data)
        else:
            # 显示通知（后续实现）
            pass
    
    def on_message_sent(self, data):
        """消息发送成功"""
        message = data.get('message')
        if message:
            self.display_message(message)
    
    def load_groups(self):
        """加载群组列表"""
        response = self.api_client.get_my_groups()
        
        if response['code'] == 200:
            groups = response['data']['groups']
            self.groups = {group['id']: group for group in groups}
            
            # 更新群组列表
            self.groups_list.clear()
            for group in groups:
                item = QListWidgetItem(f"👥 {group['name']}")
                item.setData(Qt.UserRole, group['id'])
                self.groups_list.addItem(item)
                
                # 加入群组房间（接收消息）
                self.socket_client.join_group_room(group['id'])
        else:
            QMessageBox.warning(self, '错误', f"加载群组失败: {response['message']}")
    
    def on_search_users(self):
        """搜索用户"""
        keyword = self.user_search_input.text().strip()
        
        if not keyword:
            QMessageBox.warning(self, '错误', '请输入搜索关键词')
            return
        
        response = self.api_client.search_users(keyword)
        
        if response['code'] == 200:
            users = response['data']['users']
            
            if not users:
                QMessageBox.information(self, '搜索结果', '未找到匹配的用户')
                return
            
            # 更新联系人列表
            self.contacts_list.clear()
            for user in users:
                self.contacts[user['id']] = user
                item = QListWidgetItem(f"👤 {user['nickname']} (@{user['username']})")
                item.setData(Qt.UserRole, user['id'])
                self.contacts_list.addItem(item)
        else:
            QMessageBox.warning(self, '错误', f"搜索失败: {response['message']}")
    
    def on_contact_clicked(self, item):
        """点击联系人"""
        user_id = item.data(Qt.UserRole)
        user = self.contacts.get(user_id)
        
        if user:
            self.open_private_chat(user_id, user['nickname'])
    
    def on_group_clicked(self, item):
        """点击群组"""
        group_id = item.data(Qt.UserRole)
        group = self.groups.get(group_id)
        
        if group:
            self.open_group_chat(group_id, group['name'])
    
    def on_group_context_menu(self, pos):
        """群组右键菜单"""
        item = self.groups_list.itemAt(pos)
        if not item:
            return
        
        group_id = item.data(Qt.UserRole)
        
        menu = QMenu(self)
        
        # 查看成员
        view_members_action = QAction('查看成员', self)
        view_members_action.triggered.connect(lambda: self.on_view_members(group_id))
        menu.addAction(view_members_action)
        
        # 退出群组
        leave_action = QAction('退出群组', self)
        leave_action.triggered.connect(lambda: self.on_leave_group(group_id))
        menu.addAction(leave_action)
        
        menu.exec(self.groups_list.mapToGlobal(pos))
    
    def open_private_chat(self, user_id: int, user_name: str):
        """
        打开私聊窗口
        
        Args:
            user_id: 用户ID
            user_name: 用户名
        """
        self.current_chat_type = 'private'
        self.current_chat_id = user_id
        self.current_chat_name = user_name
        
        self.chat_title_label.setText(f'💬 {user_name}')
        self.send_button.setEnabled(True)
        
        # 加载历史消息
        self.load_private_messages(user_id)
    
    def open_group_chat(self, group_id: int, group_name: str):
        """
        打开群组聊天窗口
        
        Args:
            group_id: 群组ID
            group_name: 群组名
        """
        self.current_chat_type = 'group'
        self.current_chat_id = group_id
        self.current_chat_name = group_name
        
        self.chat_title_label.setText(f'👥 {group_name}')
        self.send_button.setEnabled(True)
        
        # 加载历史消息
        self.load_group_messages(group_id)
    
    def load_private_messages(self, user_id: int):
        """加载私聊历史消息"""
        self.message_display.clear()
        
        response = self.api_client.get_private_messages(user_id, page=1, per_page=50)
        
        if response['code'] == 200:
            messages = response['data']['messages']
            for msg in messages:
                self.display_message(msg)
        else:
            self.message_display.append(f'<p style="color: red;">加载消息失败: {response["message"]}</p>')
    
    def load_group_messages(self, group_id: int):
        """加载群组历史消息"""
        self.message_display.clear()
        
        response = self.api_client.get_group_messages(group_id, page=1, per_page=50)
        
        if response['code'] == 200:
            messages = response['data']['messages']
            for msg in messages:
                self.display_message(msg)
        else:
            self.message_display.append(f'<p style="color: red;">加载消息失败: {response["message"]}</p>')
    
    def display_message(self, message: dict):
        """
        显示消息
        
        Args:
            message: 消息数据
        """
        sender_name = message.get('sender_name', '未知')
        content = message.get('content', '')
        created_at = message.get('created_at', '')
        
        # 判断是否是自己发送的
        is_me = message.get('sender_id') == self.user_info['id']
        
        # 格式化时间
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            time_str = dt.strftime('%H:%M:%S')
        except:
            time_str = created_at
        
        # 显示消息
        if is_me:
            html = f'''
            <div style="text-align: right; margin: 10px;">
                <span style="color: {Config.TEXT_SECONDARY}; font-size: 12px;">{time_str}</span><br>
                <span style="background-color: {Config.PRIMARY_COLOR}; color: white; 
                      padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 70%;">
                    {content}
                </span>
            </div>
            '''
        else:
            html = f'''
            <div style="text-align: left; margin: 10px;">
                <span style="font-weight: bold; color: {Config.PRIMARY_COLOR};">{sender_name}</span>
                <span style="color: {Config.TEXT_SECONDARY}; font-size: 12px; margin-left: 8px;">{time_str}</span><br>
                <span style="background-color: white; border: 1px solid {Config.BORDER_COLOR}; 
                      padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 70%;">
                    {content}
                </span>
            </div>
            '''
        
        self.message_display.append(html)
        
        # 滚动到底部
        scrollbar = self.message_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_send_message(self):
        """发送消息"""
        content = self.message_input.toPlainText().strip()
        
        if not content:
            return
        
        if not self.current_chat_type or not self.current_chat_id:
            QMessageBox.warning(self, '错误', '请先选择聊天对象')
            return
        
        # 发送消息
        if self.current_chat_type == 'private':
            self.socket_client.send_private_message(self.current_chat_id, content)
        elif self.current_chat_type == 'group':
            self.socket_client.send_group_message(self.current_chat_id, content)
        
        # 清空输入框
        self.message_input.clear()
    
    def on_create_group(self):
        """创建群组"""
        name, ok = QInputDialog.getText(self, '创建群组', '群组名称:')
        
        if not ok or not name:
            return
        
        response = self.api_client.create_group(name)
        
        if response['code'] == 201:
            QMessageBox.information(self, '成功', '群组创建成功')
            self.load_groups()  # 重新加载群组列表
        else:
            QMessageBox.critical(self, '失败', f"创建群组失败: {response['message']}")
    
    def on_join_group(self):
        """加入群组"""
        # 获取公开群组列表
        response = self.api_client.get_public_groups()
        
        if response['code'] != 200:
            QMessageBox.critical(self, '错误', f"获取群组列表失败: {response['message']}")
            return
        
        groups = response['data']['groups']
        
        if not groups:
            QMessageBox.information(self, '提示', '暂无可加入的公开群组')
            return
        
        # 让用户选择群组
        group_names = [f"{g['name']} (成员: {g['member_count']})" for g in groups]
        name, ok = QInputDialog.getItem(self, '加入群组', '选择群组:', group_names, 0, False)
        
        if not ok:
            return
        
        # 获取选中的群组
        index = group_names.index(name)
        group = groups[index]
        
        # 加入群组
        response = self.api_client.join_group(group['id'])
        
        if response['code'] == 200:
            QMessageBox.information(self, '成功', '加入群组成功')
            self.load_groups()  # 重新加载群组列表
        else:
            QMessageBox.critical(self, '失败', f"加入群组失败: {response['message']}")
    
    def on_view_members(self, group_id: int):
        """查看群组成员"""
        response = self.api_client.get_group_members(group_id)
        
        if response['code'] == 200:
            members = response['data']['members']
            member_list = '\n'.join([f"{m['nickname']} ({m['role']})" for m in members])
            QMessageBox.information(self, '群组成员', member_list)
        else:
            QMessageBox.critical(self, '错误', f"获取成员列表失败: {response['message']}")
    
    def on_leave_group(self, group_id: int):
        """退出群组"""
        reply = QMessageBox.question(
            self, '确认', '确定要退出该群组吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            response = self.api_client.leave_group(group_id)
            
            if response['code'] == 200:
                QMessageBox.information(self, '成功', '已退出群组')
                self.load_groups()  # 重新加载群组列表
            else:
                QMessageBox.critical(self, '失败', f"退出群组失败: {response['message']}")
    
    def on_logout(self):
        """退出登录"""
        reply = QMessageBox.question(
            self, '确认', '确定要退出登录吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 断开WebSocket
            self.socket_client.disconnect_from_server()
            
            # 清除Token
            Storage.clear_token()
            
            # 关闭主窗口
            self.close()
            
            # 重新打开登录窗口
            from .login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
    
    def on_about(self):
        """关于"""
        QMessageBox.about(
            self,
            '关于',
            f'{Config.APP_NAME}\n版本: {Config.APP_VERSION}\n\n'
            '一个基于Flask和PySide6的聊天室应用'
        )
    
    def closeEvent(self, event):
        """关闭事件"""
        # 断开WebSocket
        self.socket_client.disconnect_from_server()
        event.accept()
