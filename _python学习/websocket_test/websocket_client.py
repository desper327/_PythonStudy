#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets
import json
import datetime
import sys

async def send_message(websocket, message):
    """发送消息到服务器"""
    try:
        # 构造消息
        data = {
            "message": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "broadcast": True  # 设置为True以广播消息
        }
        
        # 发送JSON消息
        await websocket.send(json.dumps(data))
        
        # 等待并打印服务器响应
        response = await websocket.recv()
        try:
            # 尝试解析JSON响应
            response_data = json.loads(response)
            print(f"服务器响应: {json.dumps(response_data, indent=2)}")
        except json.JSONDecodeError:
            # 如果不是JSON格式，直接打印文本
            print(f"服务器响应: {response}")
            
    except websockets.exceptions.ConnectionClosed:
        print("连接已关闭")
        sys.exit(1)

async def receive_messages(websocket):
    """接收服务器消息"""
    try:
        while True:
            message = await websocket.recv()
            try:
                # 尝试解析JSON消息
                data = json.loads(message)
                print(f"收到消息: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError:
                # 如果不是JSON格式，直接打印文本
                print(f"收到消息: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("连接已关闭")
        sys.exit(1)

async def main():
    # WebSocket服务器地址
    uri = "ws://localhost:8765"
    
    try:
        # 连接到WebSocket服务器
        async with websockets.connect(uri) as websocket:
            print(f"已连接到服务器: {uri}")
            
            # 创建接收消息的任务
            receive_task = asyncio.create_task(receive_messages(websocket))
            
            # 持续发送消息
            while True:
                # 从控制台获取输入
                message = input("请输入要发送的消息（输入'exit'退出）: ")
                
                if message.lower() == 'exit':
                    break
                
                # 发送消息
                await send_message(websocket, message)
            
            # 取消接收消息的任务
            receive_task.cancel()
            
    except websockets.exceptions.ConnectionRefused:
        print("无法连接到服务器，请确保服务器正在运行")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n程序已通过键盘中断停止")
        sys.exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已通过键盘中断停止")
        sys.exit(0)