"""
通用UI组件模块
包含进度条、报告生成器等通用组件
"""
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, 
    QPushButton, QTextEdit, QDialog, QDialogButtonBox, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QScrollArea,
    QSplitter, QTabWidget, QComboBox, QSpinBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QBrush

from ..models.data_models import Project, Task, ProductionStage, TaskStatus


class ProgressWidget(QWidget):
    """进度条组件"""
    
    # 信号
    cancelled = Signal()  # 取消信号
    
    def __init__(self, title: str = "处理中...", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # 标题标签
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)
        
        # 状态标签
        self.status_label = QLabel("准备中...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # 详细信息文本
        self.detail_text = QTextEdit()
        self.detail_text.setMaximumHeight(100)
        self.detail_text.setReadOnly(True)
        layout.addWidget(self.detail_text)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.cancelled.emit)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # 设置样式
        self.setStyleSheet("""
            ProgressWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: #333;
            }
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 4px;
                text-align: center;
                background-color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
    
    def set_progress(self, value: int, status: str = ""):
        """设置进度"""
        self.progress_bar.setValue(value)
        if status:
            self.status_label.setText(status)
            self.add_detail(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")
    
    def add_detail(self, text: str):
        """添加详细信息"""
        self.detail_text.append(text)
        # 自动滚动到底部
        scrollbar = self.detail_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def set_title(self, title: str):
        """设置标题"""
        self.title = title
        self.title_label.setText(title)
    
    def start_animation(self):
        """开始动画效果"""
        self.animation_timer.start(100)
    
    def stop_animation(self):
        """停止动画效果"""
        self.animation_timer.stop()
    
    def update_animation(self):
        """更新动画"""
        # 简单的文本闪烁效果
        current_text = self.status_label.text()
        if current_text.endswith("..."):
            self.status_label.setText(current_text[:-3])
        else:
            self.status_label.setText(current_text + "...")
    
    def set_completed(self, success: bool = True):
        """设置完成状态"""
        self.stop_animation()
        self.cancel_button.setText("关闭")
        
        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText("完成")
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #4CAF50;
                }
            """)
        else:
            self.status_label.setText("失败")
            self.progress_bar.setStyleSheet("""
                QProgressBar::chunk {
                    background-color: #f44336;
                }
            """)


class ReportDialog(QDialog):
    """报告对话框"""
    
    def __init__(self, title: str = "报告", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Close
        )
        button_box.accepted.connect(self.save_report)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def add_summary_tab(self, data: Dict[str, Any]):
        """添加摘要选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 创建摘要信息
        summary_text = QTextEdit()
        summary_text.setReadOnly(True)
        
        # 格式化摘要信息
        summary_content = self._format_summary(data)
        summary_text.setHtml(summary_content)
        
        layout.addWidget(summary_text)
        self.tab_widget.addTab(widget, "摘要")
    
    def add_table_tab(self, title: str, data: List[Dict[str, Any]], headers: List[str]):
        """添加表格选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 创建表格
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        # 填充数据
        for row, item in enumerate(data):
            for col, header in enumerate(headers):
                value = item.get(header, "")
                table.setItem(row, col, QTableWidgetItem(str(value)))
        
        # 调整列宽
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        layout.addWidget(table)
        self.tab_widget.addTab(widget, title)
    
    def add_chart_tab(self, title: str, chart_data: Dict[str, Any]):
        """添加图表选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 创建简单的图表（这里用文本显示，实际项目可以集成matplotlib等）
        chart_widget = self._create_simple_chart(chart_data)
        layout.addWidget(chart_widget)
        
        self.tab_widget.addTab(widget, title)
    
    def _format_summary(self, data: Dict[str, Any]) -> str:
        """格式化摘要信息"""
        html = "<html><body>"
        html += f"<h2>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>"
        
        for key, value in data.items():
            if isinstance(value, dict):
                html += f"<h3>{key}</h3><ul>"
                for sub_key, sub_value in value.items():
                    html += f"<li><b>{sub_key}:</b> {sub_value}</li>"
                html += "</ul>"
            else:
                html += f"<p><b>{key}:</b> {value}</p>"
        
        html += "</body></html>"
        return html
    
    def _create_simple_chart(self, chart_data: Dict[str, Any]) -> QWidget:
        """创建简单图表"""
        widget = QWidget()
        widget.setMinimumHeight(300)
        
        # 这里可以集成matplotlib或其他图表库
        # 暂时用文本显示
        layout = QVBoxLayout(widget)
        
        chart_text = QTextEdit()
        chart_text.setReadOnly(True)
        
        content = "图表数据:\n"
        for key, value in chart_data.items():
            content += f"{key}: {value}\n"
        
        chart_text.setText(content)
        layout.addWidget(chart_text)
        
        return widget
    
    def save_report(self):
        """保存报告"""
        # 这里可以实现保存到文件的功能
        print("报告保存功能待实现")
        self.accept()


class ProjectStatisticsWidget(QWidget):
    """项目统计组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("项目统计")
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)
        
        # 统计卡片容器
        cards_layout = QHBoxLayout()
        
        # 总任务数卡片
        self.total_tasks_card = self._create_stat_card("总任务", "0", "#2196F3")
        cards_layout.addWidget(self.total_tasks_card)
        
        # 已完成任务卡片
        self.completed_tasks_card = self._create_stat_card("已完成", "0", "#4CAF50")
        cards_layout.addWidget(self.completed_tasks_card)
        
        # 进行中任务卡片
        self.in_progress_tasks_card = self._create_stat_card("进行中", "0", "#FF9800")
        cards_layout.addWidget(self.in_progress_tasks_card)
        
        # 完成率卡片
        self.completion_rate_card = self._create_stat_card("完成率", "0%", "#9C27B0")
        cards_layout.addWidget(self.completion_rate_card)
        
        layout.addLayout(cards_layout)
        
        # 阶段统计表格
        self.stage_table = QTableWidget()
        self.stage_table.setColumnCount(4)
        self.stage_table.setHorizontalHeaderLabels(["阶段", "总数", "已完成", "完成率"])
        self.stage_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.stage_table)
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QWidget:
        """创建统计卡片"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # 标题
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 数值
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)
        
        # 保存引用以便更新
        card.value_label = value_label
        
        return card
    
    def update_statistics(self, stats: Dict[str, Any]):
        """更新统计信息"""
        # 更新卡片
        self.total_tasks_card.value_label.setText(str(stats.get("total_tasks", 0)))
        self.completed_tasks_card.value_label.setText(str(stats.get("completed_tasks", 0)))
        self.in_progress_tasks_card.value_label.setText(str(stats.get("in_progress_tasks", 0)))
        
        completion_rate = stats.get("completion_rate", 0.0)
        self.completion_rate_card.value_label.setText(f"{completion_rate:.1%}")
        
        # 更新阶段统计表格
        stage_stats = stats.get("stage_statistics", {})
        self.stage_table.setRowCount(len(stage_stats))
        
        for row, (stage_name, stage_data) in enumerate(stage_stats.items()):
            self.stage_table.setItem(row, 0, QTableWidgetItem(stage_name))
            self.stage_table.setItem(row, 1, QTableWidgetItem(str(stage_data.get("total", 0))))
            self.stage_table.setItem(row, 2, QTableWidgetItem(str(stage_data.get("completed", 0))))
            
            stage_rate = stage_data.get("completion_rate", 0.0)
            self.stage_table.setItem(row, 3, QTableWidgetItem(f"{stage_rate:.1%}"))


class FilterWidget(QWidget):
    """过滤器组件"""
    
    # 信号
    filter_changed = Signal(dict)  # 过滤条件变化
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("过滤条件")
        title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(title_label)
        
        # 过滤器表单
        form_layout = QVBoxLayout()
        
        # 阶段过滤
        stage_layout = QHBoxLayout()
        stage_layout.addWidget(QLabel("阶段:"))
        
        self.stage_combo = QComboBox()
        self.stage_combo.addItem("全部", None)
        for stage in ProductionStage:
            self.stage_combo.addItem(stage.value, stage)
        self.stage_combo.currentIndexChanged.connect(self._on_filter_changed)
        stage_layout.addWidget(self.stage_combo)
        
        form_layout.addLayout(stage_layout)
        
        # 状态过滤
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("状态:"))
        
        self.status_combo = QComboBox()
        self.status_combo.addItem("全部", None)
        for status in TaskStatus:
            self.status_combo.addItem(status.value, status)
        self.status_combo.currentIndexChanged.connect(self._on_filter_changed)
        status_layout.addWidget(self.status_combo)
        
        form_layout.addLayout(status_layout)
        
        # 优先级过滤
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("优先级:"))
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItem("全部", None)
        for i in range(1, 6):
            self.priority_combo.addItem(f"优先级 {i}", i)
        self.priority_combo.currentIndexChanged.connect(self._on_filter_changed)
        priority_layout.addWidget(self.priority_combo)
        
        form_layout.addLayout(priority_layout)
        
        # 只显示我的任务
        self.my_tasks_checkbox = QCheckBox("只显示我的任务")
        self.my_tasks_checkbox.stateChanged.connect(self._on_filter_changed)
        form_layout.addWidget(self.my_tasks_checkbox)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        # 重置按钮
        reset_button = QPushButton("重置过滤")
        reset_button.clicked.connect(self.reset_filters)
        layout.addWidget(reset_button)
    
    def _on_filter_changed(self):
        """过滤条件变化"""
        filters = self.get_current_filters()
        self.filter_changed.emit(filters)
    
    def get_current_filters(self) -> Dict[str, Any]:
        """获取当前过滤条件"""
        return {
            "stage": self.stage_combo.currentData(),
            "status": self.status_combo.currentData(),
            "priority": self.priority_combo.currentData(),
            "my_tasks_only": self.my_tasks_checkbox.isChecked()
        }
    
    def reset_filters(self):
        """重置过滤条件"""
        self.stage_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self.priority_combo.setCurrentIndex(0)
        self.my_tasks_checkbox.setChecked(False)
        self._on_filter_changed()


class ReportGenerator:
    """报告生成器"""
    
    @staticmethod
    def generate_project_report(project: Project) -> ReportDialog:
        """生成项目报告"""
        dialog = ReportDialog(f"项目报告 - {project.project_name}")
        
        # 获取统计信息
        stats = project.get_project_statistics()
        
        # 添加摘要选项卡
        summary_data = {
            "项目名称": project.project_name,
            "项目描述": project.description,
            "创建时间": project.created_time.strftime("%Y-%m-%d"),
            "集数": len(project.episodes),
            "统计信息": stats
        }
        dialog.add_summary_tab(summary_data)
        
        # 添加任务列表选项卡
        all_tasks = project.get_all_tasks()
        task_data = []
        for task in all_tasks:
            task_data.append({
                "任务ID": task.task_id,
                "任务名称": task.task_name,
                "阶段": task.stage.value,
                "状态": task.status.value,
                "负责人": task.assignee,
                "优先级": task.priority,
                "进度": f"{task.progress:.1%}"
            })
        
        headers = ["任务ID", "任务名称", "阶段", "状态", "负责人", "优先级", "进度"]
        dialog.add_table_tab("任务列表", task_data, headers)
        
        # 添加图表选项卡
        chart_data = {
            "总任务数": stats["total_tasks"],
            "已完成": stats["completed_tasks"],
            "进行中": stats["in_progress_tasks"],
            "待开始": stats["pending_tasks"]
        }
        dialog.add_chart_tab("统计图表", chart_data)
        
        return dialog
    
    @staticmethod
    def generate_task_report(tasks: List[Task]) -> ReportDialog:
        """生成任务报告"""
        dialog = ReportDialog("任务报告")
        
        # 统计信息
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        in_progress_tasks = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
        
        summary_data = {
            "任务总数": total_tasks,
            "已完成": completed_tasks,
            "进行中": in_progress_tasks,
            "完成率": f"{completed_tasks/total_tasks:.1%}" if total_tasks > 0 else "0%"
        }
        dialog.add_summary_tab(summary_data)
        
        # 任务详情表格
        task_data = []
        for task in tasks:
            task_data.append({
                "任务名称": task.task_name,
                "阶段": task.stage.value,
                "状态": task.status.value,
                "负责人": task.assignee,
                "创建时间": task.created_time.strftime("%Y-%m-%d"),
                "进度": f"{task.progress:.1%}"
            })
        
        headers = ["任务名称", "阶段", "状态", "负责人", "创建时间", "进度"]
        dialog.add_table_tab("任务详情", task_data, headers)
        
        return dialog