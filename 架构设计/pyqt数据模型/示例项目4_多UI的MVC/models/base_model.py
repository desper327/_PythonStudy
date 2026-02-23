"""
基础数据模型类
使用Pydantic进行数据验证，Beartype进行类型检查
"""
from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict
from beartype import beartype


class BaseDataModel(BaseModel):
    """
    基础数据模型类
    所有业务模型都应该继承此类
    """
    
    # Pydantic v2配置
    model_config = ConfigDict(
        # 允许额外字段
        extra='allow',
        # 验证赋值
        validate_assignment=True,
        # 使用枚举值
        use_enum_values=True,
        # 序列化时排除None值
        exclude_none=True
    )
    
    # 基础字段
    id: Optional[int] = Field(default=None, description="主键ID")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="创建时间")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="更新时间")
    
    @beartype
    def to_dict(self) -> Dict[str, Any]:
        """
        将模型转换为字典
        
        Returns:
            Dict[str, Any]: 模型的字典表示
        """
        return self.model_dump()
    
    @beartype
    def update_timestamp(self) -> None:
        """
        更新时间戳
        """
        self.updated_at = datetime.now()
    
    @classmethod
    @beartype
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseDataModel':
        """
        从字典创建模型实例
        
        Args:
            data: 数据字典
            
        Returns:
            BaseDataModel: 模型实例
        """
        return cls(**data)


class TaskStatus(BaseModel):
    """
    任务状态模型
    用于跟踪异步/线程任务的执行状态
    """
    
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True
    )
    
    task_id: str = Field(..., description="任务ID")
    status: str = Field(default="pending", description="任务状态: pending, running, completed, failed")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="任务进度百分比")
    message: Optional[str] = Field(default=None, description="状态消息")
    result: Optional[Any] = Field(default=None, description="任务结果")
    error: Optional[str] = Field(default=None, description="错误信息")
    start_time: Optional[datetime] = Field(default=None, description="开始时间")
    end_time: Optional[datetime] = Field(default=None, description="结束时间")
    
    @beartype
    def mark_started(self) -> None:
        """标记任务开始"""
        self.status = "running"
        self.start_time = datetime.now()
    
    @beartype
    def mark_completed(self, result: Any = None) -> None:
        """标记任务完成"""
        self.status = "completed"
        self.progress = 100.0
        self.end_time = datetime.now()
        if result is not None:
            self.result = result
    
    @beartype
    def mark_failed(self, error: str) -> None:
        """标记任务失败"""
        self.status = "failed"
        self.end_time = datetime.now()
        self.error = error
    
    @beartype
    def update_progress(self, progress: float, message: Optional[str] = None) -> None:
        """更新任务进度"""
        self.progress = max(0.0, min(100.0, progress))
        if message:
            self.message = message


class UIState(BaseModel):
    """
    UI状态模型
    用于管理界面状态
    """
    
    model_config = ConfigDict(
        extra='allow',
        validate_assignment=True
    )
    
    window_title: str = Field(default="MVC Framework", description="窗口标题")
    is_loading: bool = Field(default=False, description="是否正在加载")
    status_message: str = Field(default="就绪", description="状态栏消息")
    current_view: str = Field(default="main", description="当前视图")
    dialog_open: bool = Field(default=False, description="是否有对话框打开")
    
    @beartype
    def set_loading(self, loading: bool, message: str = "") -> None:
        """设置加载状态"""
        self.is_loading = loading
        if message:
            self.status_message = message
    
    @beartype
    def set_status(self, message: str) -> None:
        """设置状态消息"""
        self.status_message = message
