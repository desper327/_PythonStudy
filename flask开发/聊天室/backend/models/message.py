"""
消息模型
定义消息表结构和相关方法
"""
from datetime import datetime
from .user import db


class Message(db.Model):
    """消息模型类"""
    
    __tablename__ = 'messages'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='消息ID')
    
    # 发送者（必填）
    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment='发送者ID'
    )
    
    # 接收者（私聊消息）
    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment='接收者ID'
    )
    
    # 群组（群组消息）
    group_id = db.Column(
        db.Integer,
        db.ForeignKey('groups.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment='群组ID'
    )
    
    # 消息类型
    message_type = db.Column(
        db.Enum('text', 'image', 'file', name='message_type'),
        default='text',
        nullable=False,
        comment='消息类型'
    )
    
    # 消息内容
    content = db.Column(db.Text, nullable=False, comment='消息内容')
    
    # 已读状态（仅私聊消息）
    is_read = db.Column(db.Boolean, default=False, nullable=False, comment='是否已读')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True, comment='发送时间')
    
    def __repr__(self):
        """字符串表示"""
        if self.receiver_id:
            return f'<Message from={self.sender_id} to={self.receiver_id}>'
        else:
            return f'<Message from={self.sender_id} group={self.group_id}>'
    
    def to_dict(self):
        """
        转换为字典（用于JSON序列化）
        
        Returns:
            dict: 消息信息字典
        """
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.nickname if self.sender else None,
            'sender_avatar': self.sender.avatar if self.sender else None,
            'receiver_id': self.receiver_id,
            'receiver_name': self.receiver.nickname if self.receiver else None,
            'group_id': self.group_id,
            'group_name': self.group.name if self.group else None,
            'message_type': self.message_type,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    @property
    def is_private(self):
        """
        判断是否是私聊消息
        
        Returns:
            bool: 是否是私聊消息
        """
        return self.receiver_id is not None
    
    @property
    def is_group(self):
        """
        判断是否是群组消息
        
        Returns:
            bool: 是否是群组消息
        """
        return self.group_id is not None
    
    @staticmethod
    def validate_content(content):
        """
        验证消息内容
        
        Args:
            content: 消息内容
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not content:
            return False, "消息内容不能为空"
        if len(content) > 10000:
            return False, "消息内容过长（最多10000字符）"
        return True, ""
