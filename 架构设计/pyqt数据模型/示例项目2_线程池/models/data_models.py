"""
业务数据模型 - 使用Pydantic进行数据验证
这些模型独立于UI框架，可以在任何地方使用
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"

class Task(BaseModel):
    """任务数据模型"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100, description="任务名称")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        """验证任务名称不能为空或只包含空格"""
        if not v or not v.strip():
            raise ValueError('任务名称不能为空')
        return v.strip()
    
    @field_validator('completed_at')
    def validate_completion_time(cls, v, values):
        """验证完成时间逻辑"""
        if v and values.get('status') != TaskStatus.COMPLETED:
            raise ValueError('只有已完成的任务才能有完成时间')
        return v
    
    def mark_completed(self):
        """标记任务为已完成"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def mark_in_progress(self):
        """标记任务为进行中"""
        self.status = TaskStatus.IN_PROGRESS
        self.completed_at = None
    
    def mark_pending(self):
        """标记任务为待处理"""
        self.status = TaskStatus.PENDING
        self.completed_at = None