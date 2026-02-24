"""
业务数据模型 - 使用Pydantic进行数据验证
这些模型独立于UI框架，可以在任何地方使用
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable

from pydantic import BaseModel

@dataclass
class SignalData():
    """信号数据模型"""
    signal_type: str
    params: Dict[str, Any]


@dataclass
class TextData():
    """文本数据模型"""
    text: str = 'default'

