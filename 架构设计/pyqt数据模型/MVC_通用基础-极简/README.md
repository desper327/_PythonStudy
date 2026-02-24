# MVC通用的基础，可以用这个作为基础模板使用

## 项目概述
从示例项目2_简单版演化而来
这是一个演示如何**不依赖Qt的Model/View框架**，而是使用**自定义信号和槽机制**来手动同步数据和UI的PyQt5项目。
目前已经实现只使用model和view只定义一个信号只携带一种参数，就可以互相传递，主要是利用signal_data 和 task 2个数据模型

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

