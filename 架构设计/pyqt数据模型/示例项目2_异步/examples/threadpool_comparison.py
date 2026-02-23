"""
Qt线程池 vs Python线程池对比示例
演示两种线程池方案的使用方法和适用场景
"""
import sys
import time
import json
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QProgressBar, QGroupBox, QTabWidget
)
from PyQt5.QtCore import Qt, QTimer, QThreadPool, QRunnable, QObject, pyqtSignal
from PyQt5.QtGui import QFont


# ========== Qt线程池实现 ==========

class QtTaskSignals(QObject):
    """Qt任务信号"""
    started = pyqtSignal()
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)


class QtTask(QRunnable):
    """Qt线程池任务"""
    
    def __init__(self, task_name, duration=3):
        super().__init__()
        self.task_name = task_name
        self.duration = duration
        self.signals = QtTaskSignals()
        self.setAutoDelete(True)
    
    def run(self):
        """在工作线程中执行"""
        try:
            self.signals.started.emit()
            
            # 模拟耗时操作，带进度反馈
            for i in range(self.duration * 10):
                time.sleep(0.1)
                progress = int((i + 1) / (self.duration * 10) * 100)
                self.signals.progress.emit(progress, f"处理中... {progress}%")
            
            # 模拟返回结果
            result = {
                "task_name": self.task_name,
                "duration": self.duration,
                "result": f"Qt任务 '{self.task_name}' 完成",
                "data": list(range(10))
            }
            
            self.signals.finished.emit(result)
            
        except Exception as e:
            self.signals.error.emit(str(e))


# ========== Python线程池实现 ==========

def python_task_function(task_name, duration=3):
    """Python线程池任务函数"""
    # 模拟耗时操作 (无法直接提供进度反馈)
    time.sleep(duration)
    
    # 返回结果
    return {
        "task_name": task_name,
        "duration": duration,
        "result": f"Python任务 '{task_name}' 完成",
        "data": list(range(10))
    }


# ========== 对比演示窗口 ==========

class ThreadPoolComparisonWindow(QMainWindow):
    """线程池对比演示窗口"""
    
    def __init__(self):
        super().__init__()
        
        # Qt线程池
        self.qt_pool = QThreadPool.globalInstance()
        
        # Python线程池
        self.py_executor = ThreadPoolExecutor(max_workers=4)
        
        # 活跃任务跟踪
        self.active_qt_tasks = 0
        self.active_py_tasks = 0
        self.py_futures = []  # 跟踪Python futures
        
        # 设置UI
        self.setup_ui()
        
        # 启动结果检查定时器
        self.result_timer = QTimer()
        self.result_timer.timeout.connect(self.check_python_results)
        self.result_timer.start(100)  # 每100ms检查一次
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("Qt线程池 vs Python线程池对比")
        self.setGeometry(200, 200, 1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Qt线程池选项卡
        qt_tab = self.create_qt_tab()
        tab_widget.addTab(qt_tab, "Qt线程池 (QThreadPool)")
        
        # Python线程池选项卡
        py_tab = self.create_python_tab()
        tab_widget.addTab(py_tab, "Python线程池 (ThreadPoolExecutor)")
        
        # 对比总结选项卡
        comparison_tab = self.create_comparison_tab()
        tab_widget.addTab(comparison_tab, "对比总结")
    
    def create_qt_tab(self) -> QWidget:
        """创建Qt线程池演示选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("Qt线程池 (QThreadPool + QRunnable)")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 控制面板
        control_group = QGroupBox("控制面板")
        control_layout = QHBoxLayout(control_group)
        
        self.qt_start_button = QPushButton("启动Qt任务")
        self.qt_start_button.clicked.connect(self.start_qt_task)
        control_layout.addWidget(self.qt_start_button)
        
        self.qt_status_label = QLabel("活跃任务: 0")
        control_layout.addWidget(self.qt_status_label)
        
        control_layout.addStretch()
        layout.addWidget(control_group)
        
        # 进度条
        self.qt_progress_bar = QProgressBar()
        self.qt_progress_bar.setVisible(False)
        layout.addWidget(self.qt_progress_bar)
        
        # 结果显示
        result_group = QGroupBox("执行结果")
        result_layout = QVBoxLayout(result_group)
        
        self.qt_result_display = QTextEdit()
        self.qt_result_display.setReadOnly(True)
        self.qt_result_display.setFont(QFont("Consolas", 9))
        result_layout.addWidget(self.qt_result_display)
        
        layout.addWidget(result_group)
        
        # 优缺点说明
        pros_cons_group = QGroupBox("Qt线程池特点")
        pros_cons_layout = QVBoxLayout(pros_cons_group)
        
        pros_cons_text = """
✅ 优点:
• 与Qt完美集成，线程安全的信号槽
• 实时进度反馈，用户体验好
• 自动管理线程生命周期
• 直接更新UI，无需额外处理

❌ 缺点:
• 代码相对复杂，需要定义信号类
• 任务取消机制较复杂
• 只能在Qt应用中使用

🎯 适用场景:
• 需要UI交互的任务
• 需要实时进度反馈
• 复杂的状态管理
• PyQt/PySide应用的首选
        """
        
        pros_cons_label = QLabel(pros_cons_text)
        pros_cons_label.setWordWrap(True)
        pros_cons_layout.addWidget(pros_cons_label)
        
        layout.addWidget(pros_cons_group)
        
        return widget
    
    def create_python_tab(self) -> QWidget:
        """创建Python线程池演示选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("Python线程池 (ThreadPoolExecutor)")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 控制面板
        control_group = QGroupBox("控制面板")
        control_layout = QHBoxLayout(control_group)
        
        self.py_start_button = QPushButton("启动Python任务")
        self.py_start_button.clicked.connect(self.start_python_task)
        control_layout.addWidget(self.py_start_button)
        
        self.py_batch_button = QPushButton("批量处理任务")
        self.py_batch_button.clicked.connect(self.start_batch_tasks)
        control_layout.addWidget(self.py_batch_button)
        
        self.py_status_label = QLabel("活跃任务: 0")
        control_layout.addWidget(self.py_status_label)
        
        control_layout.addStretch()
        layout.addWidget(control_group)
        
        # 结果显示
        result_group = QGroupBox("执行结果")
        result_layout = QVBoxLayout(result_group)
        
        self.py_result_display = QTextEdit()
        self.py_result_display.setReadOnly(True)
        self.py_result_display.setFont(QFont("Consolas", 9))
        result_layout.addWidget(self.py_result_display)
        
        layout.addWidget(result_group)
        
        # 优缺点说明
        pros_cons_group = QGroupBox("Python线程池特点")
        pros_cons_layout = QVBoxLayout(pros_cons_group)
        
        pros_cons_text = """
✅ 优点:
• 代码简洁，使用简单
• 强大的Future对象，支持取消
• 优秀的批量处理能力 (map, as_completed)
• 与asyncio等库集成良好
• 标准库，无额外依赖

❌ 缺点:
• 与Qt集成需要额外处理
• 无直接的进度反馈机制
• 需要轮询检查结果
• 跨线程UI更新需要小心处理

🎯 适用场景:
• 纯后台计算任务
• 批量数据处理
• 需要任务取消功能
• 与其他Python库集成
        """
        
        pros_cons_label = QLabel(pros_cons_text)
        pros_cons_label.setWordWrap(True)
        pros_cons_layout.addWidget(pros_cons_label)
        
        layout.addWidget(pros_cons_group)
        
        return widget
    
    def create_comparison_tab(self) -> QWidget:
        """创建对比总结选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("选择指南")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 对比表格文本
        comparison_text = """
📊 详细对比分析:

┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│      特性       │   QThreadPool   │ThreadPoolExecutor│     推荐场景     │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│   与Qt集成      │    ✅ 原生      │   ❌ 需要处理   │  Qt应用首选Qt   │
│   信号槽支持    │    ✅ 完美      │   ❌ 无直接     │  UI更新用Qt     │
│   进度反馈      │    ✅ 实时      │   ❌ 需要轮询   │  进度显示用Qt   │
│   任务取消      │    ❌ 较复杂    │   ✅ 简单       │  需要取消用Py   │
│   批量处理      │    ❌ 需要封装  │   ✅ 原生支持   │  批量任务用Py   │
│   代码复杂度    │    ⚠️ 较复杂   │   ✅ 简洁       │  简单任务用Py   │
│   错误处理      │    ✅ 信号机制  │   ✅ 异常捕获   │     都很好      │
│   性能表现      │    ✅ 优秀      │   ✅ 优秀       │     相当        │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

🎯 选择建议:

🔹 选择 QThreadPool 的情况:
   • PyQt/PySide 应用 (强烈推荐)
   • 需要实时UI更新
   • 需要进度反馈
   • 复杂的用户交互

🔹 选择 ThreadPoolExecutor 的情况:
   • 纯后台计算
   • 批量数据处理
   • 需要任务取消
   • 与其他Python库集成

🔹 混合使用策略:
   • UI相关任务 → QThreadPool
   • 计算任务 → ThreadPoolExecutor
   • 网络请求 → 根据需求选择

💡 最佳实践:
   1. 对于PyQt应用，优先考虑QThreadPool
   2. 简单的后台任务可以用ThreadPoolExecutor
   3. 复杂项目可以两者结合使用
   4. 始终在主线程中更新UI
   5. 合理设置线程池大小
        """
        
        comparison_label = QLabel(comparison_text)
        comparison_label.setFont(QFont("Consolas", 9))
        comparison_label.setWordWrap(True)
        comparison_label.setAlignment(Qt.AlignTop)
        layout.addWidget(comparison_label)
        
        return widget
    
    # ========== Qt线程池任务处理 ==========
    
    def start_qt_task(self):
        """启动Qt线程池任务"""
        task_name = f"Qt任务_{int(time.time()) % 1000}"
        
        # 创建任务
        task = QtTask(task_name, duration=3)
        
        # 连接信号
        task.signals.started.connect(self.on_qt_task_started)
        task.signals.progress.connect(self.on_qt_task_progress)
        task.signals.finished.connect(self.on_qt_task_finished)
        task.signals.error.connect(self.on_qt_task_error)
        
        # 启动任务
        self.qt_pool.start(task)
        
        self.qt_result_display.append(f"🚀 启动Qt任务: {task_name}")
    
    def on_qt_task_started(self):
        """Qt任务开始"""
        self.active_qt_tasks += 1
        self.update_qt_status()
        
        self.qt_progress_bar.setVisible(True)
        self.qt_progress_bar.setValue(0)
        
        self.qt_result_display.append("⏳ Qt任务开始执行...")
    
    def on_qt_task_progress(self, progress, message):
        """Qt任务进度更新"""
        self.qt_progress_bar.setValue(progress)
        self.qt_result_display.append(f"📈 进度: {message}")
    
    def on_qt_task_finished(self, result):
        """Qt任务完成"""
        self.active_qt_tasks -= 1
        self.update_qt_status()
        
        self.qt_progress_bar.setVisible(False)
        
        self.qt_result_display.append("✅ Qt任务完成!")
        self.qt_result_display.append(f"📊 结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        self.qt_result_display.append("=" * 50)
    
    def on_qt_task_error(self, error):
        """Qt任务错误"""
        self.active_qt_tasks -= 1
        self.update_qt_status()
        
        self.qt_progress_bar.setVisible(False)
        
        self.qt_result_display.append(f"❌ Qt任务失败: {error}")
        self.qt_result_display.append("=" * 50)
    
    def update_qt_status(self):
        """更新Qt任务状态"""
        self.qt_status_label.setText(f"活跃任务: {self.active_qt_tasks}")
    
    # ========== Python线程池任务处理 ==========
    
    def start_python_task(self):
        """启动Python线程池任务"""
        task_name = f"Python任务_{int(time.time()) % 1000}"
        
        # 提交任务
        future = self.py_executor.submit(python_task_function, task_name, 3)
        
        # 记录任务
        self.py_futures.append({
            'future': future,
            'task_name': task_name,
            'start_time': time.time()
        })
        
        self.active_py_tasks += 1
        self.update_py_status()
        
        self.py_result_display.append(f"🚀 启动Python任务: {task_name}")
        self.py_result_display.append("⏳ Python任务执行中... (无进度反馈)")
    
    def start_batch_tasks(self):
        """启动批量Python任务"""
        task_names = [f"批量任务_{i}" for i in range(5)]
        
        # 使用map批量提交
        futures = [self.py_executor.submit(python_task_function, name, 2) for name in task_names]
        
        # 记录所有任务
        for i, future in enumerate(futures):
            self.py_futures.append({
                'future': future,
                'task_name': task_names[i],
                'start_time': time.time()
            })
        
        self.active_py_tasks += len(futures)
        self.update_py_status()
        
        self.py_result_display.append(f"🚀 启动批量Python任务: {len(task_names)} 个")
        self.py_result_display.append("⏳ 批量任务执行中...")
    
    def check_python_results(self):
        """检查Python任务结果 (轮询机制)"""
        completed_futures = []
        
        for task_info in self.py_futures:
            future = task_info['future']
            task_name = task_info['task_name']
            
            if future.done():
                try:
                    result = future.result()
                    duration = time.time() - task_info['start_time']
                    
                    self.py_result_display.append(f"✅ Python任务完成: {task_name}")
                    self.py_result_display.append(f"⏱️ 实际耗时: {duration:.2f}秒")
                    self.py_result_display.append(f"📊 结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    self.py_result_display.append("=" * 50)
                    
                except Exception as e:
                    self.py_result_display.append(f"❌ Python任务失败: {task_name} - {e}")
                    self.py_result_display.append("=" * 50)
                
                completed_futures.append(task_info)
                self.active_py_tasks -= 1
        
        # 移除已完成的任务
        for task_info in completed_futures:
            self.py_futures.remove(task_info)
        
        if completed_futures:
            self.update_py_status()
    
    def update_py_status(self):
        """更新Python任务状态"""
        self.py_status_label.setText(f"活跃任务: {self.active_py_tasks}")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 关闭Python线程池
        self.py_executor.shutdown(wait=False)
        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    app.setApplicationName("线程池对比演示")
    app.setApplicationVersion("1.0")
    
    print("=" * 60)
    print("Qt线程池 vs Python线程池对比演示")
    print("=" * 60)
    print("这个演示将帮助你理解两种线程池的区别:")
    print("1. QThreadPool + QRunnable (Qt方式)")
    print("2. ThreadPoolExecutor (Python方式)")
    print("3. 各自的优缺点和适用场景")
    print("=" * 60)
    
    try:
        window = ThreadPoolComparisonWindow()
        window.show()
        
        print("演示程序启动成功！")
        print("请在不同选项卡中测试两种线程池的功能")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
