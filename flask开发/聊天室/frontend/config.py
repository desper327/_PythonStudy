"""
前端配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """前端配置类"""
    
    # 服务器配置
    SERVER_HOST = os.getenv('SERVER_HOST', 'http://localhost:5000')
    SOCKET_HOST = os.getenv('SOCKET_HOST', 'http://localhost:5000')
    
    # 应用配置
    APP_NAME = 'Flask聊天室'
    APP_VERSION = '1.0.0'
    
    # UI配置
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 900
    MIN_WINDOW_HEIGHT = 600
    
    # 主题颜色（现代风格）
    PRIMARY_COLOR = '#1890ff'  # 主色调（蓝色）
    SUCCESS_COLOR = '#52c41a'  # 成功（绿色）
    WARNING_COLOR = '#faad14'  # 警告（橙色）
    ERROR_COLOR = '#f5222d'    # 错误（红色）
    
    # 背景色
    BG_COLOR = '#f0f2f5'       # 浅灰背景
    CARD_BG_COLOR = '#ffffff'  # 卡片背景
    
    # 文字颜色
    TEXT_PRIMARY = '#262626'   # 主要文字
    TEXT_SECONDARY = '#8c8c8c' # 次要文字
    TEXT_DISABLED = '#bfbfbf'  # 禁用文字
    
    # 边框
    BORDER_COLOR = '#d9d9d9'   # 边框颜色
    BORDER_RADIUS = '8px'      # 圆角大小
    
    # 消息配置
    MAX_MESSAGE_LENGTH = 10000
    MESSAGE_PAGE_SIZE = 50
    
    # 本地存储
    STORAGE_DIR = os.path.join(os.path.expanduser('~'), '.chatroom')
    TOKEN_FILE = os.path.join(STORAGE_DIR, 'token.txt')
    
    @classmethod
    def ensure_storage_dir(cls):
        """确保存储目录存在"""
        if not os.path.exists(cls.STORAGE_DIR):
            os.makedirs(cls.STORAGE_DIR)
