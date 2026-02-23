"""
用户模型
定义用户表结构和相关方法
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    """用户模型类"""
    
    __tablename__ = 'users'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    
    # 基本信息
    username = db.Column(db.String(50), unique=True, nullable=False, index=True, comment='用户名')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    nickname = db.Column(db.String(50), nullable=False, comment='昵称')
    email = db.Column(db.String(100), unique=True, nullable=True, comment='邮箱')
    avatar = db.Column(db.String(255), nullable=True, comment='头像URL')
    
    # 用户状态
    status = db.Column(
        db.Enum('active', 'banned', 'deleted', name='user_status'),
        default='active',
        nullable=False,
        comment='用户状态'
    )
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment='更新时间'
    )
    
    # 关系
    # 发送的消息
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    # 接收的消息
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    # 创建的群组
    owned_groups = db.relationship('Group', backref='owner', lazy='dynamic')
    # 加入的群组（通过group_member表）
    group_memberships = db.relationship('GroupMember', backref='user', lazy='dynamic')
    
    def __repr__(self):
        """字符串表示"""
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        设置密码（加密存储）
        
        Args:
            password: 明文密码
        """
        # 使用bcrypt加密密码
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """
        验证密码
        
        Args:
            password: 待验证的明文密码
            
        Returns:
            bool: 密码是否正确
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self, include_email=False):
        """
        转换为字典（用于JSON序列化）
        
        Args:
            include_email: 是否包含邮箱（隐私信息）
            
        Returns:
            dict: 用户信息字典
        """
        data = {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        # 根据需要包含邮箱
        if include_email:
            data['email'] = self.email
            
        return data
    
    @staticmethod
    def validate_username(username):
        """
        验证用户名格式
        
        Args:
            username: 用户名
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not username:
            return False, "用户名不能为空"
        if len(username) < 3 or len(username) > 50:
            return False, "用户名长度必须在3-50个字符之间"
        if not username.isalnum():
            return False, "用户名只能包含字母和数字"
        return True, ""
    
    @staticmethod
    def validate_password(password):
        """
        验证密码强度
        
        Args:
            password: 密码
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not password:
            return False, "密码不能为空"
        if len(password) < 6:
            return False, "密码长度至少为6个字符"
        return True, ""
