# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from context import PluginContext
from plugin_manager import PluginManager


class MainWindow(QMainWindow):
    """主窗口，仅负责 UI 框架，业务全部交给插件"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 插件化示例")
        self.resize(800, 600)

        # ---------- 状态栏 ----------
        self.statusBar().showMessage("就绪")

        # ---------- 中央区域（插件可以随意添加控件） ----------
        central = QWidget()
        self.layout = QVBoxLayout()
        central.setLayout(self.layout)
        self.setCentralWidget(central)

        # 欢迎标签（可被插件覆盖或追加）
        self.layout.addWidget(QLabel("<h1>欢迎使用插件化主程序</h1>", alignment=Qt.AlignCenter))

        # ---------- 创建上下文 & 插件管理器 ----------
        self.ctx = PluginContext(self)
        self.plugin_mgr = PluginManager(self.ctx)

        # 加载插件
        self.plugin_mgr.load_all()

        # ---------- 主程序自带的几个菜单（演示） ----------
        self.ctx.add_menu_item("File/Exit", "退出(&Q)", callback=self.close, shortcut="Ctrl+Q")
        self.ctx.add_menu_item("Help/About", "关于", callback=self.show_about)

    # -------------------------------------------------
    # 主程序自带的小功能
    # -------------------------------------------------
    def show_about(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "About",
                                "PyQt5 插件化框架示例\n"
                                "作者：ChatGPT\n"
                                "日期：2025-11")

    # -------------------------------------------------
    # 提供给插件的快捷入口（可选）
    # -------------------------------------------------
    def add_central_widget(self, widget):
        """插件可直接把控件塞到主布局"""
        self.layout.addWidget(widget)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()