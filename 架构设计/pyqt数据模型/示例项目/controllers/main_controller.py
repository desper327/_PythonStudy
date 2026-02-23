"""
主控制器 - 协调模型和视图之间的交互
"""
from Qt.QtCore import QObject
from models.data_models import Task, TaskRepository, TaskStatus
from models.qt_models import TaskListModel
from views.main_view import MainView

class MainController(QObject):
    """主控制器"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化模型
        self.repository = TaskRepository()
        self.model = TaskListModel(self.repository)
        
        # 初始化视图
        self.view = MainView()
        # self.view.set_model(self.model) # 不再需要
        
        # 连接信号和槽
        self.connect_signals()
        
        # 添加一些示例数据
        self.add_sample_data()
    
    def connect_signals(self):
        """连接视图信号到控制器方法"""
        # 视图信号连接
        self.view.addTaskRequested.connect(self.add_task)
        self.view.deleteTaskRequested.connect(self.delete_task)
        self.view.updateTaskStatusRequested.connect(self.update_task_status)
        
        # 模型信号连接到UI更新槽
        self.model.taskAdded.connect(self.on_task_added_ui_update)
        self.model.taskRemoved.connect(self.on_task_removed_ui_update)
        self.model.taskUpdated.connect(self.on_task_updated_ui_update)
        self.model.modelReset.connect(self.on_model_reset_ui_update)
    
    def add_task(self, task_data: dict):
        """添加任务，从view发出的信号触发了槽函数，然后操作模型添加任务"""
        try:
            success = self.model.add_task(task_data)
            if success:
                self.view.show_message("成功", "任务添加成功！")
            else:
                self.view.show_message("错误", "任务添加失败！", "error")
        except Exception as e:
            self.view.show_message("错误", f"添加任务时发生错误：{str(e)}", "error")
    
    def delete_task(self, row: int):
        """删除任务"""
        try:
            success = self.model.remove_task(row)
            if success:
                self.view.show_message("成功", "任务删除成功！")
            else:
                self.view.show_message("错误", "任务删除失败！", "error")
        except Exception as e:
            self.view.show_message("错误", f"删除任务时发生错误：{str(e)}", "error")
    
    def update_task_status(self, row: int, status: TaskStatus):
        """更新任务状态"""
        try:
            success = self.model.update_task_status(row, status)
            if success:
                status_text = {
                    TaskStatus.PENDING: "待处理",
                    TaskStatus.IN_PROGRESS: "进行中",
                    TaskStatus.COMPLETED: "已完成"
                }.get(status, "未知")
                self.view.show_message("成功", f"任务状态已更新为：{status_text}")
            else:
                self.view.show_message("错误", "任务状态更新失败！", "error")
        except Exception as e:
            self.view.show_message("错误", f"更新任务状态时发生错误：{str(e)}", "error")
    
    def on_task_added_ui_update(self, task: Task):
        """槽函数：当模型添加任务后，更新视图"""
        status_text = self.get_status_text(task.status)
        display_text = f"[{status_text}] {task.name}"
        self.view.add_task_item(display_text)
        print(f"UI已更新：添加任务 {task.name}")

    def on_task_removed_ui_update(self, row: int):
        """槽函数：当模型删除任务后，更新视图"""
        self.view.remove_task_item(row)
        print(f"UI已更新：删除第 {row} 行的任务")

    def on_task_updated_ui_update(self, row: int, task: Task):
        """槽函数：当模型更新任务后，更新视图"""
        status_text = self.get_status_text(task.status)
        display_text = f"[{status_text}] {task.name}"
        self.view.update_task_item(row, display_text)
        print(f"UI已更新：更新第 {row} 行的任务")
        
    def on_model_reset_ui_update(self):
        """槽函数：当整个模型重置时，完全刷新UI"""
        self.view.clear_task_list()
        for task in self.model._tasks: # 直接访问了内部数据，仅为示例
            status_text = self.get_status_text(task.status)
            display_text = f"[{status_text}] {task.name}"
            self.view.add_task_item(display_text)
        print("UI已完全刷新")

    def get_status_text(self, status: TaskStatus) -> str:
        """辅助函数：获取状态的文本表示"""
        return {
            TaskStatus.PENDING: "待处理",
            TaskStatus.IN_PROGRESS: "进行中",
            TaskStatus.COMPLETED: "已完成"
        }.get(status, "未知")
    
    def add_sample_data(self):
        """添加示例数据"""
        sample_tasks = [
            {"name": "学习PyQt5", "description": "掌握PyQt5的基本用法"},
            {"name": "理解MVC架构", "description": "深入理解模型-视图-控制器架构模式", "status": TaskStatus.IN_PROGRESS},
            {"name": "完成项目", "description": "完成一个完整的MVC项目", "status": TaskStatus.COMPLETED}
        ]
        
        for task_data in sample_tasks:
            self.model.add_task(task_data)
    
    def show(self):
        """显示主窗口"""
        self.view.show()