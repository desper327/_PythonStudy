"""
任务仓库 - 管理任务数据的业务逻辑，包含自定义信号
这个类继承自QObject，可以发射信号通知数据变化
"""
from typing import List, Optional
from Qt.QtCore import QObject, Signal
from .data_models import Task, TaskStatus, SignalData

class TaskRepository(QObject):
    """任务仓库 - 带有信号的数据管理层"""
    
    # 自定义信号 - 当数据发生变化时发射这些信号
    # task_added = Signal(Task)  # 任务添加信号
    # task_removed = Signal(int, Task)  # 任务删除信号 (索引, 任务对象)
    # task_updated = Signal(int, Task)  # 任务更新信号 (索引, 任务对象)
    # tasks_cleared = Signal()  # 清空所有任务信号
    model_signal = Signal(SignalData)  # 任务信号 (任务对象)
    
    def __init__(self):
        super().__init__()
        self._tasks: List[Task] = []
        self._next_id = 1
    
    def add_task(self, task: Task) -> Task:
        """
        添加新任务
        
        Args:
            task_data: 包含任务信息的字典
            
        Returns:
            Task: 创建的任务对象
            
        Raises:
            ValueError: 当任务数据无效时
        """
        try:
            # 创建任务对象，Pydantic会自动验证数据
            task.id = self._next_id
            self._next_id += 1
            
            # 添加到内部列表
            self._tasks.append(task)
            
            # 发射信号通知任务已添加
            #self.task_added.emit(task)
            self.model_signal.emit(SignalData(signal_type="add_task", params=[task]))
            
            return task
        except Exception as e:
            raise ValueError(f"添加任务失败: {str(e)}")
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务的副本"""
        return self._tasks.copy()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_task_by_index(self, index: int) -> Optional[Task]:
        """根据索引获取任务"""
        if 0 <= index < len(self._tasks):
            return self._tasks[index]
        return None
    
    def update_task(self, index: int, updates: dict) -> bool:
        """
        更新任务
        
        Args:
            index: 任务在列表中的索引
            updates: 要更新的字段字典
            
        Returns:
            bool: 更新是否成功
        """
        if 0 <= index < len(self._tasks):
            task = self._tasks[index]
            
            try:
                # 更新任务属性
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                
                # 如果更新了状态，调用相应的方法
                if 'status' in updates:
                    status = updates['status']
                    if status == TaskStatus.COMPLETED:
                        task.mark_completed()
                    elif status == TaskStatus.IN_PROGRESS:
                        task.mark_in_progress()
                    elif status == TaskStatus.PENDING:
                        task.mark_pending()
                
                # 发射信号通知任务已更新
                #self.task_updated.emit(index, task)
                self.model_signal.emit(SignalData(signal_type="update_task", params=[index,task]))
                return True
                
            except Exception as e:
                print(f"更新任务失败: {e}")
                return False
        return False
    
    def delete_task(self, index: int) -> bool:
        """
        删除任务
        
        Args:
            index: 要删除的任务索引
            
        Returns:
            bool: 删除是否成功
        """
        if 0 <= index < len(self._tasks):
            task = self._tasks[index]
            
            # 从列表中移除
            del self._tasks[index]
            
            # 发射信号通知任务已删除
            #self.task_removed.emit(index, task)
            self.model_signal.emit(SignalData(signal_type="delete_task", params=[index, task]))
            return True
        return False
    
    def clear_all_tasks(self):
        """清空所有任务"""
        self._tasks.clear()
        self._next_id = 1
        
        # 发射信号通知所有任务已清空
        #self.tasks_cleared.emit()
        self.model_signal.emit(SignalData(signal_type="clear_all_tasks", params=[]))
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """根据状态获取任务"""
        return [task for task in self._tasks if task.status == status]
    
    def get_task_count(self) -> int:
        """获取任务总数"""
        return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """获取已完成任务数量"""
        return len([task for task in self._tasks if task.status == TaskStatus.COMPLETED])
    
    def get_pending_count(self) -> int:
        """获取待处理任务数量"""
        return len([task for task in self._tasks if task.status == TaskStatus.PENDING])
    
    def get_in_progress_count(self) -> int:
        """获取进行中任务数量"""
        return len([task for task in self._tasks if task.status == TaskStatus.IN_PROGRESS])