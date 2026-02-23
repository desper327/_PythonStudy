"""
群组路由
处理群组相关请求
"""
from flask import Blueprint, request
from models import Group, GroupMember, User
from models.user import db
from utils import token_required, success_response, error_response

# 创建蓝图
group_bp = Blueprint('group', __name__)


@group_bp.route('', methods=['POST'])
@token_required
def create_group():
    """
    创建群组
    
    Headers:
        Authorization: Bearer <token>
        
    请求体:
        {
            "name": "string",
            "description": "string (optional)",
            "type": "public/private"
        }
    """
    try:
        user_id = request.user_id
        data = request.get_json()
        
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        group_type = data.get('type', 'public')
        
        # 验证群组名称
        valid, msg = Group.validate_name(name)
        if not valid:
            return error_response(msg, 400)
        
        # 验证群组类型
        if group_type not in ['public', 'private']:
            return error_response('群组类型只能是public或private', 400)
        
        # 检查群组名是否已存在
        if Group.query.filter_by(name=name).first():
            return error_response('群组名称已存在', 400)
        
        # 创建群组
        group = Group(
            name=name,
            description=description,
            type=group_type,
            owner_id=user_id
        )
        db.session.add(group)
        db.session.flush()  # 获取group.id
        
        # 创建者自动成为群主
        member = GroupMember(
            group_id=group.id,
            user_id=user_id,
            role='owner'
        )
        db.session.add(member)
        db.session.commit()
        
        return success_response(
            data=group.to_dict(),
            message='群组创建成功',
            code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'创建群组失败: {str(e)}', 500)


@group_bp.route('', methods=['GET'])
@token_required
def get_my_groups():
    """
    获取我的群组列表
    
    Headers:
        Authorization: Bearer <token>
    """
    try:
        user_id = request.user_id
        
        # 查询用户加入的所有群组
        memberships = GroupMember.query.filter_by(user_id=user_id).all()
        groups = [membership.group for membership in memberships]
        
        # 转换为字典列表
        group_list = [group.to_dict() for group in groups]
        
        return success_response(
            data={'groups': group_list, 'count': len(group_list)},
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取群组列表失败: {str(e)}', 500)


@group_bp.route('/public', methods=['GET'])
@token_required
def get_public_groups():
    """
    获取公开群组列表
    
    Headers:
        Authorization: Bearer <token>
    """
    try:
        # 查询所有公开群组
        groups = Group.query.filter_by(type='public').all()
        
        # 转换为字典列表
        group_list = [group.to_dict() for group in groups]
        
        return success_response(
            data={'groups': group_list, 'count': len(group_list)},
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取公开群组失败: {str(e)}', 500)


@group_bp.route('/<int:group_id>', methods=['GET'])
@token_required
def get_group(group_id):
    """
    获取群组详情
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        group_id: 群组ID
    """
    try:
        user_id = request.user_id
        
        group = Group.query.get(group_id)
        if not group:
            return error_response('群组不存在', 404)
        
        # 如果是私有群组，需要是成员才能查看
        if group.type == 'private' and not group.is_member(user_id):
            return error_response('无权查看该群组', 403)
        
        return success_response(
            data=group.to_dict(include_members=True),
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取群组详情失败: {str(e)}', 500)


@group_bp.route('/<int:group_id>/join', methods=['POST'])
@token_required
def join_group(group_id):
    """
    加入群组
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        group_id: 群组ID
    """
    try:
        user_id = request.user_id
        
        # 查询群组
        group = Group.query.get(group_id)
        if not group:
            return error_response('群组不存在', 404)
        
        # 检查是否已经是成员
        if group.is_member(user_id):
            return error_response('您已经是该群组成员', 400)
        
        # 私有群组暂不支持直接加入（需要审批功能）
        if group.type == 'private':
            return error_response('私有群组暂不支持直接加入', 403)
        
        # 创建成员记录
        member = GroupMember(
            group_id=group_id,
            user_id=user_id,
            role='member'
        )
        db.session.add(member)
        db.session.commit()
        
        return success_response(
            data=member.to_dict(),
            message='加入群组成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'加入群组失败: {str(e)}', 500)


@group_bp.route('/<int:group_id>/leave', methods=['DELETE'])
@token_required
def leave_group(group_id):
    """
    退出群组
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        group_id: 群组ID
    """
    try:
        user_id = request.user_id
        
        # 查询群组
        group = Group.query.get(group_id)
        if not group:
            return error_response('群组不存在', 404)
        
        # 检查是否是成员
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if not member:
            return error_response('您不是该群组成员', 400)
        
        # 群主不能直接退出（需要先转让群主）
        if member.role == 'owner':
            return error_response('群主需要先转让群主权限才能退出', 403)
        
        # 删除成员记录
        db.session.delete(member)
        db.session.commit()
        
        return success_response(message='退出群组成功')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'退出群组失败: {str(e)}', 500)


@group_bp.route('/<int:group_id>/members', methods=['GET'])
@token_required
def get_group_members(group_id):
    """
    获取群组成员列表
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        group_id: 群组ID
    """
    try:
        user_id = request.user_id
        
        # 查询群组
        group = Group.query.get(group_id)
        if not group:
            return error_response('群组不存在', 404)
        
        # 检查权限
        if not group.is_member(user_id):
            return error_response('只有群组成员可以查看成员列表', 403)
        
        # 获取成员列表
        members = GroupMember.query.filter_by(group_id=group_id).all()
        member_list = [member.to_dict() for member in members]
        
        return success_response(
            data={'members': member_list, 'count': len(member_list)},
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取成员列表失败: {str(e)}', 500)


@group_bp.route('/<int:group_id>/members/<int:target_user_id>', methods=['DELETE'])
@token_required
def kick_member(group_id, target_user_id):
    """
    踢出成员
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        group_id: 群组ID
        target_user_id: 目标用户ID
    """
    try:
        user_id = request.user_id
        
        # 查询群组
        group = Group.query.get(group_id)
        if not group:
            return error_response('群组不存在', 404)
        
        # 检查权限（只有群主和管理员可以踢人）
        if not group.is_admin(user_id):
            return error_response('只有群主和管理员可以踢出成员', 403)
        
        # 不能踢自己
        if user_id == target_user_id:
            return error_response('不能踢出自己', 400)
        
        # 不能踢群主
        if group.is_owner(target_user_id):
            return error_response('不能踢出群主', 403)
        
        # 查询目标成员
        target_member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=target_user_id
        ).first()
        
        if not target_member:
            return error_response('该用户不是群组成员', 404)
        
        # 删除成员记录
        db.session.delete(target_member)
        db.session.commit()
        
        return success_response(message='成员已被踢出')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'踢出成员失败: {str(e)}', 500)
