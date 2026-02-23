"""
路由模块
注册所有蓝图
"""
from flask import Flask
from .auth import auth_bp
from .user import user_bp
from .group import group_bp
from .message import message_bp


def register_blueprints(app: Flask):
    """
    注册所有蓝图
    
    Args:
        app: Flask应用实例
    """
    # 注册认证路由
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # 注册用户路由
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    # 注册群组路由
    app.register_blueprint(group_bp, url_prefix='/api/groups')
    
    # 注册消息路由
    app.register_blueprint(message_bp, url_prefix='/api/messages')
