# plugins/ui_plugin.py
"""
演示更复杂的 UI 扩展：
- 创建一个独立的 DockWidget
- 注册多个命令
- 监听上下文信号
"""

def init(ctx):
    from PyQt5.QtWidgets import QDockWidget, QTextEdit, QPushButton, QVBoxLayout, QWidget

    # ---------- 1. 创建 Dock ----------
    dock = QDockWidget("插件面板", ctx.main_window)
    dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

    text_edit = QTextEdit()
    text_edit.setPlaceholderText("在这里输入文字，点击按钮会打印到控制台")

    btn = QPushButton("打印内容")
    def print_text():
        content = text_edit.toPlainText()
        print("[ui_plugin] 用户输入:", content)
        ctx.show_status(f"已打印 {len(content)} 字符", 1500)

    btn.clicked.connect(print_text)

    layout = QVBoxLayout()
    layout.addWidget(text_edit)
    layout.addWidget(btn)

    container = QWidget()
    container.setLayout(layout)
    dock.setWidget(container)

    ctx.main_window.addDockWidget(Qt.RightDockWidgetArea, dock)

    # ---------- 2. 注册命令 ----------
    ctx.register_command("clear_dock", text_edit.clear)
    ctx.add_menu_item("Tools/Plugin Panel", "清空面板", command_name="clear_dock")

    # ---------- 3. 监听上下文信号（可选） ----------
    def on_status(msg, timeout):
        print(f"[ui_plugin] 状态栏消息: {msg} ({timeout}ms)")
    ctx.status_message.connect(on_status)