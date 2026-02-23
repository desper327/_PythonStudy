# 三维影视制作管理系统

基于PySide6的MVC架构桌面应用程序，用于管理三维影视制作流程中的项目、任务和文件。

## 功能特性

### 核心功能
- **项目层级管理**：支持项目 → 集 → 场 → 镜头 → 阶段的完整层级结构
- **任务管理**：创建、分配、跟踪各个制作阶段的任务（动画、原画、灯光、特效、解算等）
- **文件管理**：管理与任务相关的文件和资源
- **异步数据处理**：通过网络API获取数据，支持耗时IO操作
- **实时UI更新**：异步操作完成后自动更新用户界面

### 技术特性
- **MVC架构**：清晰的模型-视图-控制器分离
- **多线程支持**：专用子线程处理网络请求和文件操作
- **进度跟踪**：实时显示操作进度和状态
- **报告生成**：自动生成项目和任务统计报告
- **过滤和搜索**：支持多条件筛选任务
- **现代UI设计**：基于PySide6的现代化用户界面

## 系统架构

```
film_production_manager/
├── models/                 # 数据模型层
│   ├── __init__.py
│   ├── data_models.py     # 核心数据模型
│   └── api_client.py      # API客户端
├── views/                  # 视图层
│   ├── __init__.py
│   └── main_window.py     # 主窗口界面
├── controllers/            # 控制器层
│   ├── __init__.py
│   └── main_controller.py # 主控制器
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── thread_workers.py  # 线程工作器
│   └── common_widgets.py  # 通用UI组件
├── resources/              # 资源文件
├── main.py                # 程序入口
├── config.py              # 配置文件
├── requirements.txt       # 依赖包列表
└── README.md             # 说明文档
```

## 安装和运行

### 环境要求
- Python 3.8 或更高版本
- PySide6 6.5.0 或更高版本

### 安装步骤

1. **克隆或下载项目**
   ```bash
   # 如果使用git
   git clone <repository-url>
   cd film_production_manager
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```bash
   python main.py
   ```

### 配置选项

程序支持通过环境变量进行配置：

```bash
# API服务器地址
export API_BASE_URL="http://your-api-server.com/api"

# API超时时间（秒）
export API_TIMEOUT="30"

# 日志级别
export LOG_LEVEL="INFO"

# 主题设置
export THEME="default"
```

## 使用指南

### 基本操作流程

1. **启动程序**
   - 运行 `python main.py` 启动应用程序
   - 程序会显示启动画面并初始化各个组件

2. **选择项目**
   - 在左侧面板的项目选择区域选择要管理的项目
   - 点击"刷新项目列表"获取最新的项目信息

3. **浏览项目结构**
   - 在项目结构树中展开项目节点
   - 可以看到集、场、镜头和制作阶段的层级结构
   - 点击任意节点查看对应的任务

4. **管理任务**
   - 在右侧的任务列表中查看当前选择层级的所有任务
   - 使用过滤器按阶段、状态、优先级等条件筛选任务
   - 双击任务可以查看详细信息

5. **生成报告**
   - 通过菜单栏的"工具" → "生成项目报告"创建统计报告
   - 报告包含摘要、任务列表和统计图表
   - 支持保存报告到文件

### 界面说明

#### 主窗口布局
- **左侧面板**：项目选择、项目结构树、过滤器
- **右侧面板**：任务列表、项目统计（选项卡切换）
- **菜单栏**：文件、视图、工具、帮助菜单
- **工具栏**：常用操作的快捷按钮
- **状态栏**：显示当前状态和项目信息

#### 任务表格列说明
- **任务名称**：任务的显示名称
- **阶段**：制作阶段（动画、原画、灯光等）
- **状态**：当前任务状态（待开始、进行中、已完成等）
- **负责人**：任务分配的责任人
- **优先级**：任务优先级（1-5级）
- **进度**：任务完成百分比
- **创建时间**：任务创建日期
- **截止时间**：任务预期完成日期

## 开发指南

### 项目结构说明

#### 数据模型层 (Models)
- `data_models.py`：定义核心数据结构
  - `Project`：项目数据类
  - `Episode`：集数据类
  - `Scene`：场数据类
  - `Shot`：镜头数据类
  - `Task`：任务数据类
  - `FileInfo`：文件信息数据类

- `api_client.py`：API客户端
  - 处理与后端服务的网络通信
  - 提供数据获取和更新接口
  - 包含模拟数据用于开发测试

#### 视图层 (Views)
- `main_window.py`：主窗口实现
  - `MainWindow`：主窗口类
  - `ProjectTreeWidget`：项目树组件
  - `TaskTableWidget`：任务表格组件

#### 控制器层 (Controllers)
- `main_controller.py`：主控制器
  - 协调视图和模型之间的交互
  - 管理业务逻辑和数据流
  - 处理用户操作和事件

#### 工具模块 (Utils)
- `thread_workers.py`：线程工作器
  - `BaseWorker`：基础工作器类
  - `ProjectDataWorker`：项目数据获取工作器
  - `TaskDataWorker`：任务数据获取工作器
  - `FileProcessWorker`：文件处理工作器
  - `BatchTaskWorker`：批量任务处理工作器
  - `ThreadManager`：线程管理器

- `common_widgets.py`：通用UI组件
  - `ProgressWidget`：进度条组件
  - `ReportDialog`：报告对话框
  - `ProjectStatisticsWidget`：项目统计组件
  - `FilterWidget`：过滤器组件
  - `ReportGenerator`：报告生成器

### 扩展开发

#### 添加新的制作阶段
1. 在 `data_models.py` 的 `ProductionStage` 枚举中添加新阶段
2. 更新相关的UI组件以支持新阶段
3. 在API客户端中添加对应的数据处理逻辑

#### 添加新的任务状态
1. 在 `data_models.py` 的 `TaskStatus` 枚举中添加新状态
2. 更新任务表格的状态显示样式
3. 在控制器中添加状态转换逻辑

#### 自定义报告格式
1. 在 `ReportGenerator` 类中添加新的报告生成方法
2. 创建对应的报告模板
3. 在主窗口菜单中添加新的报告选项

#### 集成外部API
1. 修改 `api_client.py` 中的API端点配置
2. 更新数据解析方法以匹配API响应格式
3. 在配置文件中添加API相关设置

## 故障排除

### 常见问题

1. **程序启动失败**
   - 检查Python版本是否满足要求（3.8+）
   - 确认已安装所有依赖包：`pip install -r requirements.txt`
   - 查看错误日志获取详细信息

2. **API连接失败**
   - 检查网络连接
   - 确认API服务器地址配置正确
   - 检查防火墙设置

3. **数据加载缓慢**
   - 检查网络连接速度
   - 考虑调整API超时设置
   - 查看是否有大量数据需要处理

4. **界面显示异常**
   - 检查屏幕分辨率和DPI设置
   - 尝试重置窗口大小
   - 检查系统主题兼容性

### 日志文件
程序运行时会在 `logs/app.log` 中记录详细日志，可以通过查看日志文件来诊断问题。

## 技术支持

如果遇到问题或需要技术支持，请：

1. 查看本文档的故障排除部分
2. 检查日志文件中的错误信息
3. 在项目仓库中提交Issue（如果适用）
4. 联系开发团队获取支持

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 更新日志

### v1.0.0 (2024-11-16)
- 初始版本发布
- 实现基础的项目和任务管理功能
- 支持多线程异步数据处理
- 提供现代化的用户界面
- 包含完整的MVC架构实现