"""
PyQt5适配器模型 - 连接业务模型和PyQt5视图
这些模型负责将业务数据转换为PyQt5视图可以理解的格式
"""
from Qt.QtCore import Signal, QObject, QAbstractListModel, QModelIndex, Qt
from typing import List
from .data_models import Task, TaskRepository, TaskStatus

class TaskListModel(QAbstractListModel):
    """任务列表的PyQt5适配器模型"""
    
    # 自定义信号
    taskAdded = Signal(Task)
    taskRemoved = Signal(int) # 新定义：传递被删除的行号 row
    taskUpdated = Signal(int, Task) # 新定义：传递被更新的行号 row 和 task 对象
    modelReset = Signal() # 新定义：用于通知模型已重置
    
    def __init__(self, repository: TaskRepository):
        super().__init__()
        self._repository = repository
        self._tasks = []
        self.refresh_data()
            
    def data(self, index: QModelIndex, role: int):
        """返回指定索引和角色的数据"""
        if not index.isValid() or index.row() >= len(self._tasks):
            return None
        
        task = self._tasks[index.row()]
        
        if role == Qt.DisplayRole:
            status_text = {
                TaskStatus.PENDING: "待处理",
                TaskStatus.IN_PROGRESS: "进行中", 
                TaskStatus.COMPLETED: "已完成"
            }.get(task.status, "未知")
            return f"[{status_text}] {task.name}"
        
        elif role == Qt.ToolTipRole:
            return f"任务: {task.name}\n描述: {task.description or '无'}\n创建时间: {task.created_at.strftime('%Y-%m-%d %H:%M')}"
        
        elif role == Qt.UserRole:
            # 返回完整的Task对象
            return task
        
        return None
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """返回行数"""
        return len(self._tasks)
    
    def refresh_data(self):
        """从仓库刷新数据"""
        self.beginResetModel()
        self._tasks = self._repository.get_all_tasks()
        self.endResetModel()
        self.modelReset.emit()
    
    def add_task(self, task_data: dict) -> bool:
        """添加任务"""
        try:
            task = self._repository.add_task(task_data)
            self.beginInsertRows(QModelIndex(), len(self._tasks), len(self._tasks))
            self._tasks.append(task)
            self.endInsertRows()
            self.taskAdded.emit(task)
            return True
        except Exception as e:
            print(f"添加任务失败: {e}")
            return False
    
    def remove_task(self, row: int) -> bool:
        """删除任务"""
        if 0 <= row < len(self._tasks):
            task = self._tasks[row]
            if self._repository.delete_task(task.id):
                self.beginRemoveRows(QModelIndex(), row, row)
                del self._tasks[row]
                self.endRemoveRows()
                self.taskRemoved.emit(row)
                return True
        return False
    
    def update_task_status(self, row: int, status: TaskStatus) -> bool:
        """更新任务状态"""
        if 0 <= row < len(self._tasks):
            task = self._tasks[row]
            if self._repository.update_task(task.id, {'status': status}):
                # 更新本地缓存
                task.status = status
                if status == TaskStatus.COMPLETED:
                    task.mark_completed()
                elif status == TaskStatus.IN_PROGRESS:
                    task.mark_in_progress()
                
                # 通知视图更新
                index = self.index(row, 0)
                self.dataChanged.emit(index, index, [Qt.DisplayRole])
                self.taskUpdated.emit(row, task)
                return True
        return False
    
    def get_task(self, row: int) -> Task:
        """获取指定行的任务"""
        if 0 <= row < len(self._tasks):
            return self._tasks[row]
        return None