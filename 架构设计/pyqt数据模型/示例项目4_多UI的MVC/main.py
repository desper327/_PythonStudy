"""
MVC框架主程序入口
基于PySide6的MVC架构桌面应用程序
"""
import sys
import asyncio
import signal
from typing import Optional
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer, QCoreApplication
from beartype import beartype
from views.main_window import MainWindow
from controllers.main_controller import MainController
from config.settings import settings


class MVCApplication:
    """
    MVC应用程序主类
    负责应用程序的初始化、启动和清理
    """
    
    @beartype
    def __init__(self):
        """
        初始化MVC应用程序
        """
        self.app: Optional[QApplication] = None
        self.main_window: Optional[MainWindow] = None
        self.main_controller: Optional[MainController] = None
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None
        self.loop_timer: Optional[QTimer] = None
    
    @beartype
    def setup_application(self) -> None:
        """
        设置Qt应用程序
        """
        # 创建Qt应用程序
        self.app = QApplication(sys.argv)
        
        # 设置应用程序属性
        self.app.setApplicationName(settings.app.app_name)
        self.app.setApplicationVersion(settings.app.app_version)
        self.app.setOrganizationName("MVC Framework")
        self.app.setOrganizationDomain("mvc-framework.local")
        
        # 设置应用程序样式
        self._setup_application_style()
        
        # 设置信号处理
        self._setup_signal_handlers()
    
    @beartype
    def _setup_application_style(self) -> None:
        """
        设置应用程序样式
        """
        # 可以在这里设置全局样式表
        style_sheet = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QMenuBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
        }
        
        QMenuBar::item {
            padding: 4px 8px;
            background-color: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #e3f2fd;
        }
        
        QToolBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            spacing: 4px;
        }
        
        QPushButton {
            background-color: #2196f3;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #1976d2;
        }
        
        QPushButton:pressed {
            background-color: #0d47a1;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QProgressBar {
            border: 2px solid #cccccc;
            border-radius: 5px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #2196f3;
            border-radius: 3px;
        }
        
        QListWidget {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
        }
        
        QListWidget::item {
            padding: 4px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        QListWidget::item:selected {
            background-color: #e3f2fd;
        }
        
        QTableWidget {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
            gridline-color: #f0f0f0;
        }
        
        QTableWidget::item {
            padding: 4px;
        }
        
        QTableWidget::item:selected {
            background-color: #e3f2fd;
        }
        
        QTextEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        """
        
        self.app.setStyleSheet(style_sheet)
    
    @beartype
    def _setup_signal_handlers(self) -> None:
        """
        设置信号处理器
        """
        # 设置Ctrl+C信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # 让Qt应用程序能够处理系统信号
        timer = QTimer()
        timer.start(500)  # 每500ms检查一次信号
        timer.timeout.connect(lambda: None)
    
    @beartype
    def _signal_handler(self, signum: int, frame) -> None:
        """
        信号处理器
        
        Args:
            signum: 信号编号
            frame: 帧对象
        """
        print(f"\n收到信号 {signum}，正在关闭应用程序...")
        self.shutdown()
    
    @beartype
    def setup_async_integration(self) -> None:
        """
        设置异步事件循环集成
        """
        # 创建异步事件循环
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        
        # 创建定时器来处理异步事件
        self.loop_timer = QTimer()
        self.loop_timer.timeout.connect(self._process_async_events)
        self.loop_timer.start(10)  # 每10ms处理一次异步事件
    
    @beartype
    def _process_async_events(self) -> None:
        """
        处理异步事件
        """
        if self.event_loop and not self.event_loop.is_closed():
            try:
                # 运行一次事件循环迭代
                self.event_loop.stop()
                self.event_loop.run_forever()
            except RuntimeError:
                pass  # 事件循环可能已经停止
    
    @beartype
    async def initialize_components(self) -> None:
        """
        异步初始化组件
        """
        try:
            # 创建主控制器
            self.main_controller = MainController()
            
            # 异步初始化控制器
            await self.main_controller.initialize()
            
            # 创建主窗口
            self.main_window = MainWindow()
            
            # 设置控制器的主窗口
            self.main_controller.set_main_window(self.main_window)
            
            print("组件初始化完成")
            
        except Exception as e:
            print(f"组件初始化失败: {e}")
            self._show_error_dialog("初始化失败", f"应用程序初始化失败:\n{str(e)}")
            raise
    
    @beartype
    def _show_error_dialog(self, title: str, message: str) -> None:
        """
        显示错误对话框
        
        Args:
            title: 对话框标题
            message: 错误消息
        """
        if self.app:
            QMessageBox.critical(None, title, message)
    
    @beartype
    def run(self) -> int:
        """
        运行应用程序
        
        Returns:
            int: 应用程序退出代码
        """
        try:
            # 设置Qt应用程序
            self.setup_application()
            
            # 设置异步集成
            self.setup_async_integration()
            
            # 异步初始化组件
            if self.event_loop:
                self.event_loop.run_until_complete(self.initialize_components())
            
            # 显示主窗口
            if self.main_window:
                self.main_window.show()
                print(f"{settings.app.app_name} 已启动")
            
            # 运行Qt事件循环
            return self.app.exec() if self.app else 1
            
        except KeyboardInterrupt:
            print("\n用户中断，正在关闭应用程序...")
            return 0
        except Exception as e:
            print(f"应用程序运行失败: {e}")
            self._show_error_dialog("运行错误", f"应用程序运行失败:\n{str(e)}")
            return 1
        finally:
            self.cleanup()
    
    @beartype
    def shutdown(self) -> None:
        """
        关闭应用程序
        """
        print("正在关闭应用程序...")
        
        if self.app:
            self.app.quit()
    
    @beartype
    def cleanup(self) -> None:
        """
        清理资源
        """
        try:
            # 停止异步事件循环定时器
            if self.loop_timer:
                self.loop_timer.stop()
            
            # 清理控制器
            if self.main_controller and self.event_loop:
                self.event_loop.run_until_complete(self.main_controller.cleanup())
            
            # 关闭异步事件循环
            if self.event_loop and not self.event_loop.is_closed():
                # 取消所有待处理的任务
                pending_tasks = asyncio.all_tasks(self.event_loop)
                for task in pending_tasks:
                    task.cancel()
                
                # 等待任务取消完成
                if pending_tasks:
                    self.event_loop.run_until_complete(
                        asyncio.gather(*pending_tasks, return_exceptions=True)
                    )
                
                self.event_loop.close()
            
            print("资源清理完成")
            
        except Exception as e:
            print(f"清理资源时出错: {e}")


@beartype
def main() -> int:
    """
    主函数
    
    Returns:
        int: 程序退出代码
    """
    # 创建并运行应用程序
    app = MVCApplication()
    return app.run()


if __name__ == "__main__":
    # 设置异常处理
    sys.excepthook = lambda exc_type, exc_value, exc_tb: print(
        f"未处理的异常: {exc_type.__name__}: {exc_value}"
    )
    
    # 运行应用程序
    exit_code = main()
    sys.exit(exit_code)
