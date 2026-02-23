"""
WebSocket客户端
用于实时消息通信
"""
import socketio
from typing import Callable, Optional
from PySide6.QtCore import QObject, Signal
from config import Config


class SocketClient(QObject):
    """WebSocket客户端类（集成Qt信号）"""
    
    # Qt信号
    connected = Signal()                    # 连接成功
    disconnected = Signal()                 # 断开连接
    authenticated = Signal(dict)            # 认证成功
    error_occurred = Signal(str)            # 错误
    new_private_message = Signal(dict)      # 新私聊消息
    new_group_message = Signal(dict)        # 新群组消息
    message_sent = Signal(dict)             # 消息发送成功
    user_online = Signal(dict)              # 用户上线
    user_offline = Signal(dict)             # 用户下线
    
    def __init__(self):
        """初始化WebSocket客户端"""
        super().__init__()
        
        self.server_url = Config.SOCKET_HOST
        self.sio = socketio.Client()
        self.is_connected = False
        
        # 注册事件处理器
        self._register_handlers()
    
    def _register_handlers(self):
        """注册事件处理器"""
        
        @self.sio.event
        def connect():
            """连接事件"""
            print('WebSocket连接成功')
            self.is_connected = True
            self.connected.emit()
        
        @self.sio.event
        def disconnect():
            """断开连接事件"""
            print('WebSocket连接断开')
            self.is_connected = False
            self.disconnected.emit()
        
        @self.sio.event
        def authenticated(data):
            """认证成功事件"""
            print(f"认证成功: {data}")
            self.authenticated.emit(data)
        
        @self.sio.event
        def error(data):
            """错误事件"""
            message = data.get('message', '未知错误')
            print(f"错误: {message}")
            self.error_occurred.emit(message)
        
        @self.sio.event
        def new_private_message(data):
            """新私聊消息事件"""
            print(f"收到私聊消息: {data}")
            self.new_private_message.emit(data)
        
        @self.sio.event
        def new_group_message(data):
            """新群组消息事件"""
            print(f"收到群组消息: {data}")
            self.new_group_message.emit(data)
        
        @self.sio.event
        def message_sent(data):
            """消息发送成功事件"""
            print(f"消息发送成功: {data}")
            self.message_sent.emit(data)
        
        @self.sio.event
        def user_online(data):
            """用户上线事件"""
            print(f"用户上线: {data}")
            self.user_online.emit(data)
        
        @self.sio.event
        def user_offline(data):
            """用户下线事件"""
            print(f"用户下线: {data}")
            self.user_offline.emit(data)
    
    def connect_to_server(self):
        """连接到服务器"""
        try:
            if not self.is_connected:
                print(f'正在连接到WebSocket服务器: {self.server_url}')
                self.sio.connect(self.server_url)
        except Exception as e:
            print(f'连接失败: {str(e)}')
            self.error_occurred.emit(f'连接失败: {str(e)}')
    
    def disconnect_from_server(self):
        """断开连接"""
        try:
            if self.is_connected:
                self.sio.disconnect()
        except Exception as e:
            print(f'断开连接失败: {str(e)}')
    
    def authenticate(self, token: str):
        """
        发送认证请求
        
        Args:
            token: JWT Token
        """
        self.sio.emit('authenticate', {'token': token})
    
    def send_private_message(self, receiver_id: int, content: str):
        """
        发送私聊消息
        
        Args:
            receiver_id: 接收者ID
            content: 消息内容
        """
        self.sio.emit('send_private_message', {
            'receiver_id': receiver_id,
            'content': content
        })
    
    def send_group_message(self, group_id: int, content: str):
        """
        发送群组消息
        
        Args:
            group_id: 群组ID
            content: 消息内容
        """
        self.sio.emit('send_group_message', {
            'group_id': group_id,
            'content': content
        })
    
    def join_group_room(self, group_id: int):
        """
        加入群组房间
        
        Args:
            group_id: 群组ID
        """
        self.sio.emit('join_group_room', {'group_id': group_id})
    
    def leave_group_room(self, group_id: int):
        """
        离开群组房间
        
        Args:
            group_id: 群组ID
        """
        self.sio.emit('leave_group_room', {'group_id': group_id})
