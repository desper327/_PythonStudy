#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
现代命令工具启动器
"""
import sys
import os
import subprocess

def ensure_dependencies():
    """确保所有依赖已安装"""
    try:
        import PySide6
        print("PySide6已安装")
    except ImportError:
        print("正在安装PySide6...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])
        print("PySide6安装完成")

def main():
    """主函数"""
    # 确保依赖已安装
    ensure_dependencies()
    
    # 导入主模块
    from modern_cmd_tool import MainWindow, QApplication
    
    # 启动应用
    app = QApplication(sys.argv)
    
    # 设置全局字体
    from PySide6.QtGui import QFont
    font = QFont("Microsoft YaHei UI", 10)
    app.setFont(font)
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    # 设置Python默认编码为UTF-8
    if sys.platform == 'win32':
        # 设置Windows控制台编码为UTF-8
        os.system('chcp 65001')
        # 设置Python的默认编码
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr.reconfigure(encoding='utf-8')
    
    main() 