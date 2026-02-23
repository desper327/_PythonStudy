# 聊天服务器后端（server.py）
# 使用 FastAPI + python-socketio 实现 SocketIO 聊天服务

import socketio
from fastapi import FastAPI
import uvicorn

# 创建一个 Async Socket.IO 服务器对象，允许跨域
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# 创建 FastAPI 应用
app = FastAPI()

# 将 Socket.IO 服务器挂载到 FastAPI 应用上
# 这样同一个服务既能处理 HTTP 请求，也能处理 SocketIO 实时通信
app.mount('/', socketio.ASGIApp(sio, other_asgi_app=app))

# 记录已连接的客户端 sid
connected_clients = set()

@sio.event
async def connect(sid, environ):
    """
    新客户端连接时自动调用（异步）。
    sid: session id，唯一标识每个客户端
    environ: 客户端请求的环境信息
    """
    print(f'客户端已连接: {sid}')
    connected_clients.add(sid)
    # 广播新用户加入消息
    await sio.emit('message', f'用户 {sid[:8]} 已加入聊天')

@sio.event
async def disconnect(sid):
    """
    客户端断开连接时自动调用（异步）。
    """
    print(f'客户端已断开: {sid}')
    connected_clients.discard(sid)
    await sio.emit('message', f'用户 {sid[:8]} 已离开聊天')

@sio.event
async def message(sid, data):
    """
    客户端发送 'message' 事件时自动调用（异步）。
    data: 客户端发来的消息内容
    """
    print(f'收到 {sid[:8]} 的消息: {data}')
    # 广播消息到所有客户端
    await sio.emit('message', f'用户 {sid[:8]}: {data}')

if __name__ == '__main__':
    # 使用 uvicorn 启动 FastAPI 应用，监听 5000 端口
    # reload=True 支持热重载，开发时方便
    uvicorn.run('server:app', host='0.0.0.0', port=5000, reload=True)
