"""
三维影视制作管理系统主程序入口
基于PySide6的MVC架构桌面应用程序
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from controllers.main_controller import MainController


class SplashScreen(QSplashScreen):
    """启动画面"""
    
    def __init__(self):
        # 创建一个简单的启动画面
        pixmap = QPixmap(400, 300)
        pixmap.fill(QColor(45, 45, 45))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 255, 255))
        
        # 设置字体
        title_font = QFont("Arial", 18, QFont.Bold)
        subtitle_font = QFont("Arial", 12)
        
        # 绘制标题
        painter.setFont(title_font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "三维影视制作管理系统")
        
        # 绘制副标题
        painter.setFont(subtitle_font)
        subtitle_rect = pixmap.rect()
        subtitle_rect.setTop(subtitle_rect.center().y() + 30)
        painter.drawText(subtitle_rect, Qt.AlignCenter, "Film Production Manager v1.0")
        
        # 绘制版权信息
        copyright_rect = pixmap.rect()
        copyright_rect.setTop(copyright_rect.bottom() - 50)
        painter.drawText(copyright_rect, Qt.AlignCenter, "基于PySide6的MVC架构")
        
        painter.end()
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
    
    def show_message(self, message: str):
        """显示加载消息"""
        self.showMessage(
            message, 
            Qt.AlignBottom | Qt.AlignCenter, 
            QColor(255, 255, 255)
        )
        QApplication.processEvents()


class FilmProductionApp:
    """应用程序主类"""
    
    def __init__(self):
        self.app = None
        self.controller = None
        self.main_window = None
        self.splash = None
    
    def initialize_app(self):
        """初始化应用程序"""
        # 创建QApplication实例
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("三维影视制作管理系统")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Film Production Studio")
        
        # 设置应用程序样式
        self.set_application_style()
        
        # 显示启动画面
        self.splash = SplashScreen()
        self.splash.show()
        
        return True
    
    def set_application_style(self):
        """设置应用程序样式"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QMenuBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            padding: 4px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
            border-radius: 4px;
        }
        
        QMenuBar::item:selected {
            background-color: #e3f2fd;
        }
        
        QToolBar {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            spacing: 4px;
            padding: 4px;
        }
        
        QToolBar::separator {
            background-color: #e0e0e0;
            width: 1px;
            margin: 4px;
        }
        
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #1976D2;
        }
        
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QComboBox {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px 8px;
            background-color: white;
        }
        
        QComboBox:hover {
            border-color: #2196F3;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #666;
            margin-right: 5px;
        }
        
        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px 8px;
            background-color: white;
        }
        
        QLineEdit:focus {
            border-color: #2196F3;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: #f5f5f5;
        }
        
        QTabWidget::pane {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
        }
        
        QTabBar::tab {
            background-color: #f0f0f0;
            border: 1px solid #cccccc;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 1px solid white;
        }
        
        QTabBar::tab:hover {
            background-color: #e3f2fd;
        }
        
        QStatusBar {
            background-color: #f0f0f0;
            border-top: 1px solid #cccccc;
        }
        """
        
        self.app.setStyleSheet(style)
    
    def initialize_controller(self):
        """初始化控制器"""
        self.splash.show_message("正在初始化控制器...")
        
        try:
            # 创建主控制器
            self.controller = MainController(api_base_url="http://www.baidu.com")
            
            # 初始化控制器并获取主窗口
            self.main_window = self.controller.initialize()
            
            return True
            
        except Exception as e:
            self.show_error(f"控制器初始化失败: {str(e)}")
            return False
    
    def setup_connections(self):
        """设置信号连接"""
        self.splash.show_message("正在设置信号连接...")
        
        # 连接应用程序退出信号
        if self.main_window:
            self.main_window.destroyed.connect(self.cleanup)
    
    def show_main_window(self):
        """显示主窗口"""
        self.splash.show_message("正在启动主界面...")
        
        # 延迟显示主窗口
        QTimer.singleShot(1000, self._show_main_window_delayed)
    
    def _show_main_window_delayed(self):
        """延迟显示主窗口"""
        if self.main_window:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
        
        if self.splash:
            self.splash.finish(self.main_window)
            self.splash = None
    
    def run(self):
        """运行应用程序"""
        if not self.app:
            return 1
        
        try:
            return self.app.exec()
        except Exception as e:
            self.show_error(f"应用程序运行时错误: {str(e)}")
            return 1
    
    def cleanup(self):
        """清理资源"""
        if self.controller:
            self.controller.cleanup()
    
    def show_error(self, message: str):
        """显示错误消息"""
        if self.splash:
            self.splash.hide()
        
        QMessageBox.critical(None, "错误", message)


def main():
    """主函数"""
    # 创建应用程序实例
    app_instance = FilmProductionApp()
    
    try:
        # 初始化应用程序
        if not app_instance.initialize_app():
            return 1
        
        # 初始化控制器
        if not app_instance.initialize_controller():
            return 1
        
        # 设置信号连接
        app_instance.setup_connections()
        
        # 显示主窗口
        app_instance.show_main_window()
        
        # 运行应用程序
        return app_instance.run()
        
    except KeyboardInterrupt:
        print("\n应用程序被用户中断")
        return 0
    
    except Exception as e:
        app_instance.show_error(f"应用程序启动失败: {str(e)}")
        return 1
    
    finally:
        # 清理资源
        app_instance.cleanup()


if __name__ == "__main__":
    # 设置异常处理
    sys.excepthook = lambda exc_type, exc_value, exc_tb: (
        QMessageBox.critical(None, "未处理的异常", 
                           f"发生未处理的异常:\n{exc_type.__name__}: {exc_value}"),
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    )
    
    # 运行主程序
    exit_code = main()
    sys.exit(exit_code)