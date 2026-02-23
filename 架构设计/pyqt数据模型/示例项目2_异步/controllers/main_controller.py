"""
主控制器 - 协调模型和视图之间的交互
使用自定义信号和槽机制，手动同步数据和UI
"""
from PyQt5.QtCore import QObject
from models.data_models import Task, TaskStatus
from models.task_repository import TaskRepository
from views.main_view import MainView

class MainController(QObject):
    """主控制器 - 使用自定义信号槽架构"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化数据仓库
        self.repository = TaskRepository()
        
        # 初始化视图
        self.view = MainView()
        
        # 连接信号和槽
        self.connect_signals()
        
        # 添加一些示例数据
        self.add_sample_data()
        
        # 初始化UI统计信息
        self.update_ui_statistics()
    
    def connect_signals(self):
        """连接视图信号到控制器方法，连接仓库信号到UI更新方法"""
        
        # ========== 视图信号 -> 控制器方法 ==========
        # 用户在UI上的操作请求
        self.view.add_task_requested.connect(self.handle_add_task)
        self.view.delete_task_requested.connect(self.handle_delete_task)
        self.view.update_task_status_requested.connect(self.handle_update_task_status)
        self.view.clear_all_requested.connect(self.handle_clear_all)
        
        # ========== 仓库信号 -> UI更新槽函数 ==========
        # 数据变化时自动更新UI
        self.repository.task_added.connect(self.on_task_added_update_ui)
        self.repository.task_removed.connect(self.on_task_removed_update_ui)
        self.repository.task_updated.connect(self.on_task_updated_update_ui)
        self.repository.tasks_cleared.connect(self.on_tasks_cleared_update_ui)
    
    # ========== 处理视图请求的方法 ==========
    
    def handle_add_task(self, task_data: dict):
        """
        处理添加任务请求
        
        Args:
            task_data: 包含任务信息的字典
        """
        try:
            # 调用仓库添加任务，仓库会发射task_added信号
            task = self.repository.add_task(task_data)
            self.view.show_message("成功", f"任务 '{task.name}' 添加成功！")
            print(f"[Controller] 处理添加任务请求: {task.name}")
        except Exception as e:
            self.view.show_message("错误", f"添加任务失败：{str(e)}", "error")
            print(f"[Controller] 添加任务失败: {e}")
    
    def handle_delete_task(self, index: int):
        """
        处理删除任务请求
        
        Args:
            index: 要删除的任务索引
        """
        try:
            task = self.repository.get_task_by_index(index)
            if task:
                # 调用仓库删除任务，仓库会发射task_removed信号
                success = self.repository.delete_task(index)
                if success:
                    self.view.show_message("成功", f"任务 '{task.name}' 删除成功！")
                    print(f"[Controller] 处理删除任务请求: {task.name}")
                else:
                    self.view.show_message("错误", "删除任务失败！", "error")
            else:
                self.view.show_message("错误", "找不到要删除的任务！", "error")
        except Exception as e:
            self.view.show_message("错误", f"删除任务时发生错误：{str(e)}", "error")
            print(f"[Controller] 删除任务失败: {e}")
    
    def handle_update_task_status(self, index: int, status: TaskStatus):
        """
        处理更新任务状态请求
        
        Args:
            index: 任务索引
            status: 新的任务状态
        """
        try:
            task = self.repository.get_task_by_index(index)
            if task:
                # 调用仓库更新任务，仓库会发射task_updated信号
                success = self.repository.update_task(index, {'status': status})
                if success:
                    status_text = self.get_status_text(status)
                    self.view.show_message("成功", f"任务 '{task.name}' 状态已更新为：{status_text}")
                    print(f"[Controller] 处理更新任务状态请求: {task.name} -> {status_text}")
                else:
                    self.view.show_message("错误", "更新任务状态失败！", "error")
            else:
                self.view.show_message("错误", "找不到要更新的任务！", "error")
        except Exception as e:
            self.view.show_message("错误", f"更新任务状态时发生错误：{str(e)}", "error")
            print(f"[Controller] 更新任务状态失败: {e}")
    
    def handle_clear_all(self):
        """处理清空所有任务请求"""
        try:
            # 调用仓库清空任务，仓库会发射tasks_cleared信号
            self.repository.clear_all_tasks()
            self.view.show_message("成功", "所有任务已清空！")
            print("[Controller] 处理清空所有任务请求")
        except Exception as e:
            self.view.show_message("错误", f"清空任务时发生错误：{str(e)}", "error")
            print(f"[Controller] 清空任务失败: {e}")
    
    # ========== 响应仓库信号的UI更新槽函数 ==========
    
    def on_task_added_update_ui(self, task: Task):
        """
        槽函数：当仓库添加任务后，更新UI
        
        Args:
            task: 新添加的任务对象
        """
        # 格式化任务显示文本
        display_text = self.format_task_display_text(task)
        
        # 调用视图的方法添加任务项
        self.view.add_task_item(display_text, task.id)
        
        # 更新统计信息
        self.update_ui_statistics()
        
        print(f"[Controller] UI已更新 - 添加任务: {task.name}")
    
    def on_task_removed_update_ui(self, index: int, task: Task):
        """
        槽函数：当仓库删除任务后，更新UI
        
        Args:
            index: 被删除任务的索引
            task: 被删除的任务对象
        """
        # 调用视图的方法移除任务项
        self.view.remove_task_item(index)
        
        # 更新统计信息
        self.update_ui_statistics()
        
        print(f"[Controller] UI已更新 - 删除任务: {task.name} (索引: {index})")
    
    def on_task_updated_update_ui(self, index: int, task: Task):
        """
        槽函数：当仓库更新任务后，更新UI
        
        Args:
            index: 被更新任务的索引
            task: 更新后的任务对象
        """
        # 格式化任务显示文本
        display_text = self.format_task_display_text(task)
        
        # 调用视图的方法更新任务项
        self.view.update_task_item(index, display_text)
        
        # 更新统计信息
        self.update_ui_statistics()
        
        print(f"[Controller] UI已更新 - 更新任务: {task.name} (索引: {index})")
    
    def on_tasks_cleared_update_ui(self):
        """槽函数：当仓库清空所有任务后，更新UI"""
        # 调用视图的方法清空任务列表
        self.view.clear_task_list()
        
        # 更新统计信息
        self.update_ui_statistics()
        
        print("[Controller] UI已更新 - 清空所有任务")
    
    # ========== 辅助方法 ==========
    
    def format_task_display_text(self, task: Task) -> str:
        """
        格式化任务显示文本
        
        Args:
            task: 任务对象
            
        Returns:
            str: 格式化后的显示文本
        """
        status_text = self.get_status_text(task.status)
        created_time = task.created_at.strftime("%m-%d %H:%M")
        
        # 根据状态添加不同的前缀符号
        status_symbol = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅"
        }.get(task.status, "❓")
        
        display_text = f"{status_symbol} [{status_text}] {task.name}"
        
        if task.description:
            # 如果描述太长，截断显示
            desc = task.description[:30] + "..." if len(task.description) > 30 else task.description
            display_text += f" - {desc}"
        
        display_text += f" ({created_time})"
        
        return display_text
    
    def get_status_text(self, status: TaskStatus) -> str:
        """
        获取状态的中文文本表示
        
        Args:
            status: 任务状态枚举
            
        Returns:
            str: 状态的中文文本
        """
        return {
            TaskStatus.PENDING: "待处理",
            TaskStatus.IN_PROGRESS: "进行中",
            TaskStatus.COMPLETED: "已完成"
        }.get(status, "未知")
    
    def update_ui_statistics(self):
        """更新UI中的统计信息"""
        total = self.repository.get_task_count()
        pending = self.repository.get_pending_count()
        in_progress = self.repository.get_in_progress_count()
        completed = self.repository.get_completed_count()
        
        # 调用视图的方法更新统计信息
        self.view.update_statistics(total, pending, in_progress, completed)
    
    def add_sample_data(self):
        """添加示例数据"""
        sample_tasks = [
            {
                "name": "学习PyQt5自定义信号槽",
                "description": "深入理解PyQt5中自定义信号和槽的机制",
                "status": TaskStatus.IN_PROGRESS
            },
            {
                "name": "实现手动UI更新",
                "description": "不依赖Model/View框架，手动控制UI更新",
                "status": TaskStatus.PENDING
            },
            {
                "name": "完成项目文档",
                "description": "编写详细的项目说明文档",
                "status": TaskStatus.COMPLETED
            }
        ]
        
        print("[Controller] 添加示例数据...")
        for task_data in sample_tasks:
            try:
                self.repository.add_task(task_data)
            except Exception as e:
                print(f"[Controller] 添加示例数据失败: {e}")
    
    def show(self):
        """显示主窗口"""
        self.view.show()
        print("[Controller] 应用程序已启动")