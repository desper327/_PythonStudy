# plugin_manager.py
import os
import importlib.util
from typing import List
from context import PluginContext


class PluginManager:
    """负责发现、加载、初始化插件"""

    def __init__(self, context: PluginContext, plugin_dir: str = "plugins"):
        self.context = context
        self.plugin_dir = plugin_dir
        self.loaded_modules: List[object] = []

    def load_all(self):
        """扫描 plugin_dir，加载所有 .py（除 __init__.py）"""
        if not os.path.isdir(self.plugin_dir):
            print(f"[PluginManager] 插件目录不存在: {self.plugin_dir}")
            return

        for filename in sorted(os.listdir(self.plugin_dir)):
            if not filename.endswith(".py") or filename == "__init__.py":
                continue

            filepath = os.path.join(self.plugin_dir, filename)
            self._load_single(filepath, filename)

    def _load_single(self, filepath: str, filename: str):
        """动态导入单个插件文件并调用 init / register"""
        module_name = os.path.splitext(filename)[0]

        try:
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec is None or spec.loader is None:
                raise ImportError(f"无法创建 spec: {filepath}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)               # <-- 执行插件代码

            # 插件必须提供 init(context) 或 register(context) 任意一个
            entry_point = getattr(module, "init", None) or getattr(module, "register", None)
            if entry_point is None:
                print(f"[PluginManager] 跳过 {filename}：未找到 init/register 函数")
                return

            entry_point(self.context)
            self.loaded_modules.append(module)
            print(f"[PluginManager] 成功加载插件: {filename}")

        except Exception as e:
            print(f"[PluginManager] 加载插件 {filename} 失败: {e}")

    def reload_all(self):
        """热重载（开发时常用）"""
        print("[PluginManager] 正在重新加载所有插件...")
        self.loaded_modules.clear()
        self.load_all()