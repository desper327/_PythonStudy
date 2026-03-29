"""
变量追踪器
使用 sys.settrace() 实现行级变量变化追踪
"""
import sys
import copy
from typing import Any, Dict, Callable, Optional
from datetime import datetime

from .models import VariableChange, VariableOperation


class VariableTracker:
    """变量追踪器，追踪函数内局部变量的变化"""
    
    def __init__(self, on_change_callback: Optional[Callable[[VariableChange], None]] = None):
        """
        初始化变量追踪器
        
        Args:
            on_change_callback: 变量变化时的回调函数
        """
        self._previous_locals: Dict[str, Any] = {}
        self._on_change = on_change_callback
        self._changes: list = []
        self._enabled = False
        self._target_frame = None
        
    def start(self, frame) -> None:
        """开始追踪指定栈帧的变量"""
        self._target_frame = frame
        self._previous_locals = self._safe_copy_locals(frame.f_locals)
        self._changes = []
        self._enabled = True
        
    def stop(self) -> list:
        """停止追踪，返回所有变化记录"""
        self._enabled = False
        self._target_frame = None
        changes = self._changes.copy()
        self._changes = []
        return changes
    
    def _safe_copy_locals(self, locals_dict: dict) -> dict:
        """安全地复制局部变量字典"""
        result = {}
        for key, value in locals_dict.items():
            if key.startswith('_'):  # 跳过私有变量
                continue
            try:
                # 尝试深拷贝
                result[key] = copy.deepcopy(value)
            except (TypeError, copy.Error):
                # 无法深拷贝的对象，保存其字符串表示
                try:
                    result[key] = repr(value)
                except:
                    result[key] = "<不可复制对象>"
        return result
    
    def _safe_repr(self, value: Any) -> str:
        """安全地获取值的字符串表示"""
        try:
            s = repr(value)
            # 限制长度
            if len(s) > 200:
                return s[:200] + "..."
            return s
        except:
            return "<无法表示>"
    
    def trace_callback(self, frame, event, arg) -> Optional[Callable]:
        """
        sys.settrace 的回调函数
        
        Args:
            frame: 当前栈帧
            event: 事件类型 ('call', 'line', 'return', 'exception')
            arg: 事件参数
        """
        if not self._enabled:
            return None
            
        # 只追踪目标栈帧
        if frame is not self._target_frame:
            return self.trace_callback
            
        if event == 'line':
            self._check_variable_changes(frame)
            
        return self.trace_callback
    
    def _check_variable_changes(self, frame) -> None:
        """检查变量变化"""
        current_locals = frame.f_locals
        line_no = frame.f_lineno
        
        # 检查新增和修改的变量
        for name, value in current_locals.items():
            if name.startswith('_'):  # 跳过私有变量
                continue
                
            if name not in self._previous_locals:
                # 新创建的变量
                change = VariableChange(
                    name=name,
                    operation=VariableOperation.CREATE,
                    old_value=None,
                    new_value=self._safe_repr(value),
                    line_no=line_no
                )
                self._changes.append(change)
                if self._on_change:
                    self._on_change(change)
            else:
                # 检查是否被修改
                try:
                    old_value = self._previous_locals[name]
                    # 使用字符串比较，避免复杂对象的比较问题
                    if self._safe_repr(value) != self._safe_repr(old_value):
                        change = VariableChange(
                            name=name,
                            operation=VariableOperation.MODIFY,
                            old_value=self._safe_repr(old_value) if not isinstance(old_value, str) else old_value,
                            new_value=self._safe_repr(value),
                            line_no=line_no
                        )
                        self._changes.append(change)
                        if self._on_change:
                            self._on_change(change)
                except:
                    pass
        
        # 检查删除的变量
        for name in list(self._previous_locals.keys()):
            if name not in current_locals:
                change = VariableChange(
                    name=name,
                    operation=VariableOperation.DELETE,
                    old_value=self._safe_repr(self._previous_locals[name]),
                    new_value=None,
                    line_no=line_no
                )
                self._changes.append(change)
                if self._on_change:
                    self._on_change(change)
        
        # 更新前一状态
        self._previous_locals = self._safe_copy_locals(current_locals)
