"""
用户业务服务
包含用户相关的所有业务逻辑处理
"""
import asyncio
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
from beartype import beartype
from models.user_model import UserModel, UserListModel
from models.base_model import TaskStatus
from repositories.api_client import ApiClient, UserApiRepository
from repositories.database import DatabaseManager, UserDatabaseRepository


class UserService:
    """
    用户业务服务类
    封装用户相关的所有业务逻辑，协调API和数据库操作
    """
    
    @beartype
    def __init__(
        self, 
        api_client: ApiClient, 
        db_manager: DatabaseManager,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ):
        """
        初始化用户服务
        
        Args:
            api_client: API客户端
            db_manager: 数据库管理器
            progress_callback: 进度回调函数
        """
        self.api_repository = UserApiRepository(api_client)
        self.db_repository = UserDatabaseRepository(db_manager)
        self.progress_callback = progress_callback
    
    @beartype
    def _update_progress(self, progress: float, message: str) -> None:
        """
        更新进度
        
        Args:
            progress: 进度百分比
            message: 进度消息
        """
        if self.progress_callback:
            self.progress_callback(progress, message)
    
    @beartype
    async def create_user(self, user_data: Dict[str, Any]) -> UserModel:
        """
        创建新用户
        业务逻辑：先验证数据，然后同时保存到本地数据库和远程API
        
        Args:
            user_data: 用户数据字典
            
        Returns:
            UserModel: 创建的用户
            
        Raises:
            ValueError: 数据验证失败
        """
        self._update_progress(10, "验证用户数据...")
        
        # 1. 创建用户模型并验证数据
        user = UserModel(**user_data)
        
        self._update_progress(30, "检查用户名是否已存在...")
        
        # 2. 检查用户名是否已存在（业务规则）
        existing_user = await self.db_repository.find_by_username(user.username)
        if existing_user:
            raise ValueError(f"用户名 '{user.username}' 已存在")
        
        self._update_progress(50, "保存到本地数据库...")
        
        # 3. 保存到本地数据库
        created_user = await self.db_repository.create(user)
        
        self._update_progress(80, "同步到远程服务器...")
        
        # 4. 尝试同步到远程API（可选，失败不影响本地创建）
        try:
            await self.api_repository.create(user)
        except Exception as e:
            # 记录错误但不抛出异常
            print(f"远程同步失败: {e}")
        
        self._update_progress(100, "用户创建完成")
        
        return created_user
    
    @beartype
    async def get_user_by_id(self, user_id: int, prefer_local: bool = True) -> Optional[UserModel]:
        """
        根据ID获取用户
        业务逻辑：优先从本地获取，如果本地没有则从远程获取并缓存
        
        Args:
            user_id: 用户ID
            prefer_local: 是否优先使用本地数据
            
        Returns:
            Optional[UserModel]: 用户对象或None
        """
        self._update_progress(20, "查找用户...")
        
        user = None
        
        if prefer_local:
            # 先从本地数据库查找
            user = await self.db_repository.get_by_id(user_id)
            
            if not user:
                self._update_progress(60, "本地未找到，从远程获取...")
                # 本地没有，从远程API获取
                user = await self.api_repository.get_by_id(user_id)
                
                if user:
                    # 缓存到本地数据库
                    try:
                        await self.db_repository.create(user)
                    except Exception:
                        # 可能已存在，忽略错误
                        pass
        else:
            # 直接从远程API获取
            user = await self.api_repository.get_by_id(user_id)
        
        self._update_progress(100, "查找完成")
        
        return user
    
    @beartype
    async def get_all_users(
        self, 
        limit: Optional[int] = None, 
        sync_remote: bool = False
    ) -> UserListModel:
        """
        获取所有用户
        业务逻辑：从本地获取，可选择同步远程数据
        
        Args:
            limit: 限制数量
            sync_remote: 是否同步远程数据
            
        Returns:
            UserListModel: 用户列表模型
        """
        self._update_progress(10, "获取用户列表...")
        
        if sync_remote:
            await self._sync_users_from_remote()
        
        self._update_progress(70, "从本地数据库获取用户...")
        
        # 从本地数据库获取用户
        users = await self.db_repository.get_all(limit=limit)
        
        self._update_progress(90, "构建用户列表模型...")
        
        # 创建用户列表模型
        user_list = UserListModel()
        for user in users:
            user_list.add_user(user)
        
        self._update_progress(100, "获取完成")
        
        return user_list
    
    @beartype
    async def update_user(self, user: UserModel) -> UserModel:
        """
        更新用户
        业务逻辑：更新本地数据库，同时尝试同步到远程
        
        Args:
            user: 用户对象
            
        Returns:
            UserModel: 更新后的用户
        """
        self._update_progress(20, "验证用户数据...")
        
        # 验证用户存在
        if not await self.db_repository.exists(user.id):
            raise ValueError(f"用户ID {user.id} 不存在")
        
        self._update_progress(50, "更新本地数据库...")
        
        # 更新本地数据库
        updated_user = await self.db_repository.update(user)
        
        self._update_progress(80, "同步到远程服务器...")
        
        # 尝试同步到远程API
        try:
            await self.api_repository.update(user)
        except Exception as e:
            print(f"远程同步失败: {e}")
        
        self._update_progress(100, "更新完成")
        
        return updated_user
    
    @beartype
    async def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        业务逻辑：从本地和远程同时删除
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 是否删除成功
        """
        self._update_progress(20, "验证用户存在...")
        
        # 验证用户存在
        if not await self.db_repository.exists(user_id):
            return False
        
        self._update_progress(50, "从本地数据库删除...")
        
        # 从本地数据库删除
        local_success = await self.db_repository.delete(user_id)
        
        self._update_progress(80, "从远程服务器删除...")
        
        # 尝试从远程API删除
        try:
            await self.api_repository.delete(user_id)
        except Exception as e:
            print(f"远程删除失败: {e}")
        
        self._update_progress(100, "删除完成")
        
        return local_success
    
    @beartype
    async def _sync_users_from_remote(self) -> None:
        """
        从远程API同步用户数据到本地
        内部业务逻辑方法
        """
        self._update_progress(30, "从远程API获取用户...")
        
        try:
            # 从远程API获取用户
            remote_users = await self.api_repository.get_all(limit=10)
            
            self._update_progress(60, "同步到本地数据库...")
            
            # 同步到本地数据库
            for user in remote_users:
                try:
                    # 检查本地是否已存在
                    existing = await self.db_repository.get_by_id(user.id)
                    if not existing:
                        await self.db_repository.create(user)
                    else:
                        # 更新现有用户
                        user.created_at = existing.created_at  # 保持原创建时间
                        await self.db_repository.update(user)
                except Exception as e:
                    print(f"同步用户 {user.id} 失败: {e}")
                    
        except Exception as e:
            print(f"远程同步失败: {e}")
    
    @beartype
    async def process_user_batch(
        self, 
        user_ids: List[int],
        operation: str = "activate"
    ) -> Dict[str, Any]:
        """
        批量处理用户
        业务逻辑：批量激活/停用用户，展示复杂业务操作
        
        Args:
            user_ids: 用户ID列表
            operation: 操作类型 ("activate" 或 "deactivate")
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        self._update_progress(0, f"开始批量{operation}用户...")
        
        results = {
            "total": len(user_ids),
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        for i, user_id in enumerate(user_ids):
            try:
                progress = (i + 1) / len(user_ids) * 100
                self._update_progress(progress, f"处理用户 {user_id}...")
                
                # 获取用户
                user = await self.db_repository.get_by_id(user_id)
                if not user:
                    results["errors"].append(f"用户 {user_id} 不存在")
                    results["failed"] += 1
                    continue
                
                # 执行操作
                if operation == "activate":
                    user.activate()
                elif operation == "deactivate":
                    user.deactivate()
                else:
                    raise ValueError(f"不支持的操作: {operation}")
                
                # 更新用户
                await self.db_repository.update(user)
                results["success"] += 1
                
                # 模拟一些处理时间
                await asyncio.sleep(0.1)
                
            except Exception as e:
                results["errors"].append(f"处理用户 {user_id} 失败: {str(e)}")
                results["failed"] += 1
        
        self._update_progress(100, "批量处理完成")
        
        return results
    
    @beartype
    async def generate_user_report(self) -> Dict[str, Any]:
        """
        生成用户报告
        业务逻辑：统计用户数据，生成报告
        
        Returns:
            Dict[str, Any]: 用户报告
        """
        self._update_progress(10, "收集用户数据...")
        
        # 获取所有用户
        users = await self.db_repository.get_all()
        
        self._update_progress(50, "分析用户数据...")
        
        # 统计分析
        total_users = len(users)
        active_users = len([u for u in users if u.is_active])
        inactive_users = total_users - active_users
        
        # 角色统计
        role_stats = {}
        for user in users:
            for role in user.roles:
                role_stats[role] = role_stats.get(role, 0) + 1
        
        # 登录统计
        total_logins = sum(user.login_count for user in users)
        avg_logins = total_logins / total_users if total_users > 0 else 0
        
        self._update_progress(80, "生成报告...")
        
        # 模拟报告生成时间
        await asyncio.sleep(1)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": inactive_users,
                "activation_rate": active_users / total_users if total_users > 0 else 0
            },
            "login_stats": {
                "total_logins": total_logins,
                "average_logins_per_user": avg_logins
            },
            "role_distribution": role_stats,
            "recent_users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "created_at": user.created_at
                }
                for user in sorted(users, key=lambda x: x.created_at or "", reverse=True)[:5]
            ]
        }
        
        self._update_progress(100, "报告生成完成")
        
        return report
