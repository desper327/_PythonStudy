"""
基础控制器类
提供控制器的通用功能和接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable
from PySide6.QtCore import QObject, QTimer
from beartype import beartype


# 解决QObject和ABC的元类冲突
class QObjectMeta(type(QObject), type(ABC)):
    """兼容QObject和ABC的元类"""
    pass


class BaseController(QObject, ABC, metaclass=QObjectMeta):
    """
    基础控制器抽象类
    定义所有控制器的通用接口和功能
    """
    
    @beartype
    def __init__(self, parent: Optional[QObject] = None):
        """
        初始化基础控制器
        
        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self._initialized = False
        self._cleanup_callbacks: list = []
    
    @abstractmethod
    @beartype
    async def initialize(self) -> None:
        """
        异步初始化控制器
        子类必须实现此方法
        """
        pass
    
    @abstractmethod
    @beartype
    def setup_connections(self) -> None:
        """
        设置信号连接
        子类必须实现此方法
        """
        pass
    
    @beartype
    def is_initialized(self) -> bool:
        """
        检查控制器是否已初始化
        
        Returns:
            bool: 是否已初始化
        """
        return self._initialized
    
    @beartype
    def mark_initialized(self) -> None:
        """
        标记控制器为已初始化
        """
        self._initialized = True
    
    @beartype
    def add_cleanup_callback(self, callback: Callable[[], None]) -> None:
        """
        添加清理回调函数
        
        Args:
            callback: 清理回调函数
        """
        self._cleanup_callbacks.append(callback)
    
    @beartype
    async def cleanup(self) -> None:
        """
        清理控制器资源
        """
        try:
            # 执行所有清理回调
            for callback in self._cleanup_callbacks:
                try:
                    if callable(callback):
                        callback()
                except Exception as e:
                    print(f"清理回调执行失败: {e}")
            
            # 清空回调列表
            self._cleanup_callbacks.clear()
            
            # 标记为未初始化
            self._initialized = False
            
        except Exception as e:
            print(f"控制器清理失败: {e}")
    
    @beartype
    def log_message(self, message: str, is_error: bool = False) -> None:
        """
        记录日志消息
        
        Args:
            message: 日志消息
            is_error: 是否为错误消息
        """
        level = "ERROR" if is_error else "INFO"
        print(f"[{level}] {self.__class__.__name__}: {message}")


class ControllerManager(QObject):
    """
    控制器管理器
    负责管理所有控制器的生命周期
    """
    
    @beartype
    def __init__(self, parent: Optional[QObject] = None):
        """
        初始化控制器管理器
        
        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self._controllers: Dict[str, BaseController] = {}
        self._initialization_order: list = []
    
    @beartype
    def register_controller(self, name: str, controller: BaseController) -> None:
        """
        注册控制器
        
        Args:
            name: 控制器名称
            controller: 控制器实例
        """
        if name in self._controllers:
            raise ValueError(f"控制器 '{name}' 已存在")
        
        self._controllers[name] = controller
        self._initialization_order.append(name)
    
    @beartype
    def get_controller(self, name: str) -> Optional[BaseController]:
        """
        获取控制器
        
        Args:
            name: 控制器名称
            
        Returns:
            Optional[BaseController]: 控制器实例或None
        """
        return self._controllers.get(name)
    
    @beartype
    def remove_controller(self, name: str) -> bool:
        """
        移除控制器
        
        Args:
            name: 控制器名称
            
        Returns:
            bool: 是否成功移除
        """
        if name in self._controllers:
            del self._controllers[name]
            if name in self._initialization_order:
                self._initialization_order.remove(name)
            return True
        return False
    
    @beartype
    async def initialize_all(self) -> None:
        """
        按顺序初始化所有控制器
        """
        for name in self._initialization_order:
            controller = self._controllers.get(name)
            if controller and not controller.is_initialized():
                try:
                    await controller.initialize()
                    controller.setup_connections()
                    controller.mark_initialized()
                    print(f"控制器 '{name}' 初始化完成")
                except Exception as e:
                    print(f"控制器 '{name}' 初始化失败: {e}")
                    raise
    
    @beartype
    async def cleanup_all(self) -> None:
        """
        清理所有控制器
        """
        # 按相反顺序清理
        for name in reversed(self._initialization_order):
            controller = self._controllers.get(name)
            if controller:
                try:
                    await controller.cleanup()
                    print(f"控制器 '{name}' 清理完成")
                except Exception as e:
                    print(f"控制器 '{name}' 清理失败: {e}")
    
    @beartype
    def get_all_controllers(self) -> Dict[str, BaseController]:
        """
        获取所有控制器
        
        Returns:
            Dict[str, BaseController]: 所有控制器字典
        """
        return self._controllers.copy()
    
    @beartype
    def get_controller_count(self) -> int:
        """
        获取控制器数量
        
        Returns:
            int: 控制器数量
        """
        return len(self._controllers)
