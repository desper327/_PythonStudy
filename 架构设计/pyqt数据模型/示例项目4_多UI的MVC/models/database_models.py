"""
SQLAlchemy数据库模型
定义数据库表结构和ORM映射
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from beartype import beartype

# 创建基础模型类
Base = declarative_base()


class BaseDBModel(Base):
    """
    基础数据库模型类
    包含所有表的公共字段
    """
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        nullable=False, 
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        onupdate=func.now(), 
        nullable=False, 
        comment="更新时间"
    )


class UserDB(BaseDBModel):
    """
    用户数据库模型
    对应users表
    """
    __tablename__ = 'users'
    
    # 基本信息字段
    username: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False, 
        index=True, 
        comment="用户名"
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(100), 
        unique=True, 
        nullable=True, 
        index=True, 
        comment="邮箱地址"
    )
    full_name: Mapped[Optional[str]] = mapped_column(
        String(100), 
        nullable=True, 
        comment="全名"
    )
    age: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        comment="年龄"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        nullable=False, 
        comment="是否激活"
    )
    
    # JSON字段存储复杂数据
    roles: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="用户角色列表"
    )
    permissions: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="用户权限列表"
    )
    
    # 统计字段
    login_count: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False, 
        comment="登录次数"
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True, 
        comment="最后登录时间"
    )
    
    # 关系映射
    tasks: Mapped[List["TaskDB"]] = relationship(
        "TaskDB", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<UserDB(id={self.id}, username='{self.username}', email='{self.email}')>"


class TaskDB(BaseDBModel):
    """
    任务数据库模型
    对应tasks表
    """
    __tablename__ = 'tasks'
    
    # 基本信息字段
    title: Mapped[str] = mapped_column(
        String(200), 
        nullable=False, 
        comment="任务标题"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="任务描述"
    )
    status: Mapped[str] = mapped_column(
        String(20), 
        default="pending", 
        nullable=False, 
        index=True, 
        comment="任务状态"
    )
    priority: Mapped[int] = mapped_column(
        Integer, 
        default=1, 
        nullable=False, 
        comment="任务优先级"
    )
    
    # 外键关系
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=True, 
        comment="关联用户ID"
    )
    
    # 任务相关字段
    start_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True, 
        comment="开始时间"
    )
    end_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True, 
        comment="结束时间"
    )
    progress: Mapped[float] = mapped_column(
        Integer, 
        default=0, 
        nullable=False, 
        comment="任务进度"
    )
    
    # JSON字段存储任务参数和结果
    parameters: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="任务参数"
    )
    result: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="任务结果"
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="错误信息"
    )
    
    # 关系映射
    user: Mapped[Optional["UserDB"]] = relationship(
        "UserDB", 
        back_populates="tasks"
    )
    
    def __repr__(self) -> str:
        return f"<TaskDB(id={self.id}, title='{self.title}', status='{self.status}')>"


class DataRecordDB(BaseDBModel):
    """
    数据记录数据库模型
    用于存储各种数据处理记录
    """
    __tablename__ = 'data_records'
    
    # 基本信息字段
    record_type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False, 
        index=True, 
        comment="记录类型"
    )
    name: Mapped[str] = mapped_column(
        String(200), 
        nullable=False, 
        comment="记录名称"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="记录描述"
    )
    
    # 数据字段
    data: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="数据内容"
    )
    record_metadata: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="元数据"
    )
    
    # 状态字段
    status: Mapped[str] = mapped_column(
        String(20), 
        default="active", 
        nullable=False, 
        comment="记录状态"
    )
    version: Mapped[int] = mapped_column(
        Integer, 
        default=1, 
        nullable=False, 
        comment="版本号"
    )
    
    def __repr__(self) -> str:
        return f"<DataRecordDB(id={self.id}, type='{self.record_type}', name='{self.name}')>"


class LogEntryDB(BaseDBModel):
    """
    日志条目数据库模型
    用于存储应用程序日志
    """
    __tablename__ = 'log_entries'
    
    # 日志基本信息
    level: Mapped[str] = mapped_column(
        String(10), 
        nullable=False, 
        index=True, 
        comment="日志级别"
    )
    message: Mapped[str] = mapped_column(
        Text, 
        nullable=False, 
        comment="日志消息"
    )
    module: Mapped[Optional[str]] = mapped_column(
        String(100), 
        nullable=True, 
        comment="模块名称"
    )
    function: Mapped[Optional[str]] = mapped_column(
        String(100), 
        nullable=True, 
        comment="函数名称"
    )
    line_number: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        comment="行号"
    )
    
    # 上下文信息
    context: Mapped[Optional[dict]] = mapped_column(
        JSON, 
        nullable=True, 
        comment="上下文信息"
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        comment="关联用户ID"
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(100), 
        nullable=True, 
        comment="会话ID"
    )
    
    def __repr__(self) -> str:
        return f"<LogEntryDB(id={self.id}, level='{self.level}', message='{self.message[:50]}...')>"


class ConfigDB(BaseDBModel):
    """
    配置数据库模型
    用于存储应用程序配置
    """
    __tablename__ = 'configs'
    
    # 配置基本信息
    key: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True, 
        comment="配置键"
    )
    value: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="配置值"
    )
    value_type: Mapped[str] = mapped_column(
        String(20), 
        default="string", 
        nullable=False, 
        comment="值类型"
    )
    
    # 配置元信息
    category: Mapped[Optional[str]] = mapped_column(
        String(50), 
        nullable=True, 
        index=True, 
        comment="配置分类"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        comment="配置描述"
    )
    is_system: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False, 
        comment="是否为系统配置"
    )
    is_encrypted: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False, 
        comment="是否加密存储"
    )
    
    def __repr__(self) -> str:
        return f"<ConfigDB(id={self.id}, key='{self.key}', category='{self.category}')>"
