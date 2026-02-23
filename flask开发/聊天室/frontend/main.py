"""
前端主程序入口
"""
import sys
sys.path.append(r'D:\TD_Depot\Python\Lib\3.11\.venv\Lib\site-packages')


from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from config import Config
from ui import LoginWindow, MainWindow
from utils import get_stylesheet, Storage


class ChatApp:
    """聊天应用类"""
    
    def __init__(self):
        """初始化应用"""
        # 创建Qt应用
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(Config.APP_NAME)
        self.app.setApplicationVersion(Config.APP_VERSION)
        
        # 设置全局样式
        self.app.setStyleSheet(get_stylesheet())
        
        # 主窗口
        self.main_window = None
        
        # 检查是否有保存的Token
        self.check_auto_login()
    
    def check_auto_login(self):
        """检查是否可以自动登录"""
        token = Storage.load_token()
        
        if token:
            # 尝试自动登录
            from network import APIClient
            api_client = APIClient()
            api_client.set_token(token)
            
            response = api_client.get_current_user()
            
            if response['code'] == 200:
                # Token有效，直接进入主窗口
                user_info = response['data']
                self.show_main_window(token, user_info)
                return
        
        # Token无效或不存在，显示登录窗口
        self.show_login_window()
    
    def show_login_window(self):
        """显示登录窗口"""
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self, token: str, user_info: dict):
        """
        登录成功回调
        
        Args:
            token: JWT Token
            user_info: 用户信息
        """
        self.show_main_window(token, user_info)
    
    def show_main_window(self, token: str, user_info: dict):
        """
        显示主窗口
        
        Args:
            token: JWT Token
            user_info: 用户信息
        """
        self.main_window = MainWindow(token, user_info)
        self.main_window.show()
    
    def run(self):
        """运行应用"""
        return self.app.exec()


def main():
    """主函数"""
    print(f"""
    ╔════════════════════════════════════════════════╗
    ║         {Config.APP_NAME} 客户端                   ║
    ╠════════════════════════════════════════════════╣
    ║  版本: {Config.APP_VERSION}                              ║
    ║  服务器: {Config.SERVER_HOST}         ║
    ╚════════════════════════════════════════════════╝
    """)
    
    # 创建并运行应用
    app = ChatApp()
    sys.exit(app.run())


if __name__ == '__main__':
    main()
