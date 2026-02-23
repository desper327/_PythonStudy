# maya_server.py（线程安全版）
import threading
import socket
import maya.cmds as cmds

HOST, PORT = "localhost", 999

def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data: break
            # 将Maya操作提交到主线程执行
            result = str(eval(data))#cmds.evalDeferred(data, ret=True)  # 关键点：evalDeferred
            conn.sendall(result.encode())
        except Exception as e:
            conn.sendall(f"Error: {str(e)}".encode())

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

# 在独立线程中运行Socket服务器
threading.Thread(target=start_server, daemon=True).start()