"""
主控制器 - 协调模型和视图之间的交互
使用自定义信号和槽机制，手动同步数据和UI
"""
from Qt.QtCore import QObject
from models.data_models import TextData, SignalData
from models.data_center import DataCenter
from views.main_view import MainView

class MainController(QObject):
    """主控制器 - 使用自定义信号槽架构"""

    def __init__(self):
        super().__init__()

        self.view_signal_dict={
            "on_show_text":self.handle_show_text,
        }
        self.model_signal_dict={
        "text_changed":self.on_text_changed_update_ui,
    }

        # 初始化数据仓库
        self.data_center = DataCenter()
        
        # 初始化视图
        self.view = MainView()
        
        # 连接信号和槽
        self.connect_signals()
        
    
    def connect_signals(self):
        """连接视图信号到控制器方法，连接仓库信号到UI更新方法"""
        
        # ========== 视图信号 -> 控制器方法 ==========
        self.view.view_signal.connect(self.handle_view_signal)
        
        # ========== 仓库信号 -> UI更新槽函数 ==========
        self.data_center.model_signal.connect(self.handle_model_signal)
    

    # ========== 处理视图请求的方法 ==========
    def handle_view_signal(self, signal_data: SignalData):
        """
        处理视图信号
        """
        print("[Controller] 收到view信号: ", signal_data.signal_type, signal_data.params)
        if signal_data.signal_type in self.view_signal_dict:
            self.view_signal_dict[signal_data.signal_type](**signal_data.params)
    
    # ========== 响应仓库信号的UI更新槽函数 ==========
    def handle_model_signal(self, signal_data: SignalData):
        """
        槽函数：当仓库发出任务信号后，更新UI
        
        Args:
            signal_data: 信号数据
        """
        print(f"[Controller] 收到model信号: {signal_data.signal_type}, {signal_data.params}")
        
        # 根据信号类型更新UI
        if signal_data.signal_type in self.model_signal_dict:
            self.model_signal_dict[signal_data.signal_type](**signal_data.params)
    
    def handle_show_text(self,text_data: TextData):
        """
        槽函数：处理显示文本按钮点击事件
        """
        print(f"[Controller] handle_show_text: {text_data.text}")
        self.data_center.text = text_data


    def on_text_changed_update_ui(self, new_text: TextData):
        """
        槽函数：当仓库中的文本发生变化时，更新UI
        
        Args:
            new_text: 新的文本数据
        """
        print(f"[Controller] on_text_changed_update_ui: {new_text.text}")
        self.view.show_label.setText(new_text.text)
    
    
    def show(self):
        """显示主窗口"""
        self.view.show()
        print("[Controller] 应用程序已启动")

    def show_error(self, error: str):
        """显示错误信息"""
        print(f"[Controller] 错误: {error}")
        self.view.show_error(error)
