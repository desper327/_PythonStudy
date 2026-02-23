"""
基础仓储类
提供通用的数据访问接口和CRUD操作
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic
from beartype import beartype

# 泛型类型变量
T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    基础仓储抽象类
    定义了所有仓储类必须实现的基本CRUD操作
    """
    
    @abstractmethod
    @beartype
    async def create(self, entity: T) -> T:
        """
        创建新实体
        
        Args:
            entity: 要创建的实体
            
        Returns:
            T: 创建后的实体（包含ID等信息）
        """
        pass
    
    @abstractmethod
    @beartype
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        根据ID获取实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            Optional[T]: 实体对象或None
        """
        pass
    
    @abstractmethod
    @beartype
    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """
        获取所有实体
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[T]: 实体列表
        """
        pass
    
    @abstractmethod
    @beartype
    async def update(self, entity: T) -> T:
        """
        更新实体
        
        Args:
            entity: 要更新的实体
            
        Returns:
            T: 更新后的实体
        """
        pass
    
    @abstractmethod
    @beartype
    async def delete(self, entity_id: int) -> bool:
        """
        删除实体
        
        Args:
            entity_id: 要删除的实体ID
            
        Returns:
            bool: 是否删除成功
        """
        pass
    
    @abstractmethod
    @beartype
    async def exists(self, entity_id: int) -> bool:
        """
        检查实体是否存在
        
        Args:
            entity_id: 实体ID
            
        Returns:
            bool: 是否存在
        """
        pass
    
    @abstractmethod
    @beartype
    async def count(self) -> int:
        """
        获取实体总数
        
        Returns:
            int: 实体总数
        """
        pass
    
    @beartype
    async def find_by_criteria(self, criteria: Dict[str, Any]) -> List[T]:
        """
        根据条件查找实体（可选实现）
        
        Args:
            criteria: 查询条件字典
            
        Returns:
            List[T]: 符合条件的实体列表
        """
        # 默认实现：返回空列表
        # 子类可以根据需要重写此方法
        return []


class RepositoryError(Exception):
    """
    仓储层异常基类
    """
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        """
        初始化仓储异常
        
        Args:
            message: 错误消息
            original_error: 原始异常
        """
        super().__init__(message)
        self.message = message
        self.original_error = original_error


class EntityNotFoundError(RepositoryError):
    """
    实体未找到异常
    """
    
    def __init__(self, entity_type: str, entity_id: int):
        """
        初始化实体未找到异常
        
        Args:
            entity_type: 实体类型
            entity_id: 实体ID
        """
        message = f"{entity_type} with ID {entity_id} not found"
        super().__init__(message)
        self.entity_type = entity_type
        self.entity_id = entity_id


class DuplicateEntityError(RepositoryError):
    """
    重复实体异常
    """
    
    def __init__(self, entity_type: str, field: str, value: Any):
        """
        初始化重复实体异常
        
        Args:
            entity_type: 实体类型
            field: 重复的字段名
            value: 重复的值
        """
        message = f"{entity_type} with {field}='{value}' already exists"
        super().__init__(message)
        self.entity_type = entity_type
        self.field = field
        self.value = value


class DatabaseConnectionError(RepositoryError):
    """
    数据库连接异常
    """
    
    def __init__(self, connection_string: str, original_error: Exception):
        """
        初始化数据库连接异常
        
        Args:
            connection_string: 连接字符串
            original_error: 原始异常
        """
        message = f"Failed to connect to database: {connection_string}"
        super().__init__(message, original_error)
        self.connection_string = connection_string
