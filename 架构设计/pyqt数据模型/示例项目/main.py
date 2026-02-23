"""
应用程序入口点
"""
import sys
from Qt.QtWidgets import QApplication
from controllers.main_controller import MainController

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建主控制器
    controller = MainController()
    
    # 显示主窗口
    controller.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()