# MVC Framework

基于PySide6的MVC架构桌面应用程序框架，支持异步任务、多线程处理和数据验证。

## 特性

- **完整的MVC架构**: 清晰的模型-视图-控制器分离
- **异步支持**: 集成asyncio，支持异步任务处理
- **多线程支持**: 使用QThread处理耗时操作
- **数据验证**: 使用Pydantic进行数据验证和序列化
- **类型检查**: 使用Beartype进行运行时类型检查
- **数据库支持**: 使用SQLAlchemy + MySQL进行数据持久化
- **API集成**: 支持HTTP API调用
- **现代UI**: 基于PySide6的现代化用户界面
- **配置管理**: 支持环境变量和配置文件
- **日志系统**: 完整的日志记录功能

## 技术栈

- **GUI框架**: PySide6 (Qt6)
- **数据验证**: Pydantic v2
- **类型检查**: Beartype
- **数据库**: MySQL + SQLAlchemy 2.0
- **异步支持**: asyncio + aiohttp
- **HTTP客户端**: aiohttp
- **配置管理**: python-dotenv

## 项目结构

```
mvc_framework/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖管理
├── .env.example           # 配置文件示例
├── README.md              # 项目文档
├── config/
│   └── settings.py        # 配置管理
├── models/                # 数据模型层
│   ├── base_model.py      # 基础模型类
│   ├── user_model.py      # 用户业务模型
│   └── database_models.py # 数据库模型
├── views/                 # 视图层
│   ├── main_window.py     # 主窗口
│   ├── dialogs/           # 对话框
│   └── widgets/           # 自定义组件
├── controllers/           # 控制器层
│   └── main_controller.py # 主控制器
├── services/              # 业务服务层
│   ├── user_service.py    # 用户服务
│   └── data_service.py    # 数据服务
├── repositories/          # 数据访问层
│   ├── base_repository.py # 基础仓储
│   ├── api_client.py      # API客户端
│   └── database.py        # 数据库访问
├── workers/               # 工作器层
│   ├── async_worker.py    # 异步工作器
│   └── thread_worker.py   # 线程工作器
├── utils/                 # 工具类
└── resources/             # 资源文件
    └── styles/            # 样式文件
```

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

1. 安装并启动MySQL服务器
2. 创建数据库：
   ```sql
   CREATE DATABASE mvc_framework CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 3. 配置环境变量

1. 复制配置文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，配置数据库连接信息：
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   DB_DATABASE=mvc_framework
   ```

### 4. 运行应用程序

```bash
python main.py
```

## 架构说明

### MVC架构

- **Model层**: 负责数据模型定义、验证和业务逻辑
- **View层**: 负责用户界面展示和用户交互
- **Controller层**: 负责协调Model和View，处理用户操作

### 分层架构

1. **Presentation Layer (表示层)**
   - Views: 用户界面组件
   - Controllers: 用户交互处理

2. **Business Layer (业务层)**
   - Services: 业务逻辑处理
   - Models: 业务数据模型

3. **Data Access Layer (数据访问层)**
   - Repositories: 数据访问抽象
   - Database Models: 数据库映射

4. **Infrastructure Layer (基础设施层)**
   - Workers: 异步/线程处理
   - Utils: 工具类和辅助功能

### 异步处理

框架支持两种异步处理方式：

1. **异步协程**: 使用asyncio处理I/O密集型任务
2. **多线程**: 使用QThread处理CPU密集型任务

### 数据流向

```
User Input → View → Controller → Service → Repository → Database/API
                                    ↓
User Interface ← View ← Controller ← Service (with progress callbacks)
```

## 使用示例

### 创建新的业务模型

```python
from models.base_model import BaseDataModel
from pydantic import Field
from beartype import beartype

class ProductModel(BaseDataModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(...)
    
    @beartype
    def calculate_tax(self, tax_rate: float) -> float:
        return self.price * tax_rate
```

### 创建服务类

```python
from services.base_service import BaseService
from beartype import beartype

class ProductService(BaseService):
    @beartype
    async def create_product(self, product_data: dict) -> ProductModel:
        # 验证数据
        product = ProductModel(**product_data)
        
        # 保存到数据库
        saved_product = await self.repository.create(product)
        
        return saved_product
```

### 添加异步任务

```python
# 在控制器中
async def process_products():
    products = await self.product_service.get_all_products()
    # 处理产品数据
    return processed_data

# 提交异步任务
self.async_task_manager.queue_task(
    task_id="process_products",
    coroutine=process_products(),
    priority=1
)
```

## 扩展指南

### 添加新的视图

1. 在 `views/` 目录下创建新的视图类
2. 继承适当的Qt基类 (QWidget, QDialog等)
3. 在控制器中连接视图信号

### 添加新的服务

1. 在 `services/` 目录下创建服务类
2. 实现业务逻辑方法
3. 在控制器中注入和使用服务

### 添加新的数据模型

1. 在 `models/` 目录下定义业务模型
2. 在 `models/database_models.py` 中定义数据库模型
3. 创建对应的仓储类

## 开发工具

推荐使用以下工具进行开发：

- **IDE**: PyCharm, VS Code
- **数据库工具**: MySQL Workbench, DBeaver
- **API测试**: Postman, Insomnia
- **代码格式化**: Black
- **类型检查**: mypy

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个框架。

## 更新日志

### v1.0.0
- 初始版本发布
- 完整的MVC架构实现
- 异步和多线程支持
- MySQL数据库集成
- 现代化UI设计
