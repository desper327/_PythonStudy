"""
消息路由
处理消息历史查询等请求
"""
from flask import Blueprint, request
from models import Message, Group
from utils import token_required, success_response, error_response

# 创建蓝图
message_bp = Blueprint('message', __name__)


@message_bp.route('/private/<int:other_user_id>', methods=['GET'])
@token_required
def get_private_messages(other_user_id):
    """
    获取与指定用户的私聊历史
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        other_user_id: 对方用户ID
        
    Query参数:
        page: 页码（默认1）
        per_page: 每页数量（默认50）
    """
    try:
        user_id = request.user_id
        
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # 限制每页数量
        if per_page > 100:
            per_page = 100
        
        # 查询私聊消息（双向）
        from models.user import db
        messages_query = Message.query.filter(
            db.or_(
                db.and_(
                    Message.sender_id == user_id,
                    Message.receiver_id == other_user_id
                ),
                db.and_(
                    Message.sender_id == other_user_id,
                    Message.receiver_id == user_id
                )
            )
        ).order_by(Message.created_at.desc())
        
        # 分页
        pagination = messages_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # 转换为字典列表（反转顺序，最新的在最后）
        message_list = [msg.to_dict() for msg in reversed(pagination.items)]
        
        return success_response(
            data={
                'messages': message_list,
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取消息历史失败: {str(e)}', 500)


@message_bp.route('/group/<int:group_id>', methods=['GET'])
@token_required
def get_group_messages(group_id):
    """
    获取群组聊天历史
    
    Headers:
        Authorization: Bearer <token>
        
    路径参数:
        group_id: 群组ID
        
    Query参数:
        page: 页码（默认1）
        per_page: 每页数量（默认50）
    """
    try:
        user_id = request.user_id
        
        # 查询群组
        group = Group.query.get(group_id)
        if not group:
            return error_response('群组不存在', 404)
        
        # 检查权限
        if not group.is_member(user_id):
            return error_response('只有群组成员可以查看消息历史', 403)
        
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # 限制每页数量
        if per_page > 100:
            per_page = 100
        
        # 查询群组消息
        messages_query = Message.query.filter_by(
            group_id=group_id
        ).order_by(Message.created_at.desc())
        
        # 分页
        pagination = messages_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # 转换为字典列表（反转顺序，最新的在最后）
        message_list = [msg.to_dict() for msg in reversed(pagination.items)]
        
        return success_response(
            data={
                'messages': message_list,
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            message='获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取消息历史失败: {str(e)}', 500)
