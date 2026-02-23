"""
本地存储工具
用于保存和读取Token等信息
"""
import os
from config import Config


class Storage:
    """本地存储类"""
    
    @staticmethod
    def save_token(token: str):
        """
        保存Token到本地
        
        Args:
            token: JWT Token
        """
        Config.ensure_storage_dir()
        
        try:
            with open(Config.TOKEN_FILE, 'w', encoding='utf-8') as f:
                f.write(token)
        except Exception as e:
            print(f'保存Token失败: {str(e)}')
    
    @staticmethod
    def load_token() -> str:
        """
        从本地读取Token
        
        Returns:
            str: JWT Token，如果不存在返回None
        """
        try:
            if os.path.exists(Config.TOKEN_FILE):
                with open(Config.TOKEN_FILE, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except Exception as e:
            print(f'读取Token失败: {str(e)}')
        
        return None
    
    @staticmethod
    def clear_token():
        """删除本地Token"""
        try:
            if os.path.exists(Config.TOKEN_FILE):
                os.remove(Config.TOKEN_FILE)
        except Exception as e:
            print(f'删除Token失败: {str(e)}')
