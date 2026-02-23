# control.py
import socket

def send_cmd(port, cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", port))
        s.sendall(cmd.encode())
        return s.recv(1024).decode()

# Test command
print(send_cmd(999, "cmds.polyCube()"))

# 控制Houdini
#print(send_cmd(9998, "hou.node('/obj').createNode('geo')"))