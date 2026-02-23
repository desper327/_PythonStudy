#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets
import json
import datetime

# 存储连接的客户端
connected_clients = set()

async def handle_client(websocket, path):
    """处理客户端连接"""
    # 将新客户端添加到集合
    connected_clients.add(websocket)
    client_id = id(websocket)
    print(f"客户端 {client_id} 已连接。当前连接数: {len(connected_clients)}")
    
    try:
        # 持续监听客户端消息
        async for message in websocket:
            try:
                # 尝试解析JSON消息
                data = json.loads(message)
                print(f"收到来自客户端 {client_id} 的消息: {data}")
                
                # 构造响应
                response = {
                    "status": "success",
                    "message": f"服务器已收到您的消息",
                    "original_message": data,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
                # 发送响应回客户端
                await websocket.send(json.dumps(response))
                
                # 广播消息给所有其他客户端
                if "broadcast" in data and data["broadcast"]:
                    await broadcast_message(websocket, data)
                
            except json.JSONDecodeError:
                # 如果不是JSON格式，直接返回文本响应
                print(f"收到来自客户端 {client_id} 的文本消息: {message}")
                await websocket.send(f"服务器收到文本消息: {message}")
    
    except websockets.exceptions.ConnectionClosed as e:
        print(f"客户端 {client_id} 连接已关闭: {e}")
    
    finally:
        # 客户端断开连接时从集合中移除
        connected_clients.remove(websocket)
        print(f"客户端 {client_id} 已断开连接。当前连接数: {len(connected_clients)}")

async def broadcast_message(sender, message):
    """广播消息给所有客户端（除了发送者）"""
    broadcast_data = {
        "type": "broadcast",
        "source_client_id": id(sender),
        "message": message,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    broadcast_json = json.dumps(broadcast_data)
    
    # 发送给除了发送者以外的所有客户端
    for client in connected_clients:
        if client != sender:
            try:
                await client.send(broadcast_json)
            except websockets.exceptions.ConnectionClosed:
                # 如果发送失败，客户端可能已断开连接
                pass

async def main():
    # 启动WebSocket服务器
    server_host = "localhost"
    server_port = 8765
    
    server = await websockets.serve(
        handle_client, 
        server_host, 
        server_port
    )
    
    print(f"WebSocket服务器已启动，监听地址: ws://{server_host}:{server_port}")
    
    # 保持服务器运行
    await server.wait_closed()

if __name__ == "__main__":
    try:
        # 启动事件循环
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器已通过键盘中断停止")