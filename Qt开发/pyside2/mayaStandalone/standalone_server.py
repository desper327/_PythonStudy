#coding=utf-8

import sys
import socket
import maya.standalone
import maya.cmds as cmds
import json

#sys.path.append("F:\Study\BaiduSyncdisk\MT_MayaPlugin\MT_plugin\scripts\Func")
#import AutoAniExportNC_Bat

#import createMod

def initialize_maya():
    """Initialize the Maya standalone environment."""
    maya.standalone.initialize(name='python')

def get_root_nodes():
    all_transforms = cmds.ls(type='transform')
    root_nodes = ''
    for transform in all_transforms:
        if not cmds.listRelatives(transform, parent=True): #and transform not in ['persp','side', 'top', 'front']:
            root_nodes += transform +'\n'
    return root_nodes

def open_maya_file(file_path):
    """Open a Maya file in the current session."""
    # if cmds.file(query=True, modified=True):
    #     cmds.file(force=True, new=True)
    cmds.file(file_path, open=True, force=True)
    return "Opened file: {}".format(file_path)

def export_bone_anim(root_bone):
    a=''

    a+=str(root_bone)

    root_bone = root_bone.strip()
    try:
        a+='ggggggggggggggggggggggg'
        cmds.select(root_bone)
        a+='HHHHHHHHHH'
        #createMod.createModel()
        #createMod.saveFile()
        #AutoAniExportNC_Bat.ExportAni_bat()
        a+='ffffffffffffffffffffff'
        return "Export bone anim successfully!"
    except Exception as e:
        return str(e)+a
        
        
    

def handle_request(request):
    """Handle a command request from the client."""
    command = request.get("command")
    
    if command == "open_file":
        file_path = request.get("file_path")
        response = open_maya_file(file_path)
    elif command == "get_root_nodes":
        response = get_root_nodes()
    elif command == "export_bone_anim":
        root_bone_node=request.get("root_bone_node")
        response = export_bone_anim(root_bone_node)
    else:
        response = "Unknown command: {}".format(command)

    return response

def start_server():
    """Start a TCP server to receive commands from the PyQt client."""
    initialize_maya()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)
    print("Server is listening on port 12345...")

    while True:
        client_socket, addr = server_socket.accept()
        print("Connected to {}".format(addr))
        
        # Receive the data and decode JSON
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break

        request = json.loads(data)
        response = handle_request(request)
        
        # Send response back to client
        response_data = json.dumps(response)
        client_socket.sendall(response_data.encode("utf-8"))
        client_socket.close()

if __name__ == "__main__":
    start_server()

