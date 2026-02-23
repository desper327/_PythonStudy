核心思路

Context：把主窗口、命令字典、信号槽等全部封装成一个对象，插件只能通过它与主程序交互。
PluginManager：扫描 plugins/ 目录，动态 importlib 加载每个 .py，调用其 init(context)（或 register(context)）函数。
插件：只要实现 init(context)（或 register(context)）即可，插件里可以：

注册命令（context.register_command）
添加菜单 / 子菜单（context.add_menu_item）
直接操作 context.main_window 放控件
发射/接收自定义信号（context.signal_*）



5. 运行方式
bash# 1. 安装依赖
pip install pyqt5

# 2. 进入项目根目录
cd project

# 3. 直接运行主程序
python main.py




启动后你会看到：

菜单栏：File → Exit、Tools → Hello → Say Hello、Tools → Plugin Panel → 清空面板、Help → About
右侧 Dock：插件面板（带文本框 + 按钮）
中央区域：欢迎文字 + 插件按钮：点我问好

点击任意菜单 / 按钮，都能看到控制台输出与状态栏提示，证明 插件已成功获取主程序对象并扩展 UI。

6. 进阶建议（可选）



功能,实现思路
插件热重载,在 MainWindow 加一个 F5 快捷键 → self.plugin_mgr.reload_all()
插件元数据,"让插件提供 PLUGIN_INFO = {""name"": ""..."", ""version"": ""1.0""}，管理器读取后展示在 “插件管理” 窗口"
依赖声明,"在插件顶部写 REQUIREMENTS = [""numpy""]，管理器用 pip install 自动安装"
安全沙箱,使用 multiprocessing 或 restrictedpython 把插件跑在子进程
事件总线,"ctx.signal_event = pyqtSignal(str, dict)，插件 ctx.signal_event.emit(""my_event"", data)"



总结：
只要把 Context、PluginManager、统一的 init 接口 三大件写好，PyQt5 的插件化系统就可以像 Maya 一样灵活、易维护。祝你玩得开心！