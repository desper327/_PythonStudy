"""
数据库访问层
使用MySQL和SQLAlchemy提供数据存储功能
"""
import asyncio
from typing import List, Optional, Dict, Any, Type, TypeVar
from datetime import datetime
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, select, update, delete, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from beartype import beartype
from models.user_model import UserModel
from models.database_models import Base, UserDB, TaskDB, DataRecordDB, LogEntryDB, ConfigDB
from config.settings import settings
from .base_repository import BaseRepository, RepositoryError, EntityNotFoundError, DatabaseConnectionError

# 泛型类型变量
T = TypeVar('T')


class DatabaseManager:
    """
    数据库管理器
    负责MySQL数据库连接、初始化和基本操作
    """
    
    @beartype
    def __init__(self):
        """
        初始化数据库管理器
        """
        self.db_config = settings.database
        self._sync_engine = None
        self._async_engine = None
        self._sync_session_factory = None
        self._async_session_factory = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.cleanup()
    
    @beartype
    async def initialize(self) -> None:
        """
        初始化数据库连接和会话工厂
        """
        try:
            # 创建同步引擎
            self._sync_engine = create_engine(
                self.db_config.get_sync_url(),
                pool_size=self.db_config.pool_size,
                max_overflow=self.db_config.max_overflow,
                pool_timeout=self.db_config.pool_timeout,
                pool_recycle=self.db_config.pool_recycle,
                echo=settings.app.debug
            )
            
            # 创建异步引擎
            self._async_engine = create_async_engine(
                self.db_config.get_async_url(),
                pool_size=self.db_config.pool_size,
                max_overflow=self.db_config.max_overflow,
                pool_timeout=self.db_config.pool_timeout,
                pool_recycle=self.db_config.pool_recycle,
                echo=settings.app.debug
            )
            
            # 创建会话工厂
            self._sync_session_factory = sessionmaker(
                bind=self._sync_engine,
                expire_on_commit=False
            )
            
            self._async_session_factory = async_sessionmaker(
                bind=self._async_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
        except Exception as e:
            raise DatabaseConnectionError(self.db_config.get_async_url(), e)
    
    @beartype
    async def cleanup(self) -> None:
        """
        清理数据库连接
        """
        if self._async_engine:
            await self._async_engine.dispose()
            self._async_engine = None
        
        if self._sync_engine:
            self._sync_engine.dispose()
            self._sync_engine = None
        
        self._sync_session_factory = None
        self._async_session_factory = None
    
    @property
    def sync_engine(self):
        """
        获取同步数据库引擎
        
        Returns:
            Engine: 同步数据库引擎
        """
        if not self._sync_engine:
            raise DatabaseConnectionError("sync_engine", Exception("Database not initialized"))
        return self._sync_engine
    
    @property
    def async_engine(self):
        """
        获取异步数据库引擎
        
        Returns:
            AsyncEngine: 异步数据库引擎
        """
        if not self._async_engine:
            raise DatabaseConnectionError("async_engine", Exception("Database not initialized"))
        return self._async_engine
    
    @beartype
    async def create_tables(self) -> None:
        """
        创建数据库表结构
        """
        try:
            # 使用异步引擎创建表
            async with self._async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            raise RepositoryError(f"Failed to create database tables: {str(e)}", e)
    
    @beartype
    async def drop_tables(self) -> None:
        """
        删除所有表（谨慎使用）
        """
        try:
            async with self._async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
        except Exception as e:
            raise RepositoryError(f"Failed to drop database tables: {str(e)}", e)
    
    @asynccontextmanager
    async def get_async_session(self):
        """
        获取异步数据库会话的上下文管理器
        
        Yields:
            AsyncSession: 异步数据库会话
        """
        if not self._async_session_factory:
            raise DatabaseConnectionError("async_session", Exception("Database not initialized"))
        
        async with self._async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    @asynccontextmanager
    async def get_sync_session(self):
        """
        获取同步数据库会话的上下文管理器
        
        Yields:
            Session: 同步数据库会话
        """
        if not self._sync_session_factory:
            raise DatabaseConnectionError("sync_session", Exception("Database not initialized"))
        
        with self._sync_session_factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise


class UserDatabaseRepository(BaseRepository[UserModel]):
    """
    用户数据库仓储类
    使用SQLAlchemy和MySQL实现用户数据的数据库访问
    """
    
    @beartype
    def __init__(self, db_manager: DatabaseManager):
        """
        初始化用户数据库仓储
        
        Args:
            db_manager: 数据库管理器实例
        """
        self.db_manager = db_manager
    
    @beartype
    def _db_to_model(self, db_user: UserDB) -> UserModel:
        """
        将数据库模型转换为业务模型
        
        Args:
            db_user: 数据库用户模型
            
        Returns:
            UserModel: 业务用户模型
        """
        return UserModel(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            full_name=db_user.full_name,
            age=db_user.age,
            is_active=db_user.is_active,
            roles=db_user.roles or [],
            permissions=db_user.permissions or [],
            login_count=db_user.login_count,
            last_login=db_user.last_login.isoformat() if db_user.last_login else None,
            created_at=db_user.created_at.isoformat() if db_user.created_at else None,
            updated_at=db_user.updated_at.isoformat() if db_user.updated_at else None
        )
    
    @beartype
    def _model_to_db(self, user: UserModel, db_user: Optional[UserDB] = None) -> UserDB:
        """
        将业务模型转换为数据库模型
        
        Args:
            user: 业务用户模型
            db_user: 已存在的数据库用户模型（用于更新）
            
        Returns:
            UserDB: 数据库用户模型
        """
        if db_user is None:
            db_user = UserDB()
        
        db_user.username = user.username
        db_user.email = user.email
        db_user.full_name = user.full_name
        db_user.age = user.age
        db_user.is_active = user.is_active
        db_user.roles = user.roles
        db_user.permissions = user.permissions
        db_user.login_count = user.login_count
        
        if user.last_login:
            try:
                db_user.last_login = datetime.fromisoformat(user.last_login)
            except (ValueError, TypeError):
                db_user.last_login = None
        
        return db_user
    
    @beartype
    async def create(self, entity: UserModel) -> UserModel:
        """
        创建新用户
        
        Args:
            entity: 用户实体
            
        Returns:
            UserModel: 创建后的用户
        """
        try:
            async with self.db_manager.get_async_session() as session:
                # 转换为数据库模型
                db_user = self._model_to_db(entity)
                
                # 添加到会话
                session.add(db_user)
                await session.flush()  # 获取生成的ID
                
                # 转换回业务模型
                return self._db_to_model(db_user)
                
        except IntegrityError as e:
            if "username" in str(e):
                raise RepositoryError(f"用户名 '{entity.username}' 已存在", e)
            elif "email" in str(e):
                raise RepositoryError(f"邮箱 '{entity.email}' 已存在", e)
            else:
                raise RepositoryError(f"创建用户失败: {str(e)}", e)
        except Exception as e:
            raise RepositoryError(f"创建用户失败: {str(e)}", e)
    
    @beartype
    async def get_by_id(self, entity_id: int) -> Optional[UserModel]:
        """
        根据ID获取用户
        
        Args:
            entity_id: 用户ID
            
        Returns:
            Optional[UserModel]: 用户对象或None
        """
        try:
            async with self.db_manager.get_async_session() as session:
                # 使用SQLAlchemy查询
                stmt = select(UserDB).where(UserDB.id == entity_id)
                result = await session.execute(stmt)
                db_user = result.scalar_one_or_none()
                
                if db_user:
                    return self._db_to_model(db_user)
                return None
                
        except Exception as e:
            raise RepositoryError(f"获取用户失败: {str(e)}", e)
    
    @beartype
    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[UserModel]:
        """
        获取所有用户
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[UserModel]: 用户列表
        """
        try:
            async with self.db_manager.get_async_session() as session:
                # 构建查询
                stmt = select(UserDB).order_by(UserDB.created_at.desc())
                
                if offset > 0:
                    stmt = stmt.offset(offset)
                if limit:
                    stmt = stmt.limit(limit)
                
                result = await session.execute(stmt)
                db_users = result.scalars().all()
                
                return [self._db_to_model(db_user) for db_user in db_users]
                
        except Exception as e:
            raise RepositoryError(f"获取用户列表失败: {str(e)}", e)
    
    @beartype
    async def update(self, entity: UserModel) -> UserModel:
        """
        更新用户
        
        Args:
            entity: 用户实体
            
        Returns:
            UserModel: 更新后的用户
        """
        try:
            async with self.db_manager.get_async_session() as session:
                # 查找现有用户
                stmt = select(UserDB).where(UserDB.id == entity.id)
                result = await session.execute(stmt)
                db_user = result.scalar_one_or_none()
                
                if not db_user:
                    raise EntityNotFoundError("User", entity.id)
                
                # 更新数据
                self._model_to_db(entity, db_user)
                
                # 提交更新
                await session.flush()
                
                return self._db_to_model(db_user)
                
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise RepositoryError(f"更新用户失败: {str(e)}", e)
    
    @beartype
    async def delete(self, entity_id: int) -> bool:
        """
        删除用户
        
        Args:
            entity_id: 用户ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            async with self.db_manager.get_async_session() as session:
                # 查找用户
                stmt = select(UserDB).where(UserDB.id == entity_id)
                result = await session.execute(stmt)
                db_user = result.scalar_one_or_none()
                
                if not db_user:
                    return False
                
                # 删除用户
                await session.delete(db_user)
                
                return True
                
        except Exception as e:
            raise RepositoryError(f"删除用户失败: {str(e)}", e)
    
    @beartype
    async def exists(self, entity_id: int) -> bool:
        """
        检查用户是否存在
        
        Args:
            entity_id: 用户ID
            
        Returns:
            bool: 是否存在
        """
        try:
            async with self.db_manager.get_async_session() as session:
                stmt = select(func.count(UserDB.id)).where(UserDB.id == entity_id)
                result = await session.execute(stmt)
                count = result.scalar()
                
                return count > 0
                
        except Exception as e:
            raise RepositoryError(f"检查用户存在失败: {str(e)}", e)
    
    @beartype
    async def count(self) -> int:
        """
        获取用户总数
        
        Returns:
            int: 用户总数
        """
        try:
            async with self.db_manager.get_async_session() as session:
                stmt = select(func.count(UserDB.id))
                result = await session.execute(stmt)
                count = result.scalar()
                
                return count or 0
                
        except Exception as e:
            raise RepositoryError(f"获取用户总数失败: {str(e)}", e)
    
    @beartype
    async def find_by_username(self, username: str) -> Optional[UserModel]:
        """
        根据用户名查找用户
        
        Args:
            username: 用户名
            
        Returns:
            Optional[UserModel]: 用户对象或None
        """
        try:
            async with self.db_manager.get_async_session() as session:
                stmt = select(UserDB).where(UserDB.username == username)
                result = await session.execute(stmt)
                db_user = result.scalar_one_or_none()
                
                if db_user:
                    return self._db_to_model(db_user)
                return None
                
        except Exception as e:
            raise RepositoryError(f"根据用户名查找用户失败: {str(e)}", e)
    
    @beartype
    async def simulate_slow_database_operation(self, duration: float = 2.0) -> Dict[str, Any]:
        """
        模拟耗时的数据库操作
        用于测试异步和线程处理
        
        Args:
            duration: 模拟耗时（秒）
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        await asyncio.sleep(duration)
        
        # 模拟一些数据库统计操作
        user_count = await self.count()
        
        return {
            "operation": "slow_database_query",
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "result": "数据库操作完成",
            "data": {
                "total_users": user_count,
                "query_time": duration,
                "cache_hit_rate": 0.85
            }
        }
    
    @beartype
    async def find_by_criteria(self, criteria: Dict[str, Any]) -> List[UserModel]:
        """
        根据条件查找用户
        
        Args:
            criteria: 查询条件字典
            
        Returns:
            List[UserModel]: 符合条件的用户列表
        """
        try:
            async with self.db_manager.get_async_session() as session:
                stmt = select(UserDB)
                
                # 根据条件构建查询
                if 'is_active' in criteria:
                    stmt = stmt.where(UserDB.is_active == criteria['is_active'])
                
                if 'username_like' in criteria:
                    stmt = stmt.where(UserDB.username.like(f"%{criteria['username_like']}%"))
                
                if 'email_like' in criteria:
                    stmt = stmt.where(UserDB.email.like(f"%{criteria['email_like']}%"))
                
                if 'min_age' in criteria:
                    stmt = stmt.where(UserDB.age >= criteria['min_age'])
                
                if 'max_age' in criteria:
                    stmt = stmt.where(UserDB.age <= criteria['max_age'])
                
                if 'roles' in criteria:
                    # JSON查询，检查是否包含指定角色
                    for role in criteria['roles']:
                        stmt = stmt.where(UserDB.roles.contains([role]))
                
                result = await session.execute(stmt)
                db_users = result.scalars().all()
                
                return [self._db_to_model(db_user) for db_user in db_users]
                
        except Exception as e:
            raise RepositoryError(f"根据条件查找用户失败: {str(e)}", e)
