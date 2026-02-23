"""
业务数据模型 - 使用Pydantic进行数据验证
这些模型独立于UI框架，可以在任何地方使用
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable
from pydantic import BaseModel, Field, field_validator


class SignalData(BaseModel):
    """信号数据模型"""
    signal_type: str
    params: Dict[str, Any]


@dataclass
class TaskSpec:
    func: Callable[..., Any]
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = field(default_factory=dict)
    return_result: bool = False


class TextData(BaseModel):
    """任务数据模型"""
    text: str = 'default'
    
    @field_validator('text')
    def name_must_not_be_empty(cls, v):
        """验证文本不能为空或只包含空格"""
        if not v or not v.strip():
            raise ValueError('文本不能为空')
        return v.strip()
    
