# 自定义信号槽架构 - 任务管理器

## 项目概述

这是一个演示如何**不依赖Qt的Model/View框架**，而是使用**自定义信号和槽机制**来手动同步数据和UI的PyQt5项目。

## 架构特点

### 核心理念
- **数据层发射信号**：`TaskRepository`继承`QObject`，在数据变化时发射自定义信号
- **控制器连接信号槽**：`MainController`作为"胶水层"，连接数据信号到UI更新方法
- **视图提供手动操作接口**：`MainView`使用`QListWidget`，提供明确的UI操作方法
- **完全手动控制**：不依赖Qt的Model/View自动更新机制

### 数据流向

```
用户操作 → View发射信号 → Controller处理 → Repository更新数据 → Repository发射信号 → Controller接收 → Controller调用View方法 → UI更新
```

## 项目结构

```
示例项目2/
├── main.py                     # 应用程序入口
├── models/                     # 数据模型层
│   ├── __init__.py
│   ├── data_models.py         # 业务数据模型（Task, TaskStatus）
│   └── task_repository.py     # 数据仓库（带自定义信号）
├── views/                      # 视图层
│   ├── __init__.py
│   └── main_view.py           # 主视图（手动UI操作）
└── controllers/                # 控制器层
    ├── __init__.py
    └── main_controller.py      # 主控制器（信号槽连接）
```

## 关键组件说明

### 1. TaskRepository (数据仓库)
- 继承`QObject`，可以发射信号
- 定义自定义信号：`task_added`, `task_removed`, `task_updated`, `tasks_cleared`
- 在数据操作后发射相应信号通知变化

### 2. MainView (视图)
- 使用`QListWidget`而不是`QListView`
- 提供手动UI操作方法：`add_task_item()`, `remove_task_item()`, `update_task_item()`等
- 发射用户操作信号：`add_task_requested`, `delete_task_requested`等

### 3. MainController (控制器)
- 连接视图信号到处理方法
- 连接仓库信号到UI更新槽函数
- 作为数据层和视图层之间的协调者

## 与标准Model/View架构的对比

| 特性 | 标准Model/View | 自定义信号槽 |
|------|----------------|--------------|
| UI组件 | QListView + QAbstractListModel | QListWidget |
| 数据同步 | 自动（内置信号） | 手动（自定义信号） |
| 更新控制 | 框架控制 | 完全手动控制 |
| 复杂度 | 较低（框架处理） | 较高（需要手动管理） |
| 灵活性 | 受框架限制 | 完全自定义 |
| 适用场景 | 标准列表/表格 | 特殊UI需求 |

## 运行项目

```bash
cd 示例项目2
python main.py
```

## 功能特性

- ✅ 添加任务（支持名称、描述、初始状态）
- ✅ 删除任务（带确认对话框）
- ✅ 更新任务状态（待处理/进行中/已完成）
- ✅ 清空所有任务
- ✅ 实时统计信息显示
- ✅ 详细的控制台日志输出
- ✅ 美观的任务显示格式（带状态图标和时间）

## 学习要点

1. **信号定义**：如何在自定义类中定义和发射PyQt信号
2. **槽函数连接**：如何连接信号到槽函数
3. **手动UI更新**：如何直接操作UI组件而不依赖模型
4. **架构解耦**：如何通过控制器实现数据层和视图层的解耦
5. **事件驱动**：如何构建事件驱动的应用程序架构

## 注意事项

- 这种架构适合对UI有特殊控制需求的场景
- 对于标准的列表/表格显示，推荐使用Qt的Model/View框架
- 手动管理UI更新需要更多的代码和注意事项
- 需要确保信号槽连接的正确性，避免内存泄漏