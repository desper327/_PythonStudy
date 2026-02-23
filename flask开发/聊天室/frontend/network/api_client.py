"""
REST API客户端
用于与后端API通信
"""
import requests
from typing import Dict, Any, Optional
from config import Config


class APIClient:
    """API客户端类"""
    
    def __init__(self):
        """初始化API客户端"""
        self.base_url = Config.SERVER_HOST
        self.token = None
        self.timeout = 10  # 请求超时时间（秒）
    
    def set_token(self, token: str):
        """
        设置认证Token
        
        Args:
            token: JWT Token
        """
        self.token = token
    
    def get_headers(self) -> Dict[str, str]:
        """
        获取请求头
        
        Returns:
            Dict: 请求头字典
        """
        headers = {
            'Content-Type': 'application/json'
        }
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        return headers
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: 请求方法（GET/POST/PUT/DELETE）
            endpoint: API端点
            **kwargs: 其他请求参数
            
        Returns:
            Dict: 响应数据
            
        Raises:
            Exception: 请求失败
        """
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            
            # 解析响应
            data = response.json()
            return data
            
        except requests.exceptions.Timeout:
            return {
                'code': 500,
                'message': '请求超时',
                'data': None
            }
        except requests.exceptions.ConnectionError:
            return {
                'code': 500,
                'message': '无法连接到服务器',
                'data': None
            }
        except Exception as e:
            return {
                'code': 500,
                'message': f'请求失败: {str(e)}',
                'data': None
            }
    
    # ========== 认证接口 ==========
    
    def register(self, username: str, password: str, nickname: str, email: str = None) -> Dict[str, Any]:
        """
        用户注册
        
        Args:
            username: 用户名
            password: 密码
            nickname: 昵称
            email: 邮箱（可选）
            
        Returns:
            Dict: 响应数据
        """
        return self._request(
            'POST',
            '/api/auth/register',
            json={
                'username': username,
                'password': password,
                'nickname': nickname,
                'email': email
            }
        )
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            Dict: 响应数据
        """
        return self._request(
            'POST',
            '/api/auth/login',
            json={
                'username': username,
                'password': password
            }
        )
    
    # ========== 用户接口 ==========
    
    def get_current_user(self) -> Dict[str, Any]:
        """
        获取当前用户信息
        
        Returns:
            Dict: 响应数据
        """
        return self._request('GET', '/api/users/me')
    
    def update_user(self, nickname: str = None, email: str = None, avatar: str = None) -> Dict[str, Any]:
        """
        更新用户信息
        
        Args:
            nickname: 昵称
            email: 邮箱
            avatar: 头像
            
        Returns:
            Dict: 响应数据
        """
        data = {}
        if nickname is not None:
            data['nickname'] = nickname
        if email is not None:
            data['email'] = email
        if avatar is not None:
            data['avatar'] = avatar
        
        return self._request('PUT', '/api/users/me', json=data)
    
    def change_password(self, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        修改密码
        
        Args:
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            Dict: 响应数据
        """
        return self._request(
            'PUT',
            '/api/users/me/password',
            json={
                'old_password': old_password,
                'new_password': new_password
            }
        )
    
    def search_users(self, keyword: str) -> Dict[str, Any]:
        """
        搜索用户
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            Dict: 响应数据
        """
        return self._request('GET', '/api/users/search', params={'keyword': keyword})
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        获取指定用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 响应数据
        """
        return self._request('GET', f'/api/users/{user_id}')
    
    # ========== 群组接口 ==========
    
    def create_group(self, name: str, description: str = None, group_type: str = 'public') -> Dict[str, Any]:
        """
        创建群组
        
        Args:
            name: 群组名称
            description: 群组描述
            group_type: 群组类型（public/private）
            
        Returns:
            Dict: 响应数据
        """
        return self._request(
            'POST',
            '/api/groups',
            json={
                'name': name,
                'description': description,
                'type': group_type
            }
        )
    
    def get_my_groups(self) -> Dict[str, Any]:
        """
        获取我的群组列表
        
        Returns:
            Dict: 响应数据
        """
        return self._request('GET', '/api/groups')
    
    def get_public_groups(self) -> Dict[str, Any]:
        """
        获取公开群组列表
        
        Returns:
            Dict: 响应数据
        """
        return self._request('GET', '/api/groups/public')
    
    def get_group(self, group_id: int) -> Dict[str, Any]:
        """
        获取群组详情
        
        Args:
            group_id: 群组ID
            
        Returns:
            Dict: 响应数据
        """
        return self._request('GET', f'/api/groups/{group_id}')
    
    def join_group(self, group_id: int) -> Dict[str, Any]:
        """
        加入群组
        
        Args:
            group_id: 群组ID
            
        Returns:
            Dict: 响应数据
        """
        return self._request('POST', f'/api/groups/{group_id}/join')
    
    def leave_group(self, group_id: int) -> Dict[str, Any]:
        """
        退出群组
        
        Args:
            group_id: 群组ID
            
        Returns:
            Dict: 响应数据
        """
        return self._request('DELETE', f'/api/groups/{group_id}/leave')
    
    def get_group_members(self, group_id: int) -> Dict[str, Any]:
        """
        获取群组成员列表
        
        Args:
            group_id: 群组ID
            
        Returns:
            Dict: 响应数据
        """
        return self._request('GET', f'/api/groups/{group_id}/members')
    
    def kick_member(self, group_id: int, user_id: int) -> Dict[str, Any]:
        """
        踢出成员
        
        Args:
            group_id: 群组ID
            user_id: 用户ID
            
        Returns:
            Dict: 响应数据
        """
        return self._request('DELETE', f'/api/groups/{group_id}/members/{user_id}')
    
    # ========== 消息接口 ==========
    
    def get_private_messages(self, user_id: int, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """
        获取私聊消息历史
        
        Args:
            user_id: 对方用户ID
            page: 页码
            per_page: 每页数量
            
        Returns:
            Dict: 响应数据
        """
        return self._request(
            'GET',
            f'/api/messages/private/{user_id}',
            params={'page': page, 'per_page': per_page}
        )
    
    def get_group_messages(self, group_id: int, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """
        获取群组消息历史
        
        Args:
            group_id: 群组ID
            page: 页码
            per_page: 每页数量
            
        Returns:
            Dict: 响应数据
        """
        return self._request(
            'GET',
            f'/api/messages/group/{group_id}',
            params={'page': page, 'per_page': per_page}
        )
