# FastAPI 表格生成器

这是一个使用 FastAPI 和 Jinja2 模板引擎创建的简单 Web 应用程序，用于生成和显示表格。

## 功能

- 显示静态表格
- 动态生成表格（可自定义行数和列数）
- 响应式设计，适配桌面和移动设备

## 安装

1. 确保你已安装 Python 3.7 或更高版本

2. 克隆此存储库：

```
git clone <repository-url>
cd <repository-directory>
```

3. 安装所需依赖：

```
pip install -r requirements.txt
```

## 运行应用程序

1. 使用以下命令启动服务器：

```
python main.py
```

2. 在浏览器中访问：`http://localhost:8000`

## 项目结构

```
├── main.py              # FastAPI 应用程序入口
├── requirements.txt     # 项目依赖
├── static/              # 静态文件
│   └── css/
│       └── styles.css   # 样式表
└── templates/           # Jinja2 模板
    ├── base.html        # 基础模板（布局）
    ├── index.html       # 首页模板（静态表格）
    └── dynamic_table.html  # 动态表格模板
```

## 技术栈

- FastAPI：现代高性能 Web 框架
- Jinja2：强大的模板引擎
- Uvicorn：ASGI 服务器

## 自定义

可以修改 `main.py` 文件中的数据结构来自定义表格内容。

## 许可证

[MIT](LICENSE) 