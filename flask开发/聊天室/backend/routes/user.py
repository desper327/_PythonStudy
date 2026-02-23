"""
用户路由
处理用户信息相关请求
"""
from flask import Blueprint, request
from models import User
from models.user import db
from utils import token_required, success_response, error_response

# 创建蓝图
user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """
    获取当前用户信息
    
    Headers:
        Authorization: Bearer <token>
    """
    try:
        # 从token中获取用户ID
        user_id = request.user_id
        
        # 查询用户
        user = User.query.get(user_id)
        if not user:
            return error_response('用户不存在', 404)
        
        return success_response(
            data=user.to_dict(include_email=True),
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取用户信息失败: {str(e)}', 500)


@user_bp.route('/me', methods=['PUT'])
@token_required
def update_current_user():
    """
    更新当前用户信息
    
    Headers:
        Authorization: Bearer <token>
        
    请求体:
        {
            "nickname": "string (optional)",
            "email": "string (optional)",
            "avatar": "string (optional)"
        }
    """
    try:
        # 从token中获取用户ID
        user_id = request.user_id
        
        # 查询用户
        user = User.query.get(user_id)
        if not user:
            return error_response('用户不存在', 404)
        
        # 获取请求数据
        data = request.get_json()
        
        # 更新昵称
        if 'nickname' in data:
            nickname = data['nickname'].strip()
            if nickname:
                user.nickname = nickname
        
        # 更新邮箱
        if 'email' in data:
            email = data['email'].strip() or None
            if email:
                # 检查邮箱是否已被其他用户使用
                existing_user = User.query.filter_by(email=email).first()
                if existing_user and existing_user.id != user_id:
                    return error_response('邮箱已被其他用户使用', 400)
            user.email = email
        
        # 更新头像
        if 'avatar' in data:
            user.avatar = data['avatar']
        
        # 保存更改
        db.session.commit()
        
        return success_response(
            data=user.to_dict(include_email=True),
            message='更新成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'更新用户信息失败: {str(e)}', 500)


@user_bp.route('/me/password', methods=['PUT'])
@token_required
def change_password():
    """
    修改密码
    
    Headers:
        Authorization: Bearer <token>
        
    请求体:
        {
            "old_password": "string",
            "new_password": "string"
        }
    """
    try:
        # 从token中获取用户ID
        user_id = request.user_id
        
        # 查询用户
        user = User.query.get(user_id)
        if not user:
            return error_response('用户不存在', 404)
        
        # 获取请求数据
        data = request.get_json()
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        # 验证必填字段
        if not all([old_password, new_password]):
            return error_response('旧密码和新密码不能为空', 400)
        
        # 验证旧密码
        if not user.check_password(old_password):
            return error_response('旧密码错误', 401)
        
        # 验证新密码强度
        valid, msg = User.validate_password(new_password)
        if not valid:
            return error_response(msg, 400)
        
        # 设置新密码
        user.set_password(new_password)
        db.session.commit()
        
        return success_response(message='密码修改成功')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'修改密码失败: {str(e)}', 500)


@user_bp.route('/search', methods=['GET'])
@token_required
def search_users():
    """
    搜索用户
    
    Headers:
        Authorization: Bearer <token>
        
    Query参数:
        keyword: 搜索关键词（用户名或昵称）
    """
    try:
        keyword = request.args.get('keyword', '').strip()
        
        if not keyword:
            return error_response('搜索关键词不能为空', 400)
        
        # 搜索用户（用户名或昵称包含关键词）
        users = User.query.filter(
            db.or_(
                User.username.like(f'%{keyword}%'),
                User.nickname.like(f'%{keyword}%')
            ),
            User.status == 'active'
        ).limit(20).all()
        
        # 转换为字典列表
        user_list = [user.to_dict() for user in users]
        
        return success_response(
            data={'users': user_list, 'count': len(user_list)},
            message='搜索成功'
        )
        
    except Exception as e:
        return error_response(f'搜索用户失败: {str(e)}', 500)


@user_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """
    获取指定用户信息
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        user_id: 用户ID
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return error_response('用户不存在', 404)
        
        if user.status != 'active':
            return error_response('用户已被禁用或删除', 404)
        
        return success_response(
            data=user.to_dict(),
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取用户信息失败: {str(e)}', 500)
