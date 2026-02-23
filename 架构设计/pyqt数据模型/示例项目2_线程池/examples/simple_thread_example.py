"""
简单QThread示例 - 演示基本的工作线程使用方法
展示如何使用QThread处理耗时任务，避免UI阻塞
"""
import sys
import time
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QProgressBar, QGroupBox, 
    QLineEdit, QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont


class SimpleWorkerThread(QThread):
    """
    简单工作线程 - 演示基本的QThread使用
    """
    
    # 定义信号
    started = pyqtSignal()  # 任务开始
    progress = pyqtSignal(int, str)  # 进度更新
    finished = pyqtSignal(dict)  # 任务完成
    error = pyqtSignal(str)  # 任务错误
    
    def __init__(self, task_name: str, duration: int = 5):
        """
        初始化工作线程
        
        Args:
            task_name: 任务名称
            duration: 任务持续时间(秒)
        """
        super().__init__()
        self.task_name = task_name
        self.duration = duration
        self._is_running = False
    
    def run(self):
        """
        线程执行方法 - 在工作线程中运行
        这个方法会在新的线程中执行，不会阻塞主线程
        """
        try:
            self._is_running = True
            
            # 发射开始信号
            self.started.emit()
            
            print(f"[Worker Thread] 开始执行任务: {self.task_name}")
            
            # 模拟耗时任务，分步骤执行并报告进度
            total_steps = self.duration * 10  # 每秒10步
            
            for step in range(total_steps):
                if not self._is_running:  # 检查是否被中断
                    print(f"[Worker Thread] 任务被中断: {self.task_name}")
                    return
                
                # 模拟工作
                time.sleep(0.1)  # 每步0.1秒
                
                # 计算进度
                progress = int((step + 1) / total_steps * 100)
                elapsed_time = (step + 1) * 0.1
                
                # 发射进度信号
                self.progress.emit(
                    progress, 
                    f"执行中... {progress}% (已用时: {elapsed_time:.1f}秒)"
                )
            
            # 任务完成，准备结果
            result = {
                "task_name": self.task_name,
                "duration": self.duration,
                "actual_time": total_steps * 0.1,
                "status": "completed",
                "result_data": f"任务 '{self.task_name}' 执行完成",
                "steps_completed": total_steps
            }
            
            print(f"[Worker Thread] 任务完成: {self.task_name}")
            
            # 发射完成信号
            self.finished.emit(result)
            
        except Exception as e:
            print(f"[Worker Thread] 任务出错: {self.task_name} - {e}")
            # 发射错误信号
            self.error.emit(str(e))
        finally:
            self._is_running = False
    
    def stop_task(self):
        """停止任务执行"""
        print(f"[Worker Thread] 收到停止请求: {self.task_name}")
        self._is_running = False
        self.quit()  # 退出线程事件循环
        self.wait()  # 等待线程结束


class ComputationWorkerThread(QThread):
    """
    计算工作线程 - 演示CPU密集型任务
    """
    
    started = pyqtSignal()
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, iterations: int = 1000000):
        super().__init__()
        self.iterations = iterations
        self._is_running = False
    
    def run(self):
        """执行CPU密集型计算"""
        try:
            self._is_running = True
            self.started.emit()
            
            print(f"[Computation Thread] 开始计算，迭代次数: {self.iterations}")
            
            result = 0
            report_interval = max(1, self.iterations // 100)  # 每1%报告一次进度
            
            for i in range(self.iterations):
                if not self._is_running:
                    return
                
                # 执行计算
                result += i * i
                
                # 报告进度
                if i % report_interval == 0:
                    progress = int((i + 1) / self.iterations * 100)
                    self.progress.emit(progress, f"计算中... {progress}% ({i+1}/{self.iterations})")
            
            # 计算完成
            computation_result = {
                "iterations": self.iterations,
                "final_result": result,
                "status": "completed"
            }
            
            print(f"[Computation Thread] 计算完成，结果: {result}")
            self.finished.emit(computation_result)
            
        except Exception as e:
            print(f"[Computation Thread] 计算出错: {e}")
            self.error.emit(str(e))
        finally:
            self._is_running = False
    
    def stop_task(self):
        """停止计算"""
        self._is_running = False
        self.quit()
        self.wait()


class SimpleThreadExampleWindow(QMainWindow):
    """简单线程示例窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 当前活跃的线程
        self.current_thread = None
        
        # 设置UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("简单QThread示例 - 基础工作线程")
        self.setGeometry(200, 200, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("简单QThread工作线程示例")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # 控制面板
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # 进度显示
        progress_panel = self.create_progress_panel()
        main_layout.addWidget(progress_panel)
        
        # 结果显示
        result_panel = self.create_result_panel()
        main_layout.addWidget(result_panel)
        
        # 说明面板
        info_panel = self.create_info_panel()
        main_layout.addWidget(info_panel)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        group_box = QGroupBox("任务控制")
        layout = QVBoxLayout(group_box)
        
        # 任务配置
        config_layout = QHBoxLayout()
        
        config_layout.addWidget(QLabel("任务名称:"))
        self.task_name_input = QLineEdit()
        self.task_name_input.setText("示例任务")
        config_layout.addWidget(self.task_name_input)
        
        config_layout.addWidget(QLabel("持续时间(秒):"))
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 30)
        self.duration_spinbox.setValue(5)
        config_layout.addWidget(self.duration_spinbox)
        
        config_layout.addStretch()
        layout.addLayout(config_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.start_simple_button = QPushButton("启动简单任务")
        self.start_simple_button.clicked.connect(self.start_simple_task)
        button_layout.addWidget(self.start_simple_button)
        
        self.start_computation_button = QPushButton("启动计算任务")
        self.start_computation_button.clicked.connect(self.start_computation_task)
        button_layout.addWidget(self.start_computation_button)
        
        self.stop_button = QPushButton("停止任务")
        self.stop_button.clicked.connect(self.stop_current_task)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return group_box
    
    def create_progress_panel(self) -> QWidget:
        """创建进度面板"""
        group_box = QGroupBox("任务进度")
        layout = QVBoxLayout(group_box)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪 - 可以启动任务")
        layout.addWidget(self.status_label)
        
        return group_box
    
    def create_result_panel(self) -> QWidget:
        """创建结果面板"""
        group_box = QGroupBox("执行结果")
        layout = QVBoxLayout(group_box)
        
        # 结果显示区域
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont("Consolas", 9))
        layout.addWidget(self.result_display)
        
        # 清空按钮
        clear_button = QPushButton("清空结果")
        clear_button.clicked.connect(self.result_display.clear)
        layout.addWidget(clear_button)
        
        return group_box
    
    def create_info_panel(self) -> QWidget:
        """创建说明面板"""
        group_box = QGroupBox("QThread使用说明")
        layout = QVBoxLayout(group_box)
        
        info_text = """
🧵 QThread基本概念:
• QThread是Qt提供的线程类，用于在后台执行耗时任务
• 重写run()方法来定义线程要执行的工作
• 使用信号槽机制与主线程通信，确保线程安全

🔄 执行流程:
1. 创建QThread子类，重写run()方法
2. 定义信号来报告进度和结果
3. 在主线程中创建线程实例
4. 连接信号到槽函数
5. 调用start()启动线程
6. 线程执行完毕后自动销毁

⚠️ 注意事项:
• 不要在工作线程中直接操作UI组件
• 使用信号槽进行线程间通信
• 及时清理线程资源，避免内存泄漏
• 可以通过标志位控制线程的停止
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignTop)
        layout.addWidget(info_label)
        
        return group_box
    
    # ========== 任务控制方法 ==========
    
    def start_simple_task(self):
        """启动简单任务"""
        if self.current_thread and self.current_thread.isRunning():
            self.append_result("❌ 已有任务在运行中，请先停止当前任务")
            return
        
        task_name = self.task_name_input.text().strip()
        duration = self.duration_spinbox.value()
        
        if not task_name:
            task_name = "默认任务"
        
        # 创建工作线程
        self.current_thread = SimpleWorkerThread(task_name, duration)
        
        # 连接信号
        self.current_thread.started.connect(self.on_task_started)
        self.current_thread.progress.connect(self.on_task_progress)
        self.current_thread.finished.connect(self.on_task_finished)
        self.current_thread.error.connect(self.on_task_error)
        
        # 启动线程
        self.current_thread.start()
        
        self.append_result(f"🚀 启动简单任务: {task_name} (预计用时: {duration}秒)")
        
        # 更新按钮状态
        self.start_simple_button.setEnabled(False)
        self.start_computation_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    
    def start_computation_task(self):
        """启动计算任务"""
        if self.current_thread and self.current_thread.isRunning():
            self.append_result("❌ 已有任务在运行中，请先停止当前任务")
            return
        
        iterations = 5000000  # 500万次迭代
        
        # 创建计算线程
        self.current_thread = ComputationWorkerThread(iterations)
        
        # 连接信号
        self.current_thread.started.connect(self.on_task_started)
        self.current_thread.progress.connect(self.on_task_progress)
        self.current_thread.finished.connect(self.on_computation_finished)
        self.current_thread.error.connect(self.on_task_error)
        
        # 启动线程
        self.current_thread.start()
        
        self.append_result(f"🚀 启动计算任务: {iterations:,} 次迭代")
        
        # 更新按钮状态
        self.start_simple_button.setEnabled(False)
        self.start_computation_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    
    def stop_current_task(self):
        """停止当前任务"""
        if self.current_thread and self.current_thread.isRunning():
            self.append_result("🛑 正在停止任务...")
            self.current_thread.stop_task()
            self.reset_ui_state()
        else:
            self.append_result("ℹ️ 没有正在运行的任务")
    
    # ========== 信号处理方法 ==========
    
    def on_task_started(self):
        """任务开始处理"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("🔄 任务执行中...")
        
        self.append_result("⏳ 任务开始执行...")
    
    def on_task_progress(self, progress: int, message: str):
        """任务进度处理"""
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"🔄 {message}")
        
        # 每25%输出一次进度
        if progress % 25 == 0:
            self.append_result(f"📈 进度更新: {message}")
    
    def on_task_finished(self, result: dict):
        """简单任务完成处理"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("✅ 任务完成")
        
        self.append_result("✅ 简单任务执行完成!")
        self.append_result(f"📊 任务结果:")
        self.append_result(json.dumps(result, ensure_ascii=False, indent=2))
        self.append_result("=" * 50)
        
        self.reset_ui_state()
    
    def on_computation_finished(self, result: dict):
        """计算任务完成处理"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("✅ 计算完成")
        
        iterations = result.get('iterations', 0)
        final_result = result.get('final_result', 0)
        
        self.append_result("✅ 计算任务执行完成!")
        self.append_result(f"📊 计算结果:")
        self.append_result(f"   迭代次数: {iterations:,}")
        self.append_result(f"   最终结果: {final_result:,}")
        self.append_result("=" * 50)
        
        self.reset_ui_state()
    
    def on_task_error(self, error: str):
        """任务错误处理"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("❌ 任务失败")
        
        self.append_result(f"❌ 任务执行失败: {error}")
        self.append_result("=" * 50)
        
        self.reset_ui_state()
    
    def reset_ui_state(self):
        """重置UI状态"""
        self.start_simple_button.setEnabled(True)
        self.start_computation_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # 清理线程引用
        if self.current_thread:
            self.current_thread = None
    
    def append_result(self, text: str):
        """在结果区域追加文本"""
        self.result_display.append(text)
        
        # 自动滚动到底部
        cursor = self.result_display.textCursor()
        cursor.movePosition(cursor.End)
        self.result_display.setTextCursor(cursor)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 确保线程正确停止
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.stop_task()
        
        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    app.setApplicationName("简单QThread示例")
    app.setApplicationVersion("1.0")
    
    print("=" * 60)
    print("简单QThread工作线程示例")
    print("=" * 60)
    print("功能特点:")
    print("1. 演示基本的QThread使用方法")
    print("2. 展示如何处理耗时任务而不阻塞UI")
    print("3. 实时进度反馈和任务控制")
    print("4. 线程安全的信号槽通信")
    print("5. 正确的线程资源管理")
    print("=" * 60)
    
    try:
        window = SimpleThreadExampleWindow()
        window.show()
        
        print("简单线程示例启动成功！")
        print("请在界面中测试线程功能")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
