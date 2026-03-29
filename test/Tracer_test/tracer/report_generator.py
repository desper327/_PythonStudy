"""
MD报告生成器
"""
from datetime import datetime
from typing import List, Optional
from io import StringIO

from .models import TraceSession, FunctionCall, VariableChange, VariableOperation


class ReportGenerator:
    """追踪报告生成器"""
    
    def __init__(self, session: TraceSession):
        self.session = session
        self._buffer = StringIO()
    
    def generate(self) -> str:
        """生成完整的MD报告"""
        self._buffer = StringIO()
        
        self._write_header()
        self._write_summary()
        self._write_call_tree()
        self._write_timeline()
        self._write_variable_changes()
        self._write_detailed_logs()
        self._write_footer()
        
        return self._buffer.getvalue()
    
    def _write(self, text: str = "") -> None:
        """写入文本"""
        self._buffer.write(text + "\n")
    
    def _write_header(self) -> None:
        """写入报告头部"""
        self._write("# 🔍 Python 运行追踪报告")
        self._write()
        self._write(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._write(f"> 会话ID: `{self.session.session_id}`")
        self._write()
        self._write("---")
        self._write()
    
    def _write_summary(self) -> None:
        """写入执行摘要"""
        self._write("## 📊 执行摘要")
        self._write()
        
        # 基本统计
        self._write("### 基本信息")
        self._write()
        self._write("| 指标 | 值 |")
        self._write("|------|-----|")
        self._write(f"| 追踪开始时间 | {self.session.start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} |")
        
        end_time = self.session.end_time or datetime.now()
        self._write(f"| 追踪结束时间 | {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} |")
        self._write(f"| 总执行耗时 | {self.session.total_duration_ms:.2f} ms |")
        self._write(f"| 总函数调用次数 | {self.session.total_calls} |")
        
        # 统计异步调用
        async_count = sum(1 for call in self.session.function_calls if call.is_async)
        sync_count = self.session.total_calls - async_count
        self._write(f"| 同步调用次数 | {sync_count} |")
        self._write(f"| 异步调用次数 | {async_count} |")
        
        # 统计异常
        error_count = sum(1 for call in self.session.function_calls if call.exception)
        self._write(f"| 异常次数 | {error_count} |")
        self._write()
        
        # 模块列表
        self._write("### 追踪的模块")
        self._write()
        modules = self.session.get_modules()
        for module in modules:
            self._write(f"- `{module}`")
        self._write()
        
        # 函数列表
        self._write("### 追踪的函数")
        self._write()
        functions = self.session.get_functions()
        for func in functions:
            self._write(f"- `{func}`")
        self._write()
    
    def _write_call_tree(self) -> None:
        """写入调用树"""
        self._write("## 🌲 调用树")
        self._write()
        self._write("```")
        
        root_calls = self.session.get_root_calls()
        for call in root_calls:
            self._write_call_tree_node(call, prefix="", is_last=True)
        
        self._write("```")
        self._write()
    
    def _write_call_tree_node(self, call: FunctionCall, prefix: str, is_last: bool) -> None:
        """递归写入调用树节点"""
        # 构建当前节点的显示
        connector = "└── " if is_last else "├── "
        async_marker = "⚡" if call.is_async else ""
        error_marker = "❌" if call.exception else ""
        duration = f"({call.duration_ms:.2f}ms)"
        
        # 格式化参数
        args_str = self._format_args(call.args, call.kwargs)
        
        self._write(f"{prefix}{connector}{async_marker}{call.function_name}({args_str}) {duration} {error_marker}")
        
        # 处理子调用
        children = [self.session.call_map.get(child_id) for child_id in call.children_call_ids]
        children = [c for c in children if c is not None]
        
        for i, child in enumerate(children):
            new_prefix = prefix + ("    " if is_last else "│   ")
            self._write_call_tree_node(child, new_prefix, i == len(children) - 1)
    
    def _format_args(self, args: tuple, kwargs: dict, max_len: int = 50) -> str:
        """格式化参数显示"""
        parts = []
        
        for arg in args:
            s = self._safe_repr(arg, max_len=20)
            parts.append(s)
        
        for key, value in kwargs.items():
            s = f"{key}={self._safe_repr(value, max_len=15)}"
            parts.append(s)
        
        result = ", ".join(parts)
        if len(result) > max_len:
            result = result[:max_len-3] + "..."
        return result
    
    def _safe_repr(self, value, max_len: int = 50) -> str:
        """安全的repr"""
        try:
            s = repr(value)
            if len(s) > max_len:
                s = s[:max_len-3] + "..."
            return s
        except:
            return "<...>"
    
    def _write_timeline(self) -> None:
        """写入时序图表格"""
        self._write("## 📈 调用时序")
        self._write()
        self._write("| 序号 | 时间 | 函数 | 模块 | 耗时 | 类型 | 状态 |")
        self._write("|------|------|------|------|------|------|------|")
        
        for i, call in enumerate(self.session.function_calls, 1):
            time_str = call.start_time.strftime('%H:%M:%S.%f')[:-3]
            duration = f"{call.duration_ms:.2f}ms"
            call_type = "异步" if call.is_async else "同步"
            status = "❌ 异常" if call.exception else "✅ 成功"
            
            # 添加缩进以表示调用层级
            indent = "　" * call.depth  # 使用全角空格
            func_name = f"{indent}{call.function_name}"
            
            self._write(f"| {i} | {time_str} | `{func_name}` | {call.module_name} | {duration} | {call_type} | {status} |")
        
        self._write()
    
    def _write_variable_changes(self) -> None:
        """写入变量变化记录"""
        # 检查是否有变量变化
        has_changes = any(call.variable_changes for call in self.session.function_calls)
        if not has_changes:
            return
        
        self._write("## 🔄 变量变化记录")
        self._write()
        
        for call in self.session.function_calls:
            if not call.variable_changes:
                continue
            
            self._write(f"### `{call.function_name}()` (调用ID: {call.call_id})")
            self._write()
            self._write("| 变量名 | 操作 | 旧值 | 新值 | 行号 |")
            self._write("|--------|------|------|------|------|")
            
            for change in call.variable_changes:
                op = change.operation.value
                old_val = self._safe_repr(change.old_value) if change.old_value is not None else "-"
                new_val = self._safe_repr(change.new_value) if change.new_value is not None else "-"
                
                self._write(f"| `{change.name}` | {op} | `{old_val}` | `{new_val}` | {change.line_no} |")
            
            self._write()
    
    def _write_detailed_logs(self) -> None:
        """写入详细调用日志"""
        self._write("## 📝 详细调用日志")
        self._write()
        
        for i, call in enumerate(self.session.function_calls, 1):
            self._write(f"### {i}. `{call.full_name}()`")
            self._write()
            
            # 基本信息
            self._write("<details>")
            self._write(f"<summary>调用详情 (ID: {call.call_id})</summary>")
            self._write()
            
            self._write("| 属性 | 值 |")
            self._write("|------|-----|")
            self._write(f"| 调用ID | `{call.call_id}` |")
            self._write(f"| 函数名 | `{call.function_name}` |")
            self._write(f"| 模块 | `{call.module_name}` |")
            if call.package_name:
                self._write(f"| 包 | `{call.package_name}` |")
            self._write(f"| 文件 | `{call.file_path}` |")
            self._write(f"| 定义行号 | {call.line_no} |")
            self._write(f"| 调用深度 | {call.depth} |")
            self._write(f"| 类型 | {'异步' if call.is_async else '同步'} |")
            self._write(f"| 开始时间 | {call.start_time.strftime('%H:%M:%S.%f')[:-3]} |")
            if call.end_time:
                self._write(f"| 结束时间 | {call.end_time.strftime('%H:%M:%S.%f')[:-3]} |")
            self._write(f"| 执行耗时 | {call.duration_ms:.2f} ms |")
            
            if call.parent_call_id:
                parent = self.session.call_map.get(call.parent_call_id)
                if parent:
                    self._write(f"| 父调用 | `{parent.function_name}` ({call.parent_call_id}) |")
            
            self._write()
            
            # 参数
            self._write("**输入参数:**")
            self._write()
            self._write("```python")
            if call.args:
                self._write(f"args = {self._safe_repr(call.args, max_len=200)}")
            if call.kwargs:
                self._write(f"kwargs = {self._safe_repr(call.kwargs, max_len=200)}")
            if not call.args and not call.kwargs:
                self._write("# 无参数")
            self._write("```")
            self._write()
            
            # 返回值
            self._write("**返回值:**")
            self._write()
            self._write("```python")
            if call.exception:
                self._write(f"# 异常: {type(call.exception).__name__}: {call.exception}")
            else:
                self._write(f"return {self._safe_repr(call.return_value, max_len=200)}")
            self._write("```")
            self._write()
            
            self._write("</details>")
            self._write()
    
    def _write_footer(self) -> None:
        """写入报告尾部"""
        self._write("---")
        self._write()
        self._write("*此报告由 Python Tracer 自动生成*")
        self._write()
        self._write(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
