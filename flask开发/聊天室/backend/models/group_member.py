"""
群组成员模型
定义群组成员关系表结构和相关方法
"""
from datetime import datetime
from .user import db


class GroupMember(db.Model):
    """群组成员模型类"""
    
    __tablename__ = 'group_members'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='成员记录ID')
    
    # 外键
    group_id = db.Column(
        db.Integer,
        db.ForeignKey('groups.id', ondelete='CASCADE'),
        nullable=False,
        comment='群组ID'
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        comment='用户ID'
    )
    
    # 成员角色
    role = db.Column(
        db.Enum('owner', 'admin', 'member', name='member_role'),
        default='member',
        nullable=False,
        comment='成员角色'
    )
    
    # 时间戳
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, comment='加入时间')
    
    # 联合唯一索引：一个用户在一个群组中只能有一条记录
    __table_args__ = (
        db.UniqueConstraint('group_id', 'user_id', name='uk_group_user'),
        db.Index('idx_group_id', 'group_id'),
        db.Index('idx_user_id', 'user_id'),
    )
    
    def __repr__(self):
        """字符串表示"""
        return f'<GroupMember user={self.user_id} group={self.group_id} role={self.role}>'
    
    def to_dict(self):
        """
        转换为字典（用于JSON序列化）
        
        Returns:
            dict: 成员信息字典
        """
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'nickname': self.user.nickname if self.user else None,
            'avatar': self.user.avatar if self.user else None,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
        }
