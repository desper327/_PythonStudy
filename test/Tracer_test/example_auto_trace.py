"""
示例: 演示如何使用自动追踪功能（无需手动添加装饰器）

运行方式:
    python example_auto_trace.py
    
运行后将生成 trace_report_auto.md 文件
"""

import os
import sys

# 将 tracer 模块添加到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tracer import Tracer


# ============ 示例函数（无需添加 @trace 装饰器）============

def calculate_sum(a: int, b: int) -> int:
    """计算两数之和"""
    result = a + b
    return result


def calculate_product(a: int, b: int) -> int:
    """计算两数之积"""
    result = a * b
    return result


def process_numbers(x: int, y: int) -> dict:
    """处理数字：计算和与积"""
    # 调用子函数 - 这些调用会被自动追踪
    sum_result = calculate_sum(x, y)
    product_result = calculate_product(x, y)
    
    # 本地变量变化
    data = {
        "sum": sum_result,
        "product": product_result
    }
    
    # 修改变量
    data["average"] = sum_result / 2
    
    return data


def fibonacci(n: int) -> int:
    """计算斐波那契数列"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b


def helper_function(value: int) -> int:
    """辅助函数 - 也会被自动追踪"""
    return value * 2


def nested_call_demo():
    """演示嵌套调用"""
    x = helper_function(5)
    y = helper_function(x)
    z = helper_function(y)
    return z


def main():
    """主函数"""
    print("=" * 50)
    print("Python Tracer 自动追踪示例")
    print("=" * 50)
    
    # 1. 基本函数调用
    print("\n1. 基本计算:")
    result = process_numbers(10, 20)
    print(f"   结果: {result}")
    
    # 2. 斐波那契数列
    print("\n2. 斐波那契数列:")
    fib_result = fibonacci(10)
    print(f"   Fib(10) = {fib_result}")
    
    # 3. 嵌套调用
    print("\n3. 嵌套调用:")
    nested_result = nested_call_demo()
    print(f"   嵌套结果: {nested_result}")
    
    print("\n" + "=" * 50)
    print("追踪完成！")
    print("=" * 50)


# ============ 运行示例 ============

if __name__ == "__main__":
    # 获取当前脚本所在目录作为项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print(f"项目根目录: {project_root}")
    print("开始自动追踪...\n")
    
    # 使用自动追踪模式（关键：传入 project_root 参数）
    Tracer.start(project_root=project_root)
    
    # 运行主程序 - 所有函数调用都会被自动追踪
    main()
    
    # 停止追踪并生成报告
    Tracer.stop()
    report = Tracer.generate_report("trace_report_auto.md")
    
    print("\n📄 报告已生成: trace_report_auto.md")
    print("\n报告预览 (前60行):")
    print("-" * 50)
    lines = report.split('\n')[:60]
    print('\n'.join(lines))
    if len(report.split('\n')) > 60:
        print("\n... (更多内容请查看 trace_report_auto.md)")
