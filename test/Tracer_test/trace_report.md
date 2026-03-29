# 🔍 Python 运行追踪报告

> 生成时间: 2026-03-27 11:11:29
> 会话ID: `ada48fbe`

---

## 📊 执行摘要

### 基本信息

| 指标 | 值 |
|------|-----|
| 追踪开始时间 | 2026-03-27 11:11:29.201 |
| 追踪结束时间 | 2026-03-27 11:11:29.203 |
| 总执行耗时 | 1.50 ms |
| 总函数调用次数 | 8 |
| 同步调用次数 | 8 |
| 异步调用次数 | 0 |
| 异常次数 | 0 |

### 追踪的模块

- `__main__`

### 追踪的函数

- `__main__.calculate_product`
- `__main__.calculate_sum`
- `__main__.helper`
- `__main__.main`
- `__main__.nested_call`
- `__main__.process_numbers`

## 🌲 调用树

```
└── main() (0.21ms) 
    ├── process_numbers(10, 20) (0.06ms) 
    │   ├── calculate_sum(10, 20) (0.01ms) 
    │   └── calculate_product(10, 20) (0.01ms) 
    └── nested_call() (0.06ms) 
        ├── helper(5) (0.01ms) 
        ├── helper(10) (0.02ms) 
        └── helper(20) (0.01ms) 
```

## 📈 调用时序

| 序号 | 时间 | 函数 | 模块 | 耗时 | 类型 | 状态 |
|------|------|------|------|------|------|------|
| 1 | 11:11:29.202 | `main` | __main__ | 0.21ms | 同步 | ✅ 成功 |
| 2 | 11:11:29.203 | `　process_numbers` | __main__ | 0.06ms | 同步 | ✅ 成功 |
| 3 | 11:11:29.203 | `　　calculate_sum` | __main__ | 0.01ms | 同步 | ✅ 成功 |
| 4 | 11:11:29.203 | `　　calculate_product` | __main__ | 0.01ms | 同步 | ✅ 成功 |
| 5 | 11:11:29.203 | `　nested_call` | __main__ | 0.06ms | 同步 | ✅ 成功 |
| 6 | 11:11:29.203 | `　　helper` | __main__ | 0.01ms | 同步 | ✅ 成功 |
| 7 | 11:11:29.203 | `　　helper` | __main__ | 0.02ms | 同步 | ✅ 成功 |
| 8 | 11:11:29.203 | `　　helper` | __main__ | 0.01ms | 同步 | ✅ 成功 |

## 📝 详细调用日志

### 1. `__main__.main()`

<details>
<summary>调用详情 (ID: 06bce786)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `06bce786` |
| 函数名 | `main` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 52 |
| 调用深度 | 0 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.202 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.21 ms |

**输入参数:**

```python
# 无参数
```

**返回值:**

```python
return None
```

</details>

### 2. `__main__.process_numbers()`

<details>
<summary>调用详情 (ID: d6d45c35)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `d6d45c35` |
| 函数名 | `process_numbers` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 29 |
| 调用深度 | 1 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.203 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.06 ms |
| 父调用 | `main` (06bce786) |

**输入参数:**

```python
args = (10, 20)
```

**返回值:**

```python
return {'sum': 30, 'product': 200, 'average': 15.0}
```

</details>

### 3. `__main__.calculate_sum()`

<details>
<summary>调用详情 (ID: 5c296700)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `5c296700` |
| 函数名 | `calculate_sum` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 19 |
| 调用深度 | 2 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.203 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.01 ms |
| 父调用 | `process_numbers` (d6d45c35) |

**输入参数:**

```python
args = (10, 20)
```

**返回值:**

```python
return 30
```

</details>

### 4. `__main__.calculate_product()`

<details>
<summary>调用详情 (ID: 85554697)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `85554697` |
| 函数名 | `calculate_product` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 24 |
| 调用深度 | 2 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.203 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.01 ms |
| 父调用 | `process_numbers` (d6d45c35) |

**输入参数:**

```python
args = (10, 20)
```

**返回值:**

```python
return 200
```

</details>

### 5. `__main__.nested_call()`

<details>
<summary>调用详情 (ID: 4f852876)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `4f852876` |
| 函数名 | `nested_call` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 45 |
| 调用深度 | 1 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.203 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.06 ms |
| 父调用 | `main` (06bce786) |

**输入参数:**

```python
# 无参数
```

**返回值:**

```python
return 40
```

</details>

### 6. `__main__.helper()`

<details>
<summary>调用详情 (ID: f719fcdf)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `f719fcdf` |
| 函数名 | `helper` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 40 |
| 调用深度 | 2 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.203 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.01 ms |
| 父调用 | `nested_call` (4f852876) |

**输入参数:**

```python
args = (5,)
```

**返回值:**

```python
return 10
```

</details>

### 7. `__main__.helper()`

<details>
<summary>调用详情 (ID: 462fb3fb)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `462fb3fb` |
| 函数名 | `helper` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 40 |
| 调用深度 | 2 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.203 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.02 ms |
| 父调用 | `nested_call` (4f852876) |

**输入参数:**

```python
args = (10,)
```

**返回值:**

```python
return 20
```

</details>

### 8. `__main__.helper()`

<details>
<summary>调用详情 (ID: ada06cc8)</summary>

| 属性 | 值 |
|------|-----|
| 调用ID | `ada06cc8` |
| 函数名 | `helper` |
| 模块 | `__main__` |
| 文件 | `d:\ZY\python\_PipelineDev\test\Tracer_test\example.py` |
| 定义行号 | 40 |
| 调用深度 | 2 |
| 类型 | 同步 |
| 开始时间 | 11:11:29.203 |
| 结束时间 | 11:11:29.203 |
| 执行耗时 | 0.01 ms |
| 父调用 | `nested_call` (4f852876) |

**输入参数:**

```python
args = (20,)
```

**返回值:**

```python
return 40
```

</details>

---

*此报告由 Python Tracer 自动生成*

*报告生成时间: 2026-03-27 11:11:29*
