# context.py
import sys
from typing import Callable, Dict
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5.QtCore import pyqtSignal, QObject


class PluginContext(QObject):
    """
    主程序向插件提供的唯一交互对象。
    插件只能通过这里的公开方法访问主程序功能。
    """
    # 自定义信号（插件可以发射，主程序或其他插件可以连接）
    command_triggered = pyqtSignal(str)          # 参数：command name
    status_message = pyqtSignal(str, int)        # 参数：msg, timeout_ms

    def __init__(self, main_window: QMainWindow):
        super().__init__()
        self.main_window = main_window          # 主窗口对象
        self.commands: Dict[str, Callable] = {} # 命令名 -> 可调用对象
        self._menus: Dict[str, QMenu] = {}      # menu_path -> QMenu

    # -------------------------------------------------
    # 1. 命令注册
    # -------------------------------------------------
    def register_command(self, name: str, func: Callable):
        """
        插件注册一个命令，之后可以通过 menu / 快捷键 / 其它插件调用。
        """
        if name in self.commands:
            print(f"[Context] Warning: command '{name}' 已存在，将被覆盖")
        self.commands[name] = func
        print(f"[Context] 注册命令: {name}")

    def execute_command(self, name: str, *args, **kwargs):
        """外部（包括菜单）调用已注册的命令"""
        if name not in self.commands:
            print(f"[Context] Error: 未找到命令 '{name}'")
            return
        try:
            self.commands[name](*args, **kwargs)
        except Exception as e:
            print(f"[Context] 执行命令 '{name}' 出错: {e}")

    # -------------------------------------------------
    # 2. 菜单管理
    # -------------------------------------------------
    def add_menu_item(self, menu_path: str, label: str, command_name: str = None,
                      callback: Callable = None, shortcut: str = None):
        """
        在指定路径下添加菜单项。
        - menu_path: 用 '/' 分隔的多级菜单，例如 "File/Exit"
        - command_name: 若提供，则点击时自动调用 execute_command
        - callback: 直接绑定的函数（优先于 command_name）
        - shortcut: 可选快捷键
        """
        parts = menu_path.split("/")
        parent_menu = self._ensure_menu(parts[:-1])   # 递归创建父菜单
        action = QAction(label, self.main_window)

        if callback:
            action.triggered.connect(callback)
        elif command_name:
            action.triggered.connect(lambda: self.execute_command(command_name))
        else:
            raise ValueError("必须提供 command_name 或 callback")

        if shortcut:
            action.setShortcut(shortcut)

        parent_menu.addAction(action)
        print(f"[Context] 添加菜单: {menu_path} -> {label}")

    def _ensure_menu(self, path_parts):
        """
        递归确保多级菜单存在，返回最底层的 QMenu。
        """
        if not path_parts:
            return self.main_window.menuBar()

        key = "/".join(path_parts)
        if key not in self._menus:
            parent = self._ensure_menu(path_parts[:-1])
            menu = QMenu(path_parts[-1], self.main_window)
            parent.addMenu(menu)
            self._menus[key] = menu
        return self._menus[key]

    # -------------------------------------------------
    # 3. 状态栏快捷方法（可选）
    # -------------------------------------------------
    def show_status(self, msg: str, timeout: int = 3000):
        self.main_window.statusBar().showMessage(msg, timeout)
        self.status_message.emit(msg, timeout)