"""
网络请求异步处理示例
演示如何在PyQt应用中正确处理网络请求，避免UI阻塞
"""
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QLabel, QComboBox, 
    QProgressBar, QStatusBar, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from utils.async_task_manager import get_task_manager


class NetworkExampleWindow(QMainWindow):
    """网络请求示例窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 获取任务管理器
        self.task_manager = get_task_manager()
        
        # 连接任务管理器信号
        self.connect_task_manager_signals()
        
        # 设置UI
        self.setup_ui()
        
        # 活跃请求计数
        self.active_requests = {}
    
    def connect_task_manager_signals(self):
        """连接任务管理器信号"""
        self.task_manager.task_started.connect(self.on_request_started)
        self.task_manager.task_finished.connect(self.on_request_finished)
        self.task_manager.task_failed.connect(self.on_request_failed)
        self.task_manager.task_progress.connect(self.on_request_progress)
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("网络请求异步处理示例")
        self.setGeometry(200, 200, 800, 600)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 请求计数标签
        self.request_count_label = QLabel("活跃请求: 0")
        self.status_bar.addPermanentWidget(self.request_count_label)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 请求配置面板
        config_panel = self.create_request_config_panel()
        main_layout.addWidget(config_panel)
        
        # 预设请求面板
        preset_panel = self.create_preset_requests_panel()
        main_layout.addWidget(preset_panel)
        
        # 响应显示区域
        response_panel = self.create_response_panel()
        main_layout.addWidget(response_panel)
        
        # 设置初始状态
        self.status_bar.showMessage("就绪 - 可以发送网络请求")
    
    def create_request_config_panel(self) -> QWidget:
        """创建请求配置面板"""
        group_box = QGroupBox("自定义网络请求")
        layout = QVBoxLayout(group_box)
        
        # URL输入
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入请求URL，例如: https://httpbin.org/get")
        self.url_input.setText("https://httpbin.org/get")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # 方法选择
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("方法:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE"])
        method_layout.addWidget(self.method_combo)
        
        # 超时设置
        method_layout.addWidget(QLabel("超时(秒):"))
        self.timeout_input = QLineEdit()
        self.timeout_input.setText("10")
        self.timeout_input.setMaximumWidth(60)
        method_layout.addWidget(self.timeout_input)
        
        method_layout.addStretch()
        layout.addLayout(method_layout)
        
        # 请求数据
        layout.addWidget(QLabel("请求数据 (JSON格式):"))
        self.data_input = QTextEdit()
        self.data_input.setPlaceholderText('{"key": "value"}')
        self.data_input.setMaximumHeight(80)
        layout.addLayout(method_layout)
        layout.addWidget(self.data_input)
        
        # 发送按钮
        self.send_button = QPushButton("发送请求")
        self.send_button.clicked.connect(self.on_send_custom_request)
        layout.addWidget(self.send_button)
        
        return group_box
    
    def create_preset_requests_panel(self) -> QWidget:
        """创建预设请求面板"""
        group_box = QGroupBox("预设网络请求示例")
        layout = QHBoxLayout(group_box)
        
        # 各种示例请求按钮
        self.get_json_button = QPushButton("GET JSON数据")
        self.post_data_button = QPushButton("POST提交数据")
        self.slow_request_button = QPushButton("慢速请求(10秒)")
        self.error_request_button = QPushButton("错误请求(404)")
        self.timeout_request_button = QPushButton("超时请求")
        
        layout.addWidget(self.get_json_button)
        layout.addWidget(self.post_data_button)
        layout.addWidget(self.slow_request_button)
        layout.addWidget(self.error_request_button)
        layout.addWidget(self.timeout_request_button)
        
        # 连接信号
        self.get_json_button.clicked.connect(self.on_get_json_request)
        self.post_data_button.clicked.connect(self.on_post_data_request)
        self.slow_request_button.clicked.connect(self.on_slow_request)
        self.error_request_button.clicked.connect(self.on_error_request)
        self.timeout_request_button.clicked.connect(self.on_timeout_request)
        
        return group_box
    
    def create_response_panel(self) -> QWidget:
        """创建响应显示面板"""
        group_box = QGroupBox("响应结果")
        layout = QVBoxLayout(group_box)
        
        # 响应显示区域
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        self.response_display.setFont(QFont("Consolas", 9))
        layout.addWidget(self.response_display)
        
        # 清空按钮
        clear_button = QPushButton("清空响应")
        clear_button.clicked.connect(self.response_display.clear)
        layout.addWidget(clear_button)
        
        return group_box
    
    # ========== 网络请求处理方法 ==========
    
    def on_send_custom_request(self):
        """发送自定义请求"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "输入错误", "请输入URL！")
            return
        
        method = self.method_combo.currentText()
        
        try:
            timeout = int(self.timeout_input.text())
        except ValueError:
            timeout = 10
        
        # 解析请求数据
        data = None
        data_text = self.data_input.toPlainText().strip()
        if data_text and method in ["POST", "PUT"]:
            try:
                data = json.loads(data_text)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "数据错误", "请求数据不是有效的JSON格式！")
                return
        
        # 发送异步请求
        self.send_network_request(
            url=url,
            method=method,
            data=data,
            timeout=timeout,
            request_name="自定义请求"
        )
    
    def on_get_json_request(self):
        """GET JSON数据请求"""
        self.send_network_request(
            url="https://httpbin.org/json",
            method="GET",
            request_name="GET JSON数据"
        )
    
    def on_post_data_request(self):
        """POST数据请求"""
        data = {
            "name": "PyQt异步请求示例",
            "version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        self.send_network_request(
            url="https://httpbin.org/post",
            method="POST",
            data=data,
            request_name="POST提交数据"
        )
    
    def on_slow_request(self):
        """慢速请求"""
        self.send_network_request(
            url="https://httpbin.org/delay/10",
            method="GET",
            timeout=15,
            request_name="慢速请求(10秒延迟)"
        )
    
    def on_error_request(self):
        """错误请求"""
        self.send_network_request(
            url="https://httpbin.org/status/404",
            method="GET",
            request_name="错误请求(404)"
        )
    
    def on_timeout_request(self):
        """超时请求"""
        self.send_network_request(
            url="https://httpbin.org/delay/10",
            method="GET",
            timeout=3,  # 3秒超时，但服务器需要10秒
            request_name="超时请求(3秒超时)"
        )
    
    def send_network_request(self, url: str, method: str = "GET", 
                           data: dict = None, timeout: int = 10,
                           request_name: str = "网络请求"):
        """
        发送网络请求
        
        Args:
            url: 请求URL
            method: HTTP方法
            data: 请求数据
            timeout: 超时时间
            request_name: 请求名称
        """
        # 生成请求ID
        request_id = self.task_manager.generate_task_id("network")
        
        # 在响应区域显示请求信息
        self.append_response(f"\n{'='*50}")
        self.append_response(f"🚀 开始请求: {request_name}")
        self.append_response(f"📍 URL: {url}")
        self.append_response(f"🔧 方法: {method}")
        if data:
            self.append_response(f"📦 数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        self.append_response(f"⏱️ 超时: {timeout}秒")
        self.append_response(f"🆔 请求ID: {request_id}")
        self.append_response("⏳ 请求中...")
        
        # 发送异步网络请求
        self.task_manager.run_network_request(
            url=url,
            method=method,
            data=data,
            timeout=timeout,
            task_id=request_id,
            on_finished=lambda result: self.on_network_success(request_id, request_name, result),
            on_error=lambda error: self.on_network_error(request_id, request_name, error),
            on_progress=lambda progress, msg: self.on_network_progress(request_id, progress, msg)
        )
    
    def on_network_success(self, request_id: str, request_name: str, result: dict):
        """网络请求成功回调"""
        status_code = result.get('status_code', 0)
        data = result.get('data', {})
        headers = result.get('headers', {})
        
        self.append_response(f"✅ 请求成功: {request_name}")
        self.append_response(f"📊 状态码: {status_code}")
        self.append_response(f"📋 响应头: {json.dumps(dict(headers), ensure_ascii=False, indent=2)}")
        self.append_response(f"📄 响应数据:")
        
        # 格式化响应数据
        if isinstance(data, dict) or isinstance(data, list):
            formatted_data = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            formatted_data = str(data)
        
        self.append_response(formatted_data)
        self.append_response(f"🎉 请求 {request_id} 完成！")
    
    def on_network_error(self, request_id: str, request_name: str, error: str):
        """网络请求失败回调"""
        self.append_response(f"❌ 请求失败: {request_name}")
        self.append_response(f"🚫 错误信息: {error}")
        self.append_response(f"💥 请求 {request_id} 失败！")
    
    def on_network_progress(self, request_id: str, progress: int, message: str):
        """网络请求进度回调"""
        self.append_response(f"📈 进度更新 ({progress}%): {message}")
    
    # ========== 任务管理器信号处理 ==========
    
    def on_request_started(self, task_id: str):
        """请求开始处理"""
        if task_id.startswith("network"):
            self.active_requests[task_id] = True
            self.update_request_status()
            
            # 显示进度条
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            self.status_bar.showMessage(f"请求 {task_id} 开始...")
    
    def on_request_finished(self, task_id: str, result):
        """请求完成处理"""
        if task_id in self.active_requests:
            del self.active_requests[task_id]
            self.update_request_status()
            
            # 如果没有活跃请求，隐藏进度条
            if not self.active_requests:
                self.progress_bar.setVisible(False)
            
            self.status_bar.showMessage(f"请求 {task_id} 完成", 3000)
    
    def on_request_failed(self, task_id: str, error: str):
        """请求失败处理"""
        if task_id in self.active_requests:
            del self.active_requests[task_id]
            self.update_request_status()
            
            # 如果没有活跃请求，隐藏进度条
            if not self.active_requests:
                self.progress_bar.setVisible(False)
            
            self.status_bar.showMessage(f"请求 {task_id} 失败: {error}", 5000)
    
    def on_request_progress(self, task_id: str, progress: int, message: str):
        """请求进度处理"""
        if progress >= 0:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(progress)
        
        self.status_bar.showMessage(f"{task_id}: {message}")
    
    def update_request_status(self):
        """更新请求状态显示"""
        active_count = len(self.active_requests)
        self.request_count_label.setText(f"活跃请求: {active_count}")
    
    def append_response(self, text: str):
        """在响应区域追加文本"""
        self.response_display.append(text)
        
        # 自动滚动到底部
        cursor = self.response_display.textCursor()
        cursor.movePosition(cursor.End)
        self.response_display.setTextCursor(cursor)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("网络请求异步处理示例")
    app.setApplicationVersion("1.0")
    
    print("=" * 60)
    print("网络请求异步处理示例")
    print("=" * 60)
    print("功能特点:")
    print("1. 使用QThreadPool处理网络请求，避免UI阻塞")
    print("2. 支持GET、POST、PUT、DELETE等HTTP方法")
    print("3. 实时显示请求进度和状态")
    print("4. 完整的错误处理和超时控制")
    print("5. 响应数据的格式化显示")
    print("=" * 60)
    
    try:
        # 创建主窗口
        window = NetworkExampleWindow()
        window.show()
        
        print("网络请求示例启动成功！")
        print("请在界面中测试各种网络请求功能")
        print("=" * 60)
        
        # 启动事件循环
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
