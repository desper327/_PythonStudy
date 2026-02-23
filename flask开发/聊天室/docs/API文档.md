# API 接口文档

## 基础信息

**服务器地址**: `http://localhost:5000`

**响应格式**: JSON

**统一响应结构**:
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

**状态码说明**:
- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未认证或认证失败
- `403`: 无权限
- `404`: 资源不存在
- `500`: 服务器错误

---

## 认证相关

### 1. 用户注册

**接口**: `POST /api/auth/register`

**请求参数**:
```json
{
  "username": "testuser",
  "password": "123456",
  "nickname": "测试用户",
  "email": "test@example.com"  // 可选
}
```

**成功响应** (201):
```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "user_id": 1,
    "username": "testuser"
  }
}
```

**错误响应**:
```json
{
  "code": 400,
  "message": "用户名已存在",
  "data": null
}
```

---

### 2. 用户登录

**接口**: `POST /api/auth/login`

**请求参数**:
```json
{
  "username": "testuser",
  "password": "123456"
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "testuser",
      "nickname": "测试用户",
      "email": "test@example.com",
      "avatar": null,
      "status": "active",
      "created_at": "2025-10-18T10:00:00"
    }
  }
}
```

---

## 用户相关

### 3. 获取当前用户信息

**接口**: `GET /api/users/me`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "nickname": "测试用户",
    "email": "test@example.com",
    "avatar": null,
    "status": "active",
    "created_at": "2025-10-18T10:00:00"
  }
}
```

---

### 4. 更新用户信息

**接口**: `PUT /api/users/me`

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "nickname": "新昵称",       // 可选
  "email": "new@example.com", // 可选
  "avatar": "http://..."      // 可选
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    // 更新后的用户信息
  }
}
```

---

### 5. 修改密码

**接口**: `PUT /api/users/me/password`

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "old_password": "123456",
  "new_password": "654321"
}
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

---

### 6. 搜索用户

**接口**: `GET /api/users/search?keyword=<关键词>`

**请求头**:
```
Authorization: Bearer <token>
```

**Query参数**:
- `keyword`: 搜索关键词（用户名或昵称）

**成功响应** (200):
```json
{
  "code": 200,
  "message": "搜索成功",
  "data": {
    "users": [
      {
        "id": 2,
        "username": "user1",
        "nickname": "张三",
        "avatar": null,
        "status": "active",
        "created_at": "2025-10-18T10:00:00"
      }
    ],
    "count": 1
  }
}
```

---

### 7. 获取指定用户信息

**接口**: `GET /api/users/<user_id>`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 2,
    "username": "user1",
    "nickname": "张三",
    "avatar": null,
    "status": "active",
    "created_at": "2025-10-18T10:00:00"
  }
}
```

---

## 群组相关

### 8. 创建群组

**接口**: `POST /api/groups`

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "name": "技术交流群",
  "description": "讨论技术问题",  // 可选
  "type": "public"               // public 或 private
}
```

**成功响应** (201):
```json
{
  "code": 201,
  "message": "群组创建成功",
  "data": {
    "id": 1,
    "name": "技术交流群",
    "description": "讨论技术问题",
    "type": "public",
    "owner_id": 1,
    "owner_name": "管理员",
    "member_count": 1,
    "created_at": "2025-10-18T10:00:00"
  }
}
```

---

### 9. 获取我的群组列表

**接口**: `GET /api/groups`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "groups": [
      {
        "id": 1,
        "name": "技术交流群",
        "description": "讨论技术问题",
        "type": "public",
        "owner_id": 1,
        "owner_name": "管理员",
        "member_count": 5,
        "created_at": "2025-10-18T10:00:00"
      }
    ],
    "count": 1
  }
}
```

---

### 10. 获取公开群组列表

**接口**: `GET /api/groups/public`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "groups": [
      // 所有公开群组列表
    ],
    "count": 10
  }
}
```

---

### 11. 获取群组详情

**接口**: `GET /api/groups/<group_id>`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 1,
    "name": "技术交流群",
    "description": "讨论技术问题",
    "type": "public",
    "owner_id": 1,
    "owner_name": "管理员",
    "member_count": 5,
    "created_at": "2025-10-18T10:00:00",
    "members": [
      {
        "id": 1,
        "group_id": 1,
        "user_id": 1,
        "username": "admin",
        "nickname": "管理员",
        "avatar": null,
        "role": "owner",
        "joined_at": "2025-10-18T10:00:00"
      }
    ]
  }
}
```

---

### 12. 加入群组

**接口**: `POST /api/groups/<group_id>/join`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "加入群组成功",
  "data": {
    "id": 2,
    "group_id": 1,
    "user_id": 2,
    "username": "user1",
    "nickname": "张三",
    "avatar": null,
    "role": "member",
    "joined_at": "2025-10-18T10:00:00"
  }
}
```

---

### 13. 退出群组

**接口**: `DELETE /api/groups/<group_id>/leave`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "退出群组成功",
  "data": null
}
```

---

### 14. 获取群组成员列表

**接口**: `GET /api/groups/<group_id>/members`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "members": [
      {
        "id": 1,
        "group_id": 1,
        "user_id": 1,
        "username": "admin",
        "nickname": "管理员",
        "avatar": null,
        "role": "owner",
        "joined_at": "2025-10-18T10:00:00"
      }
    ],
    "count": 1
  }
}
```

---

### 15. 踢出成员

**接口**: `DELETE /api/groups/<group_id>/members/<user_id>`

**请求头**:
```
Authorization: Bearer <token>
```

**权限**: 仅群主和管理员

**成功响应** (200):
```json
{
  "code": 200,
  "message": "成员已被踢出",
  "data": null
}
```

---

## 消息相关

### 16. 获取私聊消息历史

**接口**: `GET /api/messages/private/<user_id>?page=1&per_page=50`

**请求头**:
```
Authorization: Bearer <token>
```

**Query参数**:
- `page`: 页码（默认1）
- `per_page`: 每页数量（默认50，最大100）

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "messages": [
      {
        "id": 1,
        "sender_id": 1,
        "sender_name": "管理员",
        "sender_avatar": null,
        "receiver_id": 2,
        "receiver_name": "张三",
        "group_id": null,
        "group_name": null,
        "message_type": "text",
        "content": "你好！",
        "is_read": false,
        "created_at": "2025-10-18T10:00:00"
      }
    ],
    "total": 100,
    "page": 1,
    "per_page": 50,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### 17. 获取群组消息历史

**接口**: `GET /api/messages/group/<group_id>?page=1&per_page=50`

**请求头**:
```
Authorization: Bearer <token>
```

**Query参数**:
- `page`: 页码（默认1）
- `per_page`: 每页数量（默认50，最大100）

**成功响应** (200):
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "messages": [
      {
        "id": 1,
        "sender_id": 1,
        "sender_name": "管理员",
        "sender_avatar": null,
        "receiver_id": null,
        "receiver_name": null,
        "group_id": 1,
        "group_name": "技术交流群",
        "message_type": "text",
        "content": "大家好！",
        "is_read": false,
        "created_at": "2025-10-18T10:00:00"
      }
    ],
    "total": 50,
    "page": 1,
    "per_page": 50,
    "has_next": false,
    "has_prev": false
  }
}
```

---

## WebSocket 事件

### 连接和认证

#### 1. 连接服务器

**事件**: `connect`

连接成功后，服务器会发送 `connected` 事件。

---

#### 2. 认证

**客户端发送**: `authenticate`

**数据格式**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**服务器响应**: `authenticated`

**数据格式**:
```json
{
  "user_id": 1,
  "username": "testuser",
  "message": "认证成功"
}
```

---

### 消息发送

#### 3. 发送私聊消息

**客户端发送**: `send_private_message`

**数据格式**:
```json
{
  "receiver_id": 2,
  "content": "你好！"
}
```

**服务器响应**: `message_sent`

**数据格式**:
```json
{
  "message_id": 1,
  "message": {
    "id": 1,
    "sender_id": 1,
    "sender_name": "管理员",
    "receiver_id": 2,
    "receiver_name": "张三",
    "content": "你好！",
    "created_at": "2025-10-18T10:00:00"
  }
}
```

**接收者收到**: `new_private_message`

---

#### 4. 发送群组消息

**客户端发送**: `send_group_message`

**数据格式**:
```json
{
  "group_id": 1,
  "content": "大家好！"
}
```

**服务器响应**: `message_sent`

**群组成员收到**: `new_group_message`

---

### 群组房间

#### 5. 加入群组房间

**客户端发送**: `join_group_room`

**数据格式**:
```json
{
  "group_id": 1
}
```

**服务器响应**: `joined_group_room`

---

#### 6. 离开群组房间

**客户端发送**: `leave_group_room`

**数据格式**:
```json
{
  "group_id": 1
}
```

**服务器响应**: `left_group_room`

---

### 在线状态

#### 7. 用户上线通知

**服务器广播**: `user_online`

**数据格式**:
```json
{
  "user_id": 1,
  "username": "testuser"
}
```

---

#### 8. 用户下线通知

**服务器广播**: `user_offline`

**数据格式**:
```json
{
  "user_id": 1
}
```

---

### 错误处理

#### 9. 错误通知

**服务器发送**: `error`

**数据格式**:
```json
{
  "message": "错误描述"
}
```

---

## 错误码说明

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求参数格式和内容 |
| 401 | 未认证或Token无效 | 重新登录获取Token |
| 403 | 无权限 | 检查用户权限 |
| 404 | 资源不存在 | 检查资源ID是否正确 |
| 500 | 服务器内部错误 | 联系管理员或查看服务器日志 |

---

## 使用示例

### Python 示例

```python
import requests

# 1. 登录
response = requests.post('http://localhost:5000/api/auth/login', json={
    'username': 'admin',
    'password': '123456'
})
data = response.json()
token = data['data']['token']

# 2. 获取用户信息
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/users/me', headers=headers)
print(response.json())

# 3. 搜索用户
response = requests.get(
    'http://localhost:5000/api/users/search',
    params={'keyword': '张三'},
    headers=headers
)
print(response.json())
```

---

## 附录

### Token 格式

JWT Token 包含以下信息：
- `user_id`: 用户ID
- `username`: 用户名
- `exp`: 过期时间
- `iat`: 签发时间

### 数据库表关系

- `users`: 用户表
- `groups`: 群组表
- `group_members`: 群组成员表（关联用户和群组）
- `messages`: 消息表（支持私聊和群聊）

### 注意事项

1. 所有需要认证的接口都需要在请求头中携带 `Authorization: Bearer <token>`
2. Token 默认有效期为 24 小时
3. WebSocket 连接后必须先进行认证才能发送消息
4. 消息内容最大长度为 10000 字符
5. 分页查询最大每页数量为 100 条
