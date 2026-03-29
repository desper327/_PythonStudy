# 🔍 Python Tracer - 运行时调用追踪器

一个用于追踪Python程序运行时函数调用、变量变化的工具，并生成美观的Markdown报告。

## ✨ 功能特性

- 📦 **函数调用追踪** - 记录函数名、所属模块/包、调用时间、执行时长
- 🌲 **调用树生成** - 可视化展示函数调用的层级关系
- 🔄 **变量变化追踪** - 追踪函数内所有局部变量的创建和修改
- ⚡ **异步支持** - 完整支持 `async/await` 异步函数
- 📄 **MD报告生成** - 自动生成详细的Markdown格式报告

## 📁 项目结构

```
tracer/
├── __init__.py          # 包入口
├── core.py              # 核心追踪逻辑
├── decorators.py        # 装饰器实现
├── models.py            # 数据模型定义
├── report_generator.py  # MD报告生成器
└── variable_tracker.py  # 变量追踪器

example.py               # 使用示例
README.md                # 说明文档
```

## 🚀 快速开始

### 方式1: 使用装饰器（推荐）

```python
from tracer import trace, Tracer

@trace
def calculate(x, y):
    result = x + y
    doubled = result * 2
    return doubled

@trace
async def async_operation():
    await some_task()
    return result

# 开始追踪
Tracer.start()

# 调用函数
calculate(10, 20)

# 停止并生成报告
Tracer.stop()
Tracer.generate_report("trace_report.md")
```

### 方式2: 自动追踪模式

如果只使用 `@trace` 装饰器而不手动调用 `Tracer.start()`，追踪器会自动开始和停止：

```python
from tracer import trace, Tracer

@trace
def my_function():
    # 函数体
    pass

# 直接调用，追踪自动进行
my_function()

# 手动生成报告
Tracer.generate_report()
```

### 方式3: 禁用变量追踪

如果不需要追踪变量变化（提升性能）：

```python
@trace(track_variables=False)
def fast_function():
    pass
```

## 📊 生成的报告内容

生成的 `trace_report.md` 包含以下内容：

### 1. 执行摘要
- 追踪时间范围
- 总调用次数
- 同步/异步调用统计
- 追踪的模块和函数列表

### 2. 调用树
```
└── main() (150.00ms)
    ├── calculate_sum(10, 20) (0.50ms)
    ├── calculate_product(10, 20) (0.30ms)
    └── ⚡async_process() (200.00ms)
        ├── ⚡async_fetch_data(...) (100.00ms)
        └── ⚡async_fetch_data(...) (100.00ms)
```

### 3. 调用时序表
| 序号 | 时间 | 函数 | 模块 | 耗时 | 类型 | 状态 |
|------|------|------|------|------|------|------|
| 1 | 10:00:00.001 | main | __main__ | 150ms | 同步 | ✅ 成功 |

### 4. 变量变化记录
| 变量名 | 操作 | 旧值 | 新值 | 行号 |
|--------|------|------|------|------|
| result | 创建 | - | 30 | 5 |
| doubled | 创建 | - | 60 | 6 |

### 5. 详细调用日志
每个函数调用的完整信息，包括参数、返回值、执行时间等。

## 🔧 API 参考

### Tracer 类

| 方法 | 描述 |
|------|------|
| `Tracer.start(session_id=None)` | 开始追踪会话 |
| `Tracer.stop()` | 停止追踪会话 |
| `Tracer.is_enabled()` | 检查是否正在追踪 |
| `Tracer.get_session()` | 获取当前追踪会话 |
| `Tracer.reset()` | 重置追踪器 |
| `Tracer.generate_report(path)` | 生成MD报告 |

### 装饰器

| 装饰器 | 描述 |
|--------|------|
| `@trace` | 追踪函数调用 |
| `@trace(track_variables=False)` | 追踪但不记录变量变化 |
| `@trace_async` | 异步函数追踪（语义化别名） |
| `@no_trace` | 标记函数不进行追踪 |

## 📝 运行示例

```bash
python example.py
```

运行后会生成 `trace_report.md` 文件，可以用任何Markdown阅读器查看。

## ⚠️ 注意事项

1. **性能影响**: 追踪会增加一定的运行时开销，建议仅在开发/调试时使用
2. **变量追踪限制**: 异步函数中的变量追踪可能不完整
3. **递归函数**: 对于递归函数，每次调用都会被记录，可能产生大量数据

## 📄 License

MIT License
