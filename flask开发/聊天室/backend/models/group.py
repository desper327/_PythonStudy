"""
群组模型
定义群组表结构和相关方法
"""
from datetime import datetime
from .user import db


class Group(db.Model):
    """群组模型类"""
    
    __tablename__ = 'groups'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='群组ID')
    
    # 基本信息
    name = db.Column(db.String(50), unique=True, nullable=False, index=True, comment='群组名称')
    description = db.Column(db.Text, nullable=True, comment='群组描述')
    
    # 群组类型
    type = db.Column(
        db.Enum('public', 'private', name='group_type'),
        default='public',
        nullable=False,
        comment='群组类型'
    )
    
    # 群主
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        comment='群主ID'
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
    # 群组消息
    messages = db.relationship('Message', backref='group', lazy='dynamic')
    # 群组成员（通过group_member表）
    members = db.relationship('GroupMember', backref='group', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        """字符串表示"""
        return f'<Group {self.name}>'
    
    def to_dict(self, include_members=False):
        """
        转换为字典（用于JSON序列化）
        
        Args:
            include_members: 是否包含成员列表
            
        Returns:
            dict: 群组信息字典
        """
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'owner_id': self.owner_id,
            'owner_name': self.owner.nickname if self.owner else None,
            'member_count': self.members.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        # 根据需要包含成员列表
        if include_members:
            data['members'] = [member.to_dict() for member in self.members]
            
        return data
    
    def is_member(self, user_id):
        """
        检查用户是否是群组成员
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 是否是成员
        """
        return self.members.filter_by(user_id=user_id).first() is not None
    
    def is_owner(self, user_id):
        """
        检查用户是否是群主
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 是否是群主
        """
        return self.owner_id == user_id
    
    def is_admin(self, user_id):
        """
        检查用户是否是管理员（包括群主）
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 是否是管理员
        """
        if self.is_owner(user_id):
            return True
        
        member = self.members.filter_by(user_id=user_id).first()
        return member and member.role == 'admin'
    
    @staticmethod
    def validate_name(name):
        """
        验证群组名称格式
        
        Args:
            name: 群组名称
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not name:
            return False, "群组名称不能为空"
        if len(name) < 2 or len(name) > 30:
            return False, "群组名称长度必须在2-30个字符之间"
        return True, ""
