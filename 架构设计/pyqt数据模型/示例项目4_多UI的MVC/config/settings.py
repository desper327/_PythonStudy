"""
应用程序配置文件
包含数据库连接、应用设置等配置信息
"""
import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field
from beartype import beartype


class DatabaseConfig(BaseSettings):
    """
    数据库配置类
    """
    
    # MySQL数据库配置
    host: str = Field(default="localhost", description="数据库主机地址")
    port: int = Field(default=3306, description="数据库端口")
    username: str = Field(default="root", description="数据库用户名")
    password: str = Field(default="", description="数据库密码")
    database: str = Field(default="mvc_framework", description="数据库名称")
    charset: str = Field(default="utf8mb4", description="字符集")
    
    # 连接池配置
    pool_size: int = Field(default=10, description="连接池大小")
    max_overflow: int = Field(default=20, description="连接池最大溢出")
    pool_timeout: int = Field(default=30, description="连接池超时时间")
    pool_recycle: int = Field(default=3600, description="连接回收时间")
    
    # SSL配置
    use_ssl: bool = Field(default=False, description="是否使用SSL")
    ssl_ca: Optional[str] = Field(default=None, description="SSL CA文件路径")
    ssl_cert: Optional[str] = Field(default=None, description="SSL证书文件路径")
    ssl_key: Optional[str] = Field(default=None, description="SSL密钥文件路径")
    
    class Config:
        env_prefix = "DB_"  # 环境变量前缀
        case_sensitive = False
    
    @beartype
    def get_sync_url(self) -> str:
        """
        获取同步数据库连接URL
        
        Returns:
            str: 数据库连接URL
        """
        return (
            f"mysql+pymysql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}?charset={self.charset}"
        )
    
    @beartype
    def get_async_url(self) -> str:
        """
        获取异步数据库连接URL
        
        Returns:
            str: 异步数据库连接URL
        """
        return (
            f"mysql+aiomysql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}?charset={self.charset}"
        )


class AppConfig(BaseSettings):
    """
    应用程序配置类
    """
    
    # 应用基本信息
    app_name: str = Field(default="MVC Framework", description="应用程序名称")
    app_version: str = Field(default="1.0.0", description="应用程序版本")
    debug: bool = Field(default=False, description="是否为调试模式")
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: str = Field(default="logs/app.log", description="日志文件路径")
    log_max_size: int = Field(default=10, description="日志文件最大大小(MB)")
    log_backup_count: int = Field(default=5, description="日志文件备份数量")
    
    # 任务配置
    max_async_tasks: int = Field(default=10, description="最大异步任务数")
    max_thread_tasks: int = Field(default=4, description="最大线程任务数")
    task_timeout: int = Field(default=300, description="任务超时时间(秒)")
    
    # API配置
    api_base_url: str = Field(default="https://jsonplaceholder.typicode.com", description="API基础URL")
    api_timeout: int = Field(default=30, description="API请求超时时间(秒)")
    api_retry_count: int = Field(default=3, description="API请求重试次数")
    
    # UI配置
    window_width: int = Field(default=1200, description="窗口宽度")
    window_height: int = Field(default=800, description="窗口高度")
    theme: str = Field(default="default", description="UI主题")
    
    class Config:
        env_prefix = "APP_"  # 环境变量前缀
        case_sensitive = False


class Settings:
    """
    全局设置管理器
    """
    
    def __init__(self):
        """
        初始化设置管理器
        """
        self._db_config: Optional[DatabaseConfig] = None
        self._app_config: Optional[AppConfig] = None
        self._load_from_env()
    
    @beartype
    def _load_from_env(self) -> None:
        """
        从环境变量加载配置
        """
        # 尝试从.env文件加载环境变量
        try:
            from dotenv import load_dotenv
            env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
            if os.path.exists(env_path):
                load_dotenv(env_path)
        except ImportError:
            pass  # 如果没有安装python-dotenv，跳过
    
    @property
    def database(self) -> DatabaseConfig:
        """
        获取数据库配置
        
        Returns:
            DatabaseConfig: 数据库配置对象
        """
        if self._db_config is None:
            self._db_config = DatabaseConfig()
        return self._db_config
    
    @property
    def app(self) -> AppConfig:
        """
        获取应用配置
        
        Returns:
            AppConfig: 应用配置对象
        """
        if self._app_config is None:
            self._app_config = AppConfig()
        return self._app_config
    
    @beartype
    def update_database_config(self, **kwargs) -> None:
        """
        更新数据库配置
        
        Args:
            **kwargs: 配置参数
        """
        if self._db_config is None:
            self._db_config = DatabaseConfig()
        
        for key, value in kwargs.items():
            if hasattr(self._db_config, key):
                setattr(self._db_config, key, value)
    
    @beartype
    def update_app_config(self, **kwargs) -> None:
        """
        更新应用配置
        
        Args:
            **kwargs: 配置参数
        """
        if self._app_config is None:
            self._app_config = AppConfig()
        
        for key, value in kwargs.items():
            if hasattr(self._app_config, key):
                setattr(self._app_config, key, value)


# 全局设置实例
settings = Settings()
