"""
统一响应格式工具函数
"""
from flask import jsonify


def success_response(data=None, message='操作成功', code=200):
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 状态码
        
    Returns:
        Response: Flask响应对象
    """
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code


def error_response(message='操作失败', code=400, data=None):
    """
    错误响应
    
    Args:
        message: 错误消息
        code: 状态码
        data: 额外数据（可选）
        
    Returns:
        Response: Flask响应对象
    """
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code
