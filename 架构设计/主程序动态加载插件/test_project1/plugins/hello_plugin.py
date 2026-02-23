# plugins/hello_plugin.py
"""
演示最基础的插件：
- 注册一个命令
- 添加菜单项
- 发射状态栏信息
"""

def init(ctx):
    # 1. 注册命令
    def say_hello():
        print("Hello from hello_plugin!")
        ctx.show_status("插件说：Hello!", 2000)

    ctx.register_command("say_hello", say_hello)

    # 2. 添加菜单（两级）
    ctx.add_menu_item("Tools/Hello", "Say Hello", command_name="say_hello", shortcut="Ctrl+H")

    # 3. 直接在中央区域加个按钮（演示直接操作 UI）
    from PyQt5.QtWidgets import QPushButton
    btn = QPushButton("插件按钮：点我问好")
    btn.clicked.connect(say_hello)
    ctx.main_window.add_central_widget(btn)