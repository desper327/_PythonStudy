"""
数据模型定义
"""
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
from datetime import datetime
from enum import Enum


class VariableOperation(Enum):
    """变量操作类型"""
    CREATE = "创建"
    MODIFY = "修改"
    DELETE = "删除"


@dataclass
class VariableChange:
    """变量变化记录"""
    name: str
    operation: VariableOperation
    old_value: Any
    new_value: Any
    line_no: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __repr__(self):
        return f"VariableChange({self.name}: {self.old_value} -> {self.new_value})"


@dataclass
class FunctionCall:
    """函数调用记录"""
    call_id: str
    function_name: str
    module_name: str
    package_name: str
    file_path: str
    line_no: int
    args: tuple
    kwargs: dict
    return_value: Any = None
    exception: Optional[Exception] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    parent_call_id: Optional[str] = None
    children_call_ids: List[str] = field(default_factory=list)
    variable_changes: List[VariableChange] = field(default_factory=list)
    depth: int = 0
    is_async: bool = False
    
    @property
    def duration_ms(self) -> float:
        """执行时长（毫秒）"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0
    
    @property
    def full_name(self) -> str:
        """完整函数名（包含模块）"""
        if self.package_name:
            return f"{self.package_name}.{self.module_name}.{self.function_name}"
        return f"{self.module_name}.{self.function_name}"
    
    def __repr__(self):
        return f"FunctionCall({self.full_name}, duration={self.duration_ms:.2f}ms)"


@dataclass
class TraceSession:
    """追踪会话"""
    session_id: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    function_calls: List[FunctionCall] = field(default_factory=list)
    call_map: Dict[str, FunctionCall] = field(default_factory=dict)
    
    @property
    def total_duration_ms(self) -> float:
        """总执行时长（毫秒）"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0
    
    @property
    def total_calls(self) -> int:
        """总调用次数"""
        return len(self.function_calls)
    
    def get_root_calls(self) -> List[FunctionCall]:
        """获取根级调用（没有父调用的）"""
        return [call for call in self.function_calls if call.parent_call_id is None]
    
    def get_modules(self) -> List[str]:
        """获取所有追踪的模块"""
        modules = set()
        for call in self.function_calls:
            modules.add(call.module_name)
        return sorted(list(modules))
    
    def get_functions(self) -> List[str]:
        """获取所有追踪的函数"""
        functions = set()
        for call in self.function_calls:
            functions.add(call.full_name)
        return sorted(list(functions))
