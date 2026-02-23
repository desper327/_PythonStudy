# MVC Framework 使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

1. 安装MySQL并启动服务
2. 创建数据库：
   ```sql
   CREATE DATABASE mvc_framework CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 复制配置文件：
   ```bash
   cp .env.example .env
   ```
4. 编辑 `.env` 文件，配置数据库连接

### 3. 运行程序

```bash
python run.py
# 或者
python main.py
```

## 控制器架构说明

### 重构后的控制器结构

框架采用了分层的控制器架构，将复杂的逻辑分散到不同的专门控制器中：

```
MainController (主控制器)
├── DialogController (对话框控制器)
├── TaskController (任务控制器)
└── ControllerManager (控制器管理器)
```

### 1. 主控制器 (MainController)

**职责：**
- 应用程序的总体协调
- 基础组件的初始化
- 子控制器的管理
- 主窗口事件的分发

**特点：**
- 简化的事件处理，将具体逻辑委托给子控制器
- 统一的资源管理和清理
- 状态监控和UI更新

### 2. 对话框控制器 (DialogController)

**职责：**
- 管理所有对话框的创建和显示
- 处理对话框内的用户交互
- 协调对话框与服务层的通信

**管理的对话框：**
- 功能对话框 (FeatureDialog)
- 数据处理对话框
- 设置对话框
- 其他自定义对话框

### 3. 任务控制器 (TaskController)

**职责：**
- 统一管理异步任务和线程任务
- 任务状态跟踪和进度监控
- 任务队列管理和优先级控制
- 任务结果回调处理

**支持的任务类型：**
- 数据处理任务
- 用户管理任务
- 报告生成任务
- 数据导出任务

### 4. 控制器管理器 (ControllerManager)

**职责：**
- 控制器的注册和生命周期管理
- 统一的初始化和清理流程
- 控制器间的协调

## 使用示例

### 添加新的对话框

1. **创建对话框类：**
```python
# views/dialogs/my_dialog.py
from PySide6.QtWidgets import QDialog
from ..dialogs.feature_dialog import FeatureDialog

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
```

2. **在对话框控制器中添加管理方法：**
```python
# controllers/dialog_controller.py
def show_my_dialog(self, parent_window=None, data=None):
    if not hasattr(self, 'my_dialog') or self.my_dialog is None:
        self.my_dialog = MyDialog(parent_window)
        self._connect_my_dialog_signals()
    
    self.my_dialog.show()
    return self.my_dialog
```

3. **在主控制器中添加调用：**
```python
# controllers/main_controller.py
def _handle_dialog_request(self, dialog_type: str, data: Dict[str, Any]) -> None:
    if self.dialog_controller:
        if dialog_type == "my_dialog":
            self.dialog_controller.show_my_dialog(self.main_window, data)
```

### 添加新的任务类型

1. **在服务层添加业务逻辑：**
```python
# services/my_service.py
class MyService:
    async def process_my_data(self, data):
        # 业务逻辑处理
        return result
```

2. **在任务控制器中添加任务类型：**
```python
# controllers/task_controller.py
def _create_async_coroutine(self, task_type: str, data: Dict[str, Any]):
    if task_type == "my_data_processing":
        return self.my_service.process_my_data(data)
    # ... 其他任务类型
```

3. **提交任务：**
```python
# 在任何控制器中
self.task_controller.submit_async_task(
    task_type="my_data_processing",
    data={"param1": "value1"},
    priority=1,
    callback=self._on_task_complete
)
```

### 添加新的子控制器

1. **创建控制器类：**
```python
# controllers/my_controller.py
from .base_controller import BaseController

class MyController(BaseController):
    async def initialize(self):
        # 初始化逻辑
        pass
    
    def setup_connections(self):
        # 信号连接
        pass
```

2. **在主控制器中注册：**
```python
# controllers/main_controller.py
async def _initialize_sub_controllers(self):
    # ... 其他控制器
    
    self.my_controller = MyController(self)
    self.controller_manager.register_controller("my", self.my_controller)
    
    await self.controller_manager.initialize_all()
```

## 最佳实践

### 1. 控制器职责分离

- **主控制器**：只负责协调，不处理具体业务逻辑
- **子控制器**：专注于特定领域的逻辑处理
- **避免**：在一个控制器中处理多种不相关的业务

### 2. 信号槽使用

- 使用Qt信号槽进行控制器间通信
- 避免直接调用其他控制器的方法
- 保持松耦合的设计

### 3. 异常处理

- 在每个控制器方法中添加适当的异常处理
- 使用日志记录错误信息
- 向用户提供友好的错误提示

### 4. 资源管理

- 在控制器的cleanup方法中释放资源
- 使用上下文管理器管理临时资源
- 避免内存泄漏

### 5. 测试友好

- 控制器方法保持简单和可测试
- 使用依赖注入便于单元测试
- 模拟外部依赖进行测试

## 调试技巧

### 1. 日志输出

每个控制器都有内置的日志方法：
```python
self.log_message("操作完成")
self.log_message("发生错误", is_error=True)
```

### 2. 任务状态监控

```python
# 获取任务状态
status = self.task_controller.get_task_status(task_id)

# 获取任务摘要
summary = self.task_controller.get_task_summary()
```

### 3. 控制器状态检查

```python
# 检查控制器是否已初始化
if self.dialog_controller.is_initialized():
    # 执行操作
    pass
```

## 常见问题

### Q: 如何在对话框中访问主窗口的数据？

A: 通过控制器传递数据，避免直接访问：
```python
def show_dialog_with_data(self, data):
    dialog = self.create_dialog()
    dialog.set_data(data)
    dialog.show()
```

### Q: 如何处理长时间运行的任务？

A: 使用任务控制器提交异步或线程任务：
```python
self.task_controller.submit_async_task(
    task_type="long_running_task",
    data=task_data,
    callback=self._on_task_complete
)
```

### Q: 如何在控制器间共享数据？

A: 通过服务层或使用Qt信号传递数据：
```python
# 通过信号传递
self.data_updated.emit(data)

# 通过服务层共享
shared_data = self.data_service.get_shared_data()
```

这种分层的控制器架构使得代码更加模块化、可维护和可扩展。每个控制器都有明确的职责，便于团队开发和代码维护。
