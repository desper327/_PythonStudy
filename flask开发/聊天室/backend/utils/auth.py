"""
JWT认证工具函数
用于生成和验证JWT Token
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app


def create_token(user_id, username):
    """
    创建JWT Token
    
    Args:
        user_id: 用户ID
        username: 用户名
        
    Returns:
        str: JWT Token字符串
    """
    # Token过期时间
    expire_hours = current_app.config.get('JWT_EXPIRE_HOURS', 24)
    expire_time = datetime.utcnow() + timedelta(hours=expire_hours)
    
    # Token载荷
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': expire_time,  # 过期时间
        'iat': datetime.utcnow()  # 签发时间
    }
    
    # 生成Token
    secret_key = current_app.config.get('JWT_SECRET_KEY')
    algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    
    return token


def verify_token(token):
    """
    验证JWT Token
    
    Args:
        token: JWT Token字符串
        
    Returns:
        dict or None: Token载荷（验证成功）或 None（验证失败）
    """
    try:
        secret_key = current_app.config.get('JWT_SECRET_KEY')
        algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
        
        # 解码Token
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
        
    except jwt.ExpiredSignatureError:
        # Token已过期
        return None
    except jwt.InvalidTokenError:
        # Token无效
        return None


def token_required(f):
    """
    装饰器：需要Token认证
    
    使用方法：
        @token_required
        def some_route():
            # 可以通过 request.user_id 和 request.username 获取用户信息
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取Token
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            # 格式: "Bearer <token>"
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        # 如果没有Token
        if not token:
            return jsonify({
                'code': 401,
                'message': '缺少认证Token',
                'data': None
            }), 401
        
        # 验证Token
        payload = verify_token(token)
        if not payload:
            return jsonify({
                'code': 401,
                'message': 'Token无效或已过期',
                'data': None
            }), 401
        
        # 将用户信息添加到request对象
        request.user_id = payload.get('user_id')
        request.username = payload.get('username')
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_token_from_request():
    """
    从请求中提取Token（不验证）
    
    Returns:
        str or None: Token字符串
    """
    auth_header = request.headers.get('Authorization')
    
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0] == 'Bearer':
            return parts[1]
    
    return None


def get_user_from_token():
    """
    从Token中获取用户信息
    
    Returns:
        dict or None: 用户信息（包含user_id和username）
    """
    token = get_token_from_request()
    if not token:
        return None
    
    payload = verify_token(token)
    if not payload:
        return None
    
    return {
        'user_id': payload.get('user_id'),
        'username': payload.get('username')
    }
