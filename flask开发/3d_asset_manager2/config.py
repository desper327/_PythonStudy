import os

class Config:
    # MySQL 数据库配置
    DB_HOST = 'localhost'#"192.168.112.10:29292"#'  # MySQL 主机地址
    DB_USER = 'zy'  #'root'       # MySQL 用户名
    DB_PASSWORD = 'zhangyang'#'123456'  # MySQL 密码
    DB_NAME = '3DAssetManager_db'  # 数据库名称

    # Flask 配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUPER_ADMIN = 'superadmin'  # 超级管理员用户名

    # 上传文件配置
    UPLOAD_THUMBNAILS_FOLDER = os.path.join('static', 'uploads', 'thumbnails')  # 图片存储路径
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的文件类型
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大文件大小（16MB）

    # 文件路径
    DEPOT_FOLDER =  r'D:\All_depot\3DAssetsDepot' # 资产文件存储路径
