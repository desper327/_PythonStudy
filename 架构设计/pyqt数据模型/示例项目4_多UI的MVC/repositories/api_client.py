"""
API客户端
负责与外部API进行通信，获取远程数据
"""
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import aiohttp
from beartype import beartype
from models.user_model import UserModel
from .base_repository import BaseRepository, RepositoryError


class ApiClient:
    """
    API客户端类
    封装所有HTTP请求逻辑，提供统一的API访问接口
    """
    
    @beartype
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com", timeout: int = 30):
        """
        初始化API客户端
        
        Args:
            base_url: API基础URL
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'MVC-Framework/1.0'
        }
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.disconnect()
    
    @beartype
    async def connect(self) -> None:
        """
        建立HTTP会话连接
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers=self.headers
            )
    
    @beartype
    async def disconnect(self) -> None:
        """
        关闭HTTP会话连接
        """
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    @beartype
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发起HTTP请求的通用方法
        
        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求体数据
            params: URL参数
            
        Returns:
            Dict[str, Any]: 响应数据
            
        Raises:
            RepositoryError: 请求失败时抛出
        """
        if not self.session:
            await self.connect()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                json=data,
                params=params
            ) as response:
                
                # 检查响应状态
                if response.status >= 400:
                    error_text = await response.text()
                    raise RepositoryError(
                        f"API request failed: {response.status} - {error_text}"
                    )
                
                # 解析JSON响应
                try:
                    return await response.json()
                except json.JSONDecodeError:
                    # 如果不是JSON响应，返回文本内容
                    text = await response.text()
                    return {"data": text}
                    
        except aiohttp.ClientError as e:
            raise RepositoryError(f"HTTP client error: {str(e)}", e)
        except asyncio.TimeoutError as e:
            raise RepositoryError(f"Request timeout: {url}", e)
    
    @beartype
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发起GET请求
        
        Args:
            endpoint: API端点
            params: URL参数
            
        Returns:
            Dict[str, Any]: 响应数据
        """
        return await self._make_request("GET", endpoint, params=params)
    
    @beartype
    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发起POST请求
        
        Args:
            endpoint: API端点
            data: 请求体数据
            
        Returns:
            Dict[str, Any]: 响应数据
        """
        return await self._make_request("POST", endpoint, data=data)
    
    @beartype
    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发起PUT请求
        
        Args:
            endpoint: API端点
            data: 请求体数据
            
        Returns:
            Dict[str, Any]: 响应数据
        """
        return await self._make_request("PUT", endpoint, data=data)
    
    @beartype
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        发起DELETE请求
        
        Args:
            endpoint: API端点
            
        Returns:
            Dict[str, Any]: 响应数据
        """
        return await self._make_request("DELETE", endpoint)


class UserApiRepository(BaseRepository[UserModel]):
    """
    用户API仓储类
    实现用户数据的远程API访问
    """
    
    @beartype
    def __init__(self, api_client: ApiClient):
        """
        初始化用户API仓储
        
        Args:
            api_client: API客户端实例
        """
        self.api_client = api_client
    
    @beartype
    async def create(self, entity: UserModel) -> UserModel:
        """
        创建新用户（模拟）
        
        Args:
            entity: 用户实体
            
        Returns:
            UserModel: 创建后的用户
        """
        # 模拟创建用户的API调用
        user_data = entity.to_dict()
        user_data.pop('id', None)  # 移除ID，让服务器生成
        
        response = await self.api_client.post("/users", user_data)
        
        # 模拟服务器返回的用户数据
        response['id'] = response.get('id', 101)  # JSONPlaceholder返回的ID
        response['created_at'] = datetime.now().isoformat()
        response['updated_at'] = datetime.now().isoformat()
        
        return UserModel(**response)
    
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
            response = await self.api_client.get(f"/users/{entity_id}")
            
            # 转换API响应为用户模型
            user_data = {
                'id': response['id'],
                'username': response['username'],
                'email': response['email'],
                'full_name': response.get('name', ''),
                'is_active': True,
                'roles': ['user'],
                'permissions': [],
                'login_count': 0,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            return UserModel(**user_data)
            
        except RepositoryError:
            return None
    
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
        params = {}
        if limit:
            params['_limit'] = limit
        if offset:
            params['_start'] = offset
        
        response = await self.api_client.get("/users", params)
        
        users = []
        for user_data in response:
            user = {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'full_name': user_data.get('name', ''),
                'is_active': True,
                'roles': ['user'],
                'permissions': [],
                'login_count': 0,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            users.append(UserModel(**user))
        
        return users
    
    @beartype
    async def update(self, entity: UserModel) -> UserModel:
        """
        更新用户
        
        Args:
            entity: 用户实体
            
        Returns:
            UserModel: 更新后的用户
        """
        user_data = entity.to_dict()
        response = await self.api_client.put(f"/users/{entity.id}", user_data)
        
        # 更新时间戳
        response['updated_at'] = datetime.now().isoformat()
        
        return UserModel(**response)
    
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
            await self.api_client.delete(f"/users/{entity_id}")
            return True
        except RepositoryError:
            return False
    
    @beartype
    async def exists(self, entity_id: int) -> bool:
        """
        检查用户是否存在
        
        Args:
            entity_id: 用户ID
            
        Returns:
            bool: 是否存在
        """
        user = await self.get_by_id(entity_id)
        return user is not None
    
    @beartype
    async def count(self) -> int:
        """
        获取用户总数
        
        Returns:
            int: 用户总数
        """
        users = await self.get_all()
        return len(users)
    
    @beartype
    async def simulate_slow_operation(self, duration: float = 3.0) -> Dict[str, Any]:
        """
        模拟耗时的API操作
        用于测试异步和线程处理
        
        Args:
            duration: 模拟耗时（秒）
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        await asyncio.sleep(duration)
        
        return {
            "operation": "slow_api_call",
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "result": "操作完成",
            "data": {
                "processed_items": 100,
                "success_rate": 0.95
            }
        }
