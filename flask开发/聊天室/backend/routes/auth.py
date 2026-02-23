"""
认证路由
处理用户注册、登录等认证相关请求
"""
from flask import Blueprint, request
from models import User
from models.user import db
from utils import create_token, success_response, error_response

# 创建蓝图
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    
    请求体:
        {
            "username": "string",
            "password": "string",
            "nickname": "string",
            "email": "string (optional)"
        }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        nickname = data.get('nickname', '').strip()
        email = data.get('email', '').strip() or None
        
        # 验证必填字段
        if not all([username, password, nickname]):
            return error_response('用户名、密码和昵称不能为空', 400)
        
        # 验证用户名格式
        valid, msg = User.validate_username(username)
        if not valid:
            return error_response(msg, 400)
        
        # 验证密码强度
        valid, msg = User.validate_password(password)
        if not valid:
            return error_response(msg, 400)
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return error_response('用户名已存在', 400)
        
        # 检查邮箱是否已存在
        if email and User.query.filter_by(email=email).first():
            return error_response('邮箱已被使用', 400)
        
        # 创建新用户
        user = User(
            username=username,
            nickname=nickname,
            email=email
        )
        user.set_password(password)
        
        # 保存到数据库
        db.session.add(user)
        db.session.commit()
        
        # 返回成功响应
        return success_response(
            data={
                'user_id': user.id,
                'username': user.username
            },
            message='注册成功',
            code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'注册失败: {str(e)}', 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    
    请求体:
        {
            "username": "string",
            "password": "string"
        }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # 验证必填字段
        if not all([username, password]):
            return error_response('用户名和密码不能为空', 400)
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        # 验证用户是否存在
        if not user:
            return error_response('用户名或密码错误', 401)
        
        # 验证用户状态
        if user.status != 'active':
            return error_response('账号已被禁用或删除', 403)
        
        # 验证密码
        if not user.check_password(password):
            return error_response('用户名或密码错误', 401)
        
        # 生成Token
        token = create_token(user.id, user.username)
        
        # 返回成功响应
        return success_response(
            data={
                'token': token,
                'user': user.to_dict(include_email=True)
            },
            message='登录成功'
        )
        
    except Exception as e:
        return error_response(f'登录失败: {str(e)}', 500)


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """
    检查认证状态（测试接口）
    
    Headers:
        Authorization: Bearer <token>
    """
    from utils.auth import get_user_from_token
    
    user_info = get_user_from_token()
    if not user_info:
        return error_response('未认证或Token无效', 401)
    
    return success_response(
        data=user_info,
        message='认证有效'
    )
