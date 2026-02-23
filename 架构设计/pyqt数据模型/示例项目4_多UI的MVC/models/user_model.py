"""
用户数据模型
示例业务模型，展示如何使用基础模型类
"""
from typing import Optional, List
from pydantic import Field, EmailStr, validator
from beartype import beartype
from .base_model import BaseDataModel


class UserModel(BaseDataModel):
    """
    用户数据模型
    继承自BaseDataModel，包含用户相关的所有字段和验证逻辑
    """
    
    # 用户基本信息
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(default=None, description="邮箱地址")
    full_name: Optional[str] = Field(default=None, max_length=100, description="全名")
    age: Optional[int] = Field(default=None, ge=0, le=150, description="年龄")
    is_active: bool = Field(default=True, description="是否激活")
    
    # 用户权限和角色
    roles: List[str] = Field(default_factory=list, description="用户角色列表")
    permissions: List[str] = Field(default_factory=list, description="用户权限列表")
    
    # 用户统计信息
    login_count: int = Field(default=0, ge=0, description="登录次数")
    last_login: Optional[str] = Field(default=None, description="最后登录时间")
    
    @validator('username')
    @beartype
    def validate_username(cls, v: str) -> str:
        """
        验证用户名格式
        
        Args:
            v: 用户名
            
        Returns:
            str: 验证后的用户名
            
        Raises:
            ValueError: 用户名格式不正确
        """
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v.lower()
    
    @validator('roles')
    @beartype
    def validate_roles(cls, v: List[str]) -> List[str]:
        """
        验证用户角色
        
        Args:
            v: 角色列表
            
        Returns:
            List[str]: 验证后的角色列表
        """
        valid_roles = ['admin', 'user', 'guest', 'moderator']
        for role in v:
            if role not in valid_roles:
                raise ValueError(f'无效的角色: {role}')
        return v
    
    @beartype
    def add_role(self, role: str) -> None:
        """
        添加用户角色
        
        Args:
            role: 要添加的角色
        """
        if role not in self.roles:
            self.roles.append(role)
            self.update_timestamp()
    
    @beartype
    def remove_role(self, role: str) -> None:
        """
        移除用户角色
        
        Args:
            role: 要移除的角色
        """
        if role in self.roles:
            self.roles.remove(role)
            self.update_timestamp()
    
    @beartype
    def has_role(self, role: str) -> bool:
        """
        检查用户是否具有指定角色
        
        Args:
            role: 要检查的角色
            
        Returns:
            bool: 是否具有该角色
        """
        return role in self.roles
    
    @beartype
    def increment_login_count(self) -> None:
        """
        增加登录次数
        """
        self.login_count += 1
        self.last_login = str(self.updated_at)
        self.update_timestamp()
    
    @beartype
    def deactivate(self) -> None:
        """
        停用用户
        """
        self.is_active = False
        self.update_timestamp()
    
    @beartype
    def activate(self) -> None:
        """
        激活用户
        """
        self.is_active = True
        self.update_timestamp()


class UserListModel(BaseDataModel):
    """
    用户列表模型
    用于管理多个用户数据
    """
    
    users: List[UserModel] = Field(default_factory=list, description="用户列表")
    total_count: int = Field(default=0, description="总用户数")
    active_count: int = Field(default=0, description="活跃用户数")
    
    @beartype
    def add_user(self, user: UserModel) -> None:
        """
        添加用户
        
        Args:
            user: 用户模型实例
        """
        self.users.append(user)
        self._update_counts()
    
    @beartype
    def remove_user(self, user_id: int) -> bool:
        """
        移除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 是否成功移除
        """
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                self._update_counts()
                return True
        return False
    
    @beartype
    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        根据ID获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[UserModel]: 用户模型实例或None
        """
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    @beartype
    def get_active_users(self) -> List[UserModel]:
        """
        获取所有活跃用户
        
        Returns:
            List[UserModel]: 活跃用户列表
        """
        return [user for user in self.users if user.is_active]
    
    @beartype
    def _update_counts(self) -> None:
        """
        更新用户统计数据
        """
        self.total_count = len(self.users)
        self.active_count = len([user for user in self.users if user.is_active])
        self.update_timestamp()
