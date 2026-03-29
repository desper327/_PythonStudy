"""
Python 运行时调用追踪器

用于追踪Python程序运行时函数调用并生成Markdown报告。

使用方法:
    from tracer import trace, Tracer
    
    @trace()  # 自动深度追踪内部调用的本地函数
    def main():
        helper()  # 会被自动追踪
        
    main()
    Tracer.generate_report()
"""

from .core import Tracer, trace
from .models import FunctionCall, TraceSession
from .report_generator import ReportGenerator

__version__ = "2.0.0"

__all__ = [
    "Tracer",
    "trace",
    "FunctionCall",
    "TraceSession",
    "ReportGenerator",
]