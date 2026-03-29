"""
示例: 演示如何使用 @trace 装饰器进行深度追踪

运行方式:
    python example.py
    
运行后将生成 trace_report.md 文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tracer import trace, Tracer


# ============ 示例函数（无需单独加装饰器）============

def calculate_sum(a: int, b: int) -> int:
    """计算两数之和"""
    return a + b


def calculate_product(a: int, b: int) -> int:
    """计算两数之积"""
    return a * b


def process_numbers(x: int, y: int) -> dict:
    """处理数字：计算和与积"""
    sum_result = calculate_sum(x, y)
    product_result = calculate_product(x, y)
    return {
        "sum": sum_result,
        "product": product_result,
        "average": sum_result / 2
    }


def helper(value: int) -> int:
    """辅助函数"""
    return value * 2


def nested_call():
    """嵌套调用演示"""
    x = helper(5)
    y = helper(x)
    return helper(y)


@trace()  # 只需在入口函数加装饰器，内部调用会被自动追踪
def main():
    """主函数"""
    print("=" * 50)
    print("Python Tracer 深度追踪示例")
    print("=" * 50)
    
    # 调用子函数 - 会被自动追踪
    print("\n1. 处理数字:")
    result = process_numbers(10, 20)
    print(f"   结果: {result}")
    
    # 嵌套调用 - 也会被自动追踪
    print("\n2. 嵌套调用:")
    nested_result = nested_call()
    print(f"   结果: {nested_result}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
    
    # 生成报告
    Tracer.generate_report("trace_report.md")
    
    print("\n📄 报告已生成: trace_report.md")