#!/usr/bin/env python3
"""
MVC框架启动脚本
提供简单的启动方式和错误处理
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """检查必要的依赖包"""
    required_packages = [
        'PySide6',
        'pydantic',
        'beartype',
        'sqlalchemy',
        'aiomysql',
        'pymysql',
        'aiohttp'
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
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """检查环境配置"""
    env_file = project_root / '.env'
    
    if not env_file.exists():
        print("⚠️  未找到 .env 配置文件")
        print("请复制 .env.example 为 .env 并配置数据库连接信息")
        print("cp .env.example .env")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 启动 MVC Framework...")
    print("=" * 50)
    
    # 检查依赖
    print("📦 检查依赖包...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ 依赖包检查通过")
    
    # 检查环境配置
    print("⚙️  检查环境配置...")
    if not check_environment():
        print("⚠️  环境配置检查失败，但程序仍会尝试启动")
    else:
        print("✅ 环境配置检查通过")
    
    print("=" * 50)
    
    try:
        # 导入并运行主程序
        from main import main as app_main
        exit_code = app_main()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
        sys.exit(0)
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保所有依赖包已正确安装")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 程序运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
