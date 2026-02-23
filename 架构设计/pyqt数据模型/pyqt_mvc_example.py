# 导入必要的模块
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListView, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
# 尝试导入 pydantic，如果失败则提示用户安装
try:
    from pydantic import BaseModel, ValidationError, constr
except ImportError:
    print("错误：Pydantic 模块未找到。")
    print("请使用 'pip install pydantic' 命令进行安装。")
    sys.exit(1)

# --- Pydantic 数据模型定义 ---
# 定义我们的数据结构，并添加验证规则
# constr(strip_whitespace=True, min_length=1) 表示字符串必须至少有1个字符（在去除首尾空格后）
class Task(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    completed: bool = False

# --- 自定义数据模型 (Model) ---
class TaskModel(QAbstractListModel):
    """
    一个用于管理Task对象列表的自定义数据模型。
    继承自 QAbstractListModel，我们需要实现一些必要的方法。
    """
    def __init__(self, tasks=None):
        super().__init__()
        # 内部数据存储，使用Pydantic模型列表
        self.tasks = tasks or []

    def data(self, index, role):
        """ 返回指定索引和角色的数据 """
        if not index.isValid():
            return None

        # Qt.DisplayRole 是视图请求要显示的文本时使用的角色
        if role == Qt.DisplayRole:
            task = self.tasks[index.row()]
            status = "已完成" if task.completed else "未完成"
            return f"{task.name} ({status})"
        
        return None

    def rowCount(self, index=QModelIndex()):
        """ 返回模型中的行数 """
        return len(self.tasks)

    def add_task(self, task: Task):
        """ 向模型中添加一个新任务 """
        # beginInsertRows/endInsertRows 是必须的，它们通知视图数据即将改变
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.tasks.append(task)
        self.endInsertRows()

    def remove_task(self, row: int):
        """ 从模型中移除指定行的任务 """
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.tasks[row]
            self.endRemoveRows()

class MainWindow(QMainWindow):
    """
    主窗口类，扮演控制器的角色。
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("自定义模型与Pydantic验证示例")
        self.setGeometry(100, 100, 400, 300)

        # --- 模型 (Model) ---
        # 创建自定义模型的实例，并提供一些初始数据
        initial_tasks = [
            Task(name="学习PyQt5"),
            Task(name="学习MVC架构", completed=True),
            Task(name="编写一个应用")
        ]
        self.model = TaskModel(tasks=initial_tasks)

        # --- 视图 (View) ---
        self.listView = QListView()
        self.listView.setModel(self.model)

        # --- 控制器 (Controller) 的一部分：用户界面 ---
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("输入新任务名称")

        self.add_button = QPushButton("添加")
        self.delete_button = QPushButton("删除")

        # --- 事件处理 (Controller 的核心) ---
        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_item)

        # --- 布局管理 ---
        hbox = QHBoxLayout()
        hbox.addWidget(self.item_input)
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.delete_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listView)
        vbox.addLayout(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def add_item(self):
        """ 添加一个新项目到模型中，并进行数据验证 """
        text = self.item_input.text()

        try:
            # 1. 数据验证
            # 尝试用用户输入创建一个Task实例，Pydantic会自动进行验证
            new_task = Task(name=text)
            
            # 2. 更新模型
            # 如果验证成功，则将新任务添加到模型中
            self.model.add_task(new_task)
            self.item_input.clear()

        except ValidationError as e:
            # 3. 处理验证失败
            # 如果Pydantic抛出ValidationError，说明输入不符合规则
            # 我们向用户显示一个错误消息框
            QMessageBox.warning(self, "输入错误", f"任务名称不能为空！")

    def delete_item(self):
        """ 从模型中删除选定的项目 """
        selected_indexes = self.listView.selectedIndexes()

        if selected_indexes:
            index = selected_indexes[0]
            # 调用我们自定义模型的方法来删除任务
            self.model.remove_task(index.row())
        else:
            QMessageBox.warning(self, "警告", "请先选择要删除的项目！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())