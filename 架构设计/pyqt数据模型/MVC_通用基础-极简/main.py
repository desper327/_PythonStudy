"""
应用程序入口 - 自定义信号槽架构的任务管理器
极简版，没有多线程的功能
"""
import sys
from Qt.QtWidgets import QApplication
from controllers.main_controller import MainController

def main():
    """主函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("自定义信号槽任务管理器")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("PyQt学习项目")
    
    
    try:
        # 创建主控制器
        controller = MainController()
        
        # 显示主窗口
        controller.show()
        
        print("应用程序启动成功！")
        
        # 启动事件循环
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()