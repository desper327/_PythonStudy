"""
聊天WebSocket事件处理
处理实时消息发送和接收
"""
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask import request
from models import Message, Group, User
from models.user import db
from utils.auth import verify_token

# 存储在线用户 {user_id: session_id}
online_users = {}


def register_socket_events(socketio: SocketIO):
    """
    注册所有Socket事件
    
    Args:
        socketio: SocketIO实例
    """
    
    @socketio.on('connect')
    def handle_connect():
        """客户端连接事件"""
        print(f'Client connected: {request.sid}')
        emit('connected', {'message': '连接成功，请先认证'})
    
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """客户端断开连接事件"""
        print(f'Client disconnected: {request.sid}')
        
        # 从在线用户列表中移除
        user_id = None
        for uid, sid in list(online_users.items()):
            if sid == request.sid:
                user_id = uid
                del online_users[uid]
                break
        
        # 广播用户下线消息
        if user_id:
            emit('user_offline', {'user_id': user_id}, broadcast=True)
    
    
    @socketio.on('authenticate')
    def handle_authenticate(data):
        """
        认证事件
        
        数据格式:
            {
                "token": "jwt_token"
            }
        """
        try:
            token = data.get('token')
            
            if not token:
                emit('error', {'message': '缺少token'})
                return
            
            # 验证token
            payload = verify_token(token)
            if not payload:
                emit('error', {'message': 'token无效或已过期'})
                disconnect()
                return
            
            user_id = payload.get('user_id')
            username = payload.get('username')
            
            # 保存用户session
            online_users[user_id] = request.sid
            
            # 加入用户个人房间（用于接收私聊消息）
            join_room(f'user_{user_id}')
            
            print(f'User authenticated: {username} (ID: {user_id})')
            
            # 发送认证成功消息
            emit('authenticated', {
                'user_id': user_id,
                'username': username,
                'message': '认证成功'
            })
            
            # 广播用户上线消息
            emit('user_online', {'user_id': user_id, 'username': username}, broadcast=True)
            
        except Exception as e:
            emit('error', {'message': f'认证失败: {str(e)}'})
            disconnect()
    
    
    @socketio.on('send_private_message')
    def handle_private_message(data):
        """
        发送私聊消息事件
        
        数据格式:
            {
                "receiver_id": 1,
                "content": "消息内容"
            }
        """
        try:
            # 获取当前用户ID（从session中）
            sender_id = None
            for uid, sid in online_users.items():
                if sid == request.sid:
                    sender_id = uid
                    break
            
            if not sender_id:
                emit('error', {'message': '请先认证'})
                return
            
            receiver_id = data.get('receiver_id')
            content = data.get('content', '').strip()
            
            # 验证数据
            if not receiver_id:
                emit('error', {'message': '缺少接收者ID'})
                return
            
            valid, msg = Message.validate_content(content)
            if not valid:
                emit('error', {'message': msg})
                return
            
            # 检查接收者是否存在
            receiver = User.query.get(receiver_id)
            if not receiver or receiver.status != 'active':
                emit('error', {'message': '接收者不存在或已被禁用'})
                return
            
            # 创建消息记录
            message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_type='text',
                content=content
            )
            db.session.add(message)
            db.session.commit()
            
            # 转换为字典
            message_data = message.to_dict()
            
            # 发送给接收者（如果在线）
            emit('new_private_message', message_data, room=f'user_{receiver_id}')
            
            # 发送确认给发送者
            emit('message_sent', {
                'message_id': message.id,
                'message': message_data
            })
            
            print(f'Private message: {sender_id} -> {receiver_id}')
            
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': f'发送消息失败: {str(e)}'})
    
    
    @socketio.on('send_group_message')
    def handle_group_message(data):
        """
        发送群组消息事件
        
        数据格式:
            {
                "group_id": 1,
                "content": "消息内容"
            }
        """
        try:
            # 获取当前用户ID
            sender_id = None
            for uid, sid in online_users.items():
                if sid == request.sid:
                    sender_id = uid
                    break
            
            if not sender_id:
                emit('error', {'message': '请先认证'})
                return
            
            group_id = data.get('group_id')
            content = data.get('content', '').strip()
            
            # 验证数据
            if not group_id:
                emit('error', {'message': '缺少群组ID'})
                return
            
            valid, msg = Message.validate_content(content)
            if not valid:
                emit('error', {'message': msg})
                return
            
            # 检查群组是否存在
            group = Group.query.get(group_id)
            if not group:
                emit('error', {'message': '群组不存在'})
                return
            
            # 检查是否是群组成员
            if not group.is_member(sender_id):
                emit('error', {'message': '您不是该群组成员'})
                return
            
            # 创建消息记录
            message = Message(
                sender_id=sender_id,
                group_id=group_id,
                message_type='text',
                content=content
            )
            db.session.add(message)
            db.session.commit()
            
            # 转换为字典
            message_data = message.to_dict()
            
            # 广播给群组所有成员
            emit('new_group_message', message_data, room=f'group_{group_id}')
            
            # 发送确认给发送者
            emit('message_sent', {
                'message_id': message.id,
                'message': message_data
            })
            
            print(f'Group message: {sender_id} -> group {group_id}')
            
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': f'发送消息失败: {str(e)}'})
    
    
    @socketio.on('join_group_room')
    def handle_join_group_room(data):
        """
        加入群组房间（用于接收群组消息）
        
        数据格式:
            {
                "group_id": 1
            }
        """
        try:
            # 获取当前用户ID
            user_id = None
            for uid, sid in online_users.items():
                if sid == request.sid:
                    user_id = uid
                    break
            
            if not user_id:
                emit('error', {'message': '请先认证'})
                return
            
            group_id = data.get('group_id')
            
            if not group_id:
                emit('error', {'message': '缺少群组ID'})
                return
            
            # 检查群组是否存在
            group = Group.query.get(group_id)
            if not group:
                emit('error', {'message': '群组不存在'})
                return
            
            # 检查是否是群组成员
            if not group.is_member(user_id):
                emit('error', {'message': '您不是该群组成员'})
                return
            
            # 加入群组房间
            join_room(f'group_{group_id}')
            
            emit('joined_group_room', {'group_id': group_id})
            print(f'User {user_id} joined group room {group_id}')
            
        except Exception as e:
            emit('error', {'message': f'加入群组房间失败: {str(e)}'})
    
    
    @socketio.on('leave_group_room')
    def handle_leave_group_room(data):
        """
        离开群组房间
        
        数据格式:
            {
                "group_id": 1
            }
        """
        try:
            group_id = data.get('group_id')
            
            if not group_id:
                emit('error', {'message': '缺少群组ID'})
                return
            
            # 离开群组房间
            leave_room(f'group_{group_id}')
            
            emit('left_group_room', {'group_id': group_id})
            
        except Exception as e:
            emit('error', {'message': f'离开群组房间失败: {str(e)}'})
