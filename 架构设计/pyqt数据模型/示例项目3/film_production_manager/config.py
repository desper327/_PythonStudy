"""
配置文件
包含应用程序的各种配置选项
"""
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """应用程序配置类"""
    
    # 应用程序基本信息
    APP_NAME = "三维影视制作管理系统"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Film Production Studio"
    
    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent
    
    # 资源目录
    RESOURCES_DIR = PROJECT_ROOT / "resources"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FILE = PROJECT_ROOT / "logs" / "app.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # API配置
    API_BASE_URL = "http://localhost:8000/api"
    API_TIMEOUT = 30  # 秒
    API_RETRY_COUNT = 3
    API_RETRY_DELAY = 1  # 秒
    
    # 数据库配置（如果使用本地数据库）
    DATABASE_URL = "sqlite:///film_production.db"
    DATABASE_POOL_SIZE = 5
    DATABASE_POOL_RECYCLE = 3600
    
    # UI配置
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 800
    WINDOW_DEFAULT_WIDTH = 1400
    WINDOW_DEFAULT_HEIGHT = 900
    
    # 主题配置
    THEME = "default"  # default, dark, light
    
    # 缓存配置
    CACHE_ENABLED = True
    CACHE_TTL = 300  # 5分钟
    CACHE_MAX_SIZE = 100  # 最大缓存项数
    
    # 文件处理配置
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    SUPPORTED_FILE_TYPES = [
        ".ma", ".mb",  # Maya文件
        ".max",        # 3ds Max文件
        ".blend",      # Blender文件
        ".c4d",        # Cinema 4D文件
        ".fbx", ".obj", ".dae",  # 通用3D格式
        ".jpg", ".jpeg", ".png", ".tga", ".exr", ".hdr",  # 图像格式
        ".mov", ".mp4", ".avi", ".mkv",  # 视频格式
    ]
    
    # 线程配置
    MAX_WORKER_THREADS = 4
    THREAD_TIMEOUT = 60  # 秒
    
    # 报告配置
    REPORT_OUTPUT_DIR = PROJECT_ROOT / "reports"
    REPORT_TEMPLATE_DIR = RESOURCES_DIR / "templates"
    
    # 导入导出配置
    EXPORT_FORMATS = ["xlsx", "csv", "json", "xml"]
    IMPORT_FORMATS = ["xlsx", "csv", "json"]
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """获取配置字典"""
        config = {}
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and not callable(getattr(cls, attr_name)):
                config[attr_name] = getattr(cls, attr_name)
        return config
    
    @classmethod
    def create_directories(cls):
        """创建必要的目录"""
        directories = [
            cls.RESOURCES_DIR,
            cls.LOG_FILE.parent,
            cls.REPORT_OUTPUT_DIR,
            cls.REPORT_TEMPLATE_DIR,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def load_from_env(cls):
        """从环境变量加载配置"""
        # API配置
        if os.getenv("API_BASE_URL"):
            cls.API_BASE_URL = os.getenv("API_BASE_URL")
        
        if os.getenv("API_TIMEOUT"):
            try:
                cls.API_TIMEOUT = int(os.getenv("API_TIMEOUT"))
            except ValueError:
                pass
        
        # 数据库配置
        if os.getenv("DATABASE_URL"):
            cls.DATABASE_URL = os.getenv("DATABASE_URL")
        
        # 日志配置
        if os.getenv("LOG_LEVEL"):
            cls.LOG_LEVEL = os.getenv("LOG_LEVEL").upper()
        
        # 主题配置
        if os.getenv("THEME"):
            cls.THEME = os.getenv("THEME")


class DevelopmentConfig(Config):
    """开发环境配置"""
    
    LOG_LEVEL = "DEBUG"
    API_BASE_URL = "http://localhost:8000/api"
    CACHE_ENABLED = False
    
    # 开发环境特有配置
    DEBUG = True
    MOCK_DATA = True  # 使用模拟数据


class ProductionConfig(Config):
    """生产环境配置"""
    
    LOG_LEVEL = "WARNING"
    API_BASE_URL = "https://api.filmproduction.com/v1"
    
    # 生产环境特有配置
    DEBUG = False
    MOCK_DATA = False
    
    # 安全配置
    SSL_VERIFY = True
    API_KEY_REQUIRED = True


class TestingConfig(Config):
    """测试环境配置"""
    
    LOG_LEVEL = "DEBUG"
    API_BASE_URL = "http://test-api.filmproduction.com/api"
    DATABASE_URL = "sqlite:///:memory:"
    
    # 测试环境特有配置
    TESTING = True
    MOCK_DATA = True
    CACHE_ENABLED = False


# 根据环境变量选择配置
def get_config() -> Config:
    """根据环境变量获取配置类"""
    env = os.getenv("FLASK_ENV", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    
    # 从环境变量加载配置
    config_class.load_from_env()
    
    # 创建必要的目录
    config_class.create_directories()
    
    return config_class


# 默认配置实例
config = get_config()