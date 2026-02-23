"""
应用程序入口 - 自定义信号槽架构的任务管理器
演示如何不依赖Qt的Model/View框架，使用自定义信号和槽机制来手动同步数据和UI
"""
import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController

def main():
    """主函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("自定义信号槽任务管理器")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("PyQt学习项目")
    
    print("=" * 60)
    print("自定义信号槽架构 - 任务管理器")
    print("=" * 60)
    print("架构特点:")
    print("1. 数据层(Repository)继承QObject，发射自定义信号")
    print("2. 视图层(View)使用QListWidget，提供手动UI操作方法")
    print("3. 控制器层(Controller)连接信号和槽，协调数据和UI")
    print("4. 不依赖Qt的Model/View框架，完全手动控制UI更新")
    print("=" * 60)
    
    try:
        # 创建主控制器
        controller = MainController()
        
        # 显示主窗口
        controller.show()
        
        print("应用程序启动成功！")
        print("请在界面中测试以下功能:")
        print("- 添加新任务")
        print("- 删除任务")
        print("- 更新任务状态")
        print("- 清空所有任务")
        print("- 观察控制台输出，了解信号槽的工作流程")
        print("=" * 60)
        
        # 启动事件循环
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()