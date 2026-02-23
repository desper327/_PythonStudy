#!/usr/bin/env python3
"""
启动脚本
提供简化的程序启动方式
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """检查依赖包是否已安装"""
    required_packages = [
        'PySide6',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖包:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    """主函数"""
    print("🎬 三维影视制作管理系统")
    print("=" * 50)
    
    # 检查依赖
    print("🔍 检查依赖包...")
    if not check_dependencies():
        return 1
    
    print("✅ 依赖包检查完成")
    
    # 启动程序
    print("🚀 启动应用程序...")
    try:
        from main import main as app_main
        return app_main()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)