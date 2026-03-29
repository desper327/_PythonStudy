"""
核心追踪逻辑 - 简化版
"""
import sys
import os
import uuid
import functools
import sysconfig
import site
from typing import Optional, Dict, Callable, Set
from datetime import datetime

from .models import FunctionCall, TraceSession


class Tracer:
    """
    函数追踪器
    
    用法:
        @Tracer.trace()  # 自动追踪内部调用的本地函数
        def main():
            helper()  # 会被自动追踪
            
        main()
        Tracer.generate_report()
    """
    
    _session: Optional[TraceSession] = None
    _call_stack: list = []
    _frame_call_map: Dict[int, FunctionCall] = {}
    _excluded_paths: Set[str] = set()
    _project_root: Optional[str] = None
    _old_trace: Optional[Callable] = None
    
    @classmethod
    def _init_excluded_paths(cls) -> Set[str]:
        """初始化排除路径（标准库、第三方库、tracer自身）"""
        excluded = set()
        
        # 标准库
        stdlib = sysconfig.get_path('stdlib')
        if stdlib:
            excluded.add(os.path.normpath(stdlib))
        
        # site-packages
        for p in site.getsitepackages():
            excluded.add(os.path.normpath(p))
        user_site = site.getusersitepackages()
        if user_site:
            excluded.add(os.path.normpath(user_site))
        
        # tracer 模块自身
        excluded.add(os.path.normpath(os.path.dirname(__file__)))
        
        return excluded
    
    @classmethod
    def _should_trace(cls, filename: str) -> bool:
        """判断文件是否应该被追踪"""
        if not filename or filename.startswith(('<frozen', '<built-in', '<string>')):
            return False
        
        try:
            path = os.path.normpath(os.path.abspath(filename))
        except (TypeError, OSError):
            return False
        
        # 检查排除路径
        for excluded in cls._excluded_paths:
            if path.startswith(excluded):
                return False
        
        # 检查是否在项目根目录下
        if cls._project_root and not path.startswith(cls._project_root):
            return False
        
        return True
    
    @classmethod
    def _trace_callback(cls, frame, event, arg):
        """sys.settrace 回调"""
        code = frame.f_code
        filename = code.co_filename
        
        if not cls._should_trace(filename):
            return None
        
        if event == 'call':
            parent = cls._call_stack[-1] if cls._call_stack else None
            call = FunctionCall(
                call_id=str(uuid.uuid4())[:8],
                function_name=code.co_name,
                module_name=frame.f_globals.get('__name__', '__main__'),
                package_name=frame.f_globals.get('__package__', '') or '',
                file_path=filename,
                line_no=code.co_firstlineno,
                args=cls._extract_args(frame, code),
                kwargs={},
                parent_call_id=parent.call_id if parent else None,
                depth=len(cls._call_stack),
                is_async=False
            )
            
            if parent:
                parent.children_call_ids.append(call.call_id)
            
            cls._call_stack.append(call)
            cls._frame_call_map[id(frame)] = call
            cls._record_call(call)  # 在调用开始时就记录，保证顺序正确
            return cls._trace_callback
        
        elif event == 'return':
            frame_id = id(frame)
            if frame_id in cls._frame_call_map:
                call = cls._frame_call_map.pop(frame_id)
                call.return_value = arg
                call.end_time = datetime.now()
                cls._call_stack.pop()
        
        return cls._trace_callback
    
    @classmethod
    def _extract_args(cls, frame, code) -> tuple:
        """提取函数参数"""
        args = []
        for name in code.co_varnames[:code.co_argcount]:
            if name in ('self', 'cls'):
                continue
            if name in frame.f_locals:
                val = frame.f_locals[name]
                args.append(val if isinstance(val, (int, float, str, bool, type(None))) else repr(val))
        return tuple(args)
    
    @classmethod
    def _record_call(cls, call: FunctionCall):
        """记录函数调用"""
        if cls._session:
            cls._session.function_calls.append(call)
            cls._session.call_map[call.call_id] = call
    
    @classmethod
    def _ensure_session(cls):
        """确保会话存在"""
        if not cls._session:
            cls._session = TraceSession(session_id=str(uuid.uuid4())[:8])
    
    @classmethod
    def reset(cls):
        """重置追踪器"""
        cls._session = None
        cls._call_stack.clear()
        cls._frame_call_map.clear()
        cls._project_root = None
    
    @classmethod
    def generate_report(cls, output_path: str = "trace_report.md") -> str:
        """生成追踪报告"""
        from .report_generator import ReportGenerator
        if not cls._session:
            raise ValueError("没有追踪会话")
        
        cls._session.end_time = datetime.now()
        report = ReportGenerator(cls._session).generate()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 追踪报告已生成: {output_path}")
        return report
    
    @classmethod
    def trace(cls, func: Optional[Callable] = None, *, deep: bool = True):
        """
        函数追踪装饰器
        
        Args:
            func: 被装饰的函数
            deep: 是否深度追踪（自动追踪内部调用的本地函数），默认True
        
        用法:
            @Tracer.trace()
            def main():
                helper()  # 会被自动追踪
        """
        def decorator(fn: Callable) -> Callable:
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                cls._ensure_session()
                cls._excluded_paths = cls._init_excluded_paths()
                
                # 获取函数所在目录作为项目根目录（如果未设置）
                if not cls._project_root:
                    try:
                        fn_file = os.path.abspath(fn.__code__.co_filename)
                        cls._project_root = os.path.normpath(os.path.dirname(fn_file))
                    except:
                        pass
                
                # 深度追踪：启用 sys.settrace
                if deep:
                    cls._old_trace = sys.gettrace()
                    sys.settrace(cls._trace_callback)
                
                try:
                    return fn(*args, **kwargs)
                finally:
                    if deep:
                        sys.settrace(cls._old_trace)
                        cls._old_trace = None
            
            return wrapper
        
        return decorator(func) if func else decorator


# 便捷别名
trace = Tracer.trace
