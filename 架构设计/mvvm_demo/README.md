# MVVM Demo - PyQt6

This demo shows a complete **MVVM (Model-View-ViewModel)** architecture implementation using PyQt6.

## Architecture Overview

### Model Layer (`models.py`)
- `User`: Data class representing user information
- `UserModel`: Business logic and data management
- Emits signals when data changes (user_added, user_updated, user_removed)

### ViewModel Layer (`viewmodels.py`)
- `UserViewModel`: Bridges between Model and View
- Exposes observable properties using PyQt's `@pyqtProperty`
- Provides commands for user actions (addUser, updateUser, removeUser, clearForm)
- Handles data validation and transformation
- Automatically updates UI when Model data changes

### View Layer (`views.py`)
- `UserListView`: Pure UI presentation
- Binds UI controls to ViewModel properties
- No business logic, only UI behavior
- Updates automatically through property binding

## Key MVVM Features Demonstrated

### 1. Data Binding
```python
# ViewModel property
@pyqtProperty(str, notify=nameChanged)
def name(self) -> str:
    return self._name

# View binds to this property
self._viewmodel.nameChanged.connect(self._update_name_edit)
```

### 2. Command Pattern
```python
# ViewModel commands
def addUser(self):
    # Validation and business logic
    # Calls Model to add data

# View connects buttons to commands
self.add_button.clicked.connect(self._viewmodel.addUser)
```

### 3. Automatic UI Updates
- When Model data changes, ViewModel properties update
- View automatically reflects changes through bindings
- No manual UI manipulation in Controller

### 4. Separation of Concerns
- **Model**: Pure business logic, no UI dependencies
- **ViewModel**: UI-specific logic, no direct UI control
- **View**: Pure UI, no business logic

## Data Flow

```
User Action
    |
    v
View (Button Click)
    |
    v
ViewModel (Command)
    |
    v
Model (Business Logic)
    |
    v
ViewModel (Property Update)
    |
    v
View (Automatic UI Update)
```

## Running the Demo

```bash
cd mvvm_demo
python main.py
```

## Comparison with MVC

| Aspect | MVC | MVVM (This Demo) |
|--------|-----|------------------|
| UI Updates | Controller manually updates UI | Automatic through property binding |
| View Logic | Minimal, mostly passive | Pure UI, no business logic |
| Middle Layer | Controller (coordinates) | ViewModel (observable state) |
| Data Binding | Manual signal/slot connections | Automatic property binding |
| Testability | Harder (UI dependencies) | Easier (ViewModel can be tested independently) |

## Benefits of This MVVM Implementation

1. **Better Testability**: ViewModel can be unit tested without UI
2. **Cleaner Separation**: Clear boundaries between layers
3. **Automatic UI Sync**: Less manual UI update code
4. **Reusability**: ViewModel can be reused with different Views
5. **Maintainability**: Easier to modify UI or business logic independently

## Extending the Demo

- Add more complex validation rules in ViewModel
- Implement data persistence in Model
- Create additional Views for the same ViewModel
- Add undo/redo functionality using ViewModel commands
- Implement filtering/sorting in ViewModel




## MVVM 架构特点

### Model 层
- [UserModel](cci:2://file:///f:/Study/_PythonStudy/architecture_design/pyqt_data_model/MVC_Universal_Base/mvvm_demo/models.py:16:0-71:33) 处理业务逻辑，发出数据变更信号
- 不依赖任何 UI 组件

### ViewModel 层  
- 使用 `@pyqtProperty` 创建可观察属性
- 提供命令方法（addUser, updateUser, removeUser）
- 自动响应 Model 变更并更新属性

### View 层
- 纯 UI 展示，通过绑定连接到 ViewModel
- 按钮点击直接调用 ViewModel 命令
- UI 自动响应属性变化更新

## 数据流

```
用户操作 → View → ViewModel → Model → ViewModel → View(自动更新)
```

## 与原 MVC 的区别

| 特性 | 原 MVC | 新 MVVM |
|------|--------|---------|
| UI 更新 | Controller 手动调用 setText | 属性绑定自动更新 |
| 中间层 | Controller 协调 | ViewModel 状态管理 |
| 数据绑定 | 手动信号槽连接 | 自动属性绑定 |

## 运行方式

```bash
cd mvvm_demo
python main.py
```

注：代码中的导入错误是因为项目使用的是 `Qt` 而不是 `PyQt6`，你可以根据项目实际使用的 Qt 库调整导入语句。演示的核心架构模式和设计思路保持不变。