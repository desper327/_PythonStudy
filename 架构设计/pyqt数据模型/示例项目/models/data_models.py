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

class TaskRepository:
    """任务仓库 - 管理任务数据的业务逻辑"""
    
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1
    
    def add_task(self, task_data: dict) -> Task:
        """添加新任务"""
        task = Task(**task_data)
        task.id = self._next_id
        self._next_id += 1
        self._tasks.append(task)
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        return self._tasks.copy()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, updates: dict) -> bool:
        """更新任务"""
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in updates.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """删除任务"""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """根据状态获取任务"""
        return [task for task in self._tasks if task.status == status]