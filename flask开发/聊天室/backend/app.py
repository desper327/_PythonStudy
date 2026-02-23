"""
Flask应用主入口
初始化Flask应用、数据库、SocketIO等
"""
import os,sys
sys.path.append(r'D:\TD_Depot\Python\Lib\3.11\.venv\Lib\site-packages')
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import config
from models.user import db
from routes import register_blueprints
from sockets import register_socket_events


def create_app(config_name=None):
    """
    创建Flask应用
    
    Args:
        config_name: 配置名称（development/production）
        
    Returns:
        Flask: Flask应用实例
    """
    # 创建Flask应用
    app = Flask(__name__)
    
    # 加载配置
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)  # 允许跨域（前端PySide6需要访问后端API）
    
    # 创建SocketIO实例
    socketio = SocketIO(
        app,
        cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS'],
        async_mode=app.config['SOCKETIO_ASYNC_MODE']
    )
    
    # 注册路由
    register_blueprints(app)
    
    # 注册WebSocket事件
    register_socket_events(socketio)
    
    # 添加测试路由
    @app.route('/')
    def index():
        return {
            'message': 'Flask聊天室后端服务',
            'status': 'running',
            'version': '1.0.0'
        }
    
    @app.route('/health')
    def health():
        """健康检查"""
        return {'status': 'healthy'}
    
    # CLI命令：初始化数据库
    @app.cli.command()
    def init_db():
        """初始化数据库（创建所有表）"""
        with app.app_context():
            db.create_all()
            print('数据库初始化成功！')
    
    # CLI命令：删除所有表
    @app.cli.command()
    def drop_db():
        """删除所有数据库表（危险操作！）"""
        with app.app_context():
            if input('确定要删除所有表吗？(yes/no): ').lower() == 'yes':
                db.drop_all()
                print('所有表已删除！')
            else:
                print('操作已取消。')
    
    # CLI命令：重置数据库
    @app.cli.command()
    def reset_db():
        """重置数据库（删除并重新创建所有表）"""
        with app.app_context():
            if input('确定要重置数据库吗？(yes/no): ').lower() == 'yes':
                db.drop_all()
                db.create_all()
                print('数据库重置成功！')
            else:
                print('操作已取消。')
    
    return app, socketio


if __name__ == '__main__':
    # 创建应用
    app, socketio = create_app()
    
    # 获取配置
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)
    
    print(f"""
    ╔════════════════════════════════════════════════╗
    ║    Flask-PySide6 聊天室后端服务                ║
    ╠════════════════════════════════════════════════╣
    ║  服务地址: http://{host}:{port}              ║
    ║  调试模式: {'开启' if debug else '关闭'}                          ║
    ╚════════════════════════════════════════════════╝
    
    提示：首次运行请先执行以下命令初始化数据库：
    python app.py init-db
    """)
    
    # 运行应用
    socketio.run(app, host=host, port=port, debug=debug)
