#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单的WebSocket示例
包含一个简单的服务器和客户端
"""

import asyncio
import websockets
import json
import datetime
import sys
import threading
import time

# ============================== 服务器部分 ==============================

# 存储连接的客户端
connected_clients = set()

async def server_handler(websocket, path):
    """处理客户端连接的服务器处理函数"""
    # 将新客户端添加到集合
    connected_clients.add(websocket)
    client_id = id(websocket)
    print(f"[服务器] 客户端 {client_id} 已连接。当前连接数: {len(connected_clients)}")
    
    try:
        # 持续监听客户端消息
        async for message in websocket:
            print(f"[服务器] 收到消息: {message}")
            
            # 发送响应回客户端
            response = f"服务器已收到: {message} (时间: {datetime.datetime.now().strftime('%H:%M:%S')})"
            await websocket.send(response)
    
    except websockets.exceptions.ConnectionClosed:
        print(f"[服务器] 客户端 {client_id} 连接已关闭")
    
    finally:
        # 客户端断开连接时从集合中移除
        connected_clients.remove(websocket)
        print(f"[服务器] 客户端 {client_id} 已断开连接。当前连接数: {len(connected_clients)}")

async def start_server(host="localhost", port=8765):
    """启动WebSocket服务器"""
    server = await websockets.serve(server_handler, host, port)
    print(f"[服务器] WebSocket服务器已启动，监听地址: ws://{host}:{port}")
    await server.wait_closed()

# ============================== 客户端部分 ==============================

async def client_handler():
    """WebSocket客户端处理函数"""
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[客户端] 已连接到服务器: {uri}")
            
            for i in range(5):
                # 发送消息
                message = f"这是客户端消息 #{i+1}"
                print(f"[客户端] 发送: {message}")
                await websocket.send(message)
                
                # 接收服务器响应
                response = await websocket.recv()
                print(f"[客户端] 收到: {response}")
                
                # 等待一秒
                await asyncio.sleep(1)
                
            print("[客户端] 测试完成，断开连接")
            
    except websockets.exceptions.ConnectionRefused:
        print("[客户端] 无法连接到服务器，请确保服务器正在运行")

# ============================== 主程序 ==============================

def run_server():
    """在单独的线程中运行服务器"""
    asyncio.run(start_server())

def run_client():
    """运行客户端"""
    # 等待服务器启动
    time.sleep(1)
    asyncio.run(client_handler())

def main():
    """主函数，同时运行服务器和客户端"""
    # 创建并启动服务器线程
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # 设置为守护线程，这样当主线程退出时，服务器线程也会退出
    server_thread.start()
    
    try:
        # 等待服务器启动
        time.sleep(1)
        
        # 运行客户端
        run_client()
        
        # 等待一段时间，让用户看到输出
        print("\n演示完成。按Ctrl+C退出...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n程序已通过键盘中断停止")
        sys.exit(0)

if __name__ == "__main__":
    main()