# Python 聊天软件案例说明

## 项目结构
- server.py —— 聊天服务器后端，负责多客户端消息转发
- client.py —— 聊天客户端前端，PyQt5桌面界面
- requirements.txt —— 依赖说明（仅需PyQt5）

## 运行方式
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 启动服务器（新终端）：
   ```bash
   python server.py
   ```
3. 启动客户端（可多开）：
   ```bash
   python client.py
   ```

## 技术要点
- Python socket 网络编程（TCP）
- 多线程实现并发聊天
- PyQt5 图形界面开发
- 前后端分离与消息通信

## 学习建议
- 可尝试扩展：昵称设置、消息时间戳、历史记录、群聊/私聊等
- 可阅读和修改源码，体会事件驱动、信号槽、socket通信等机制

如需更详细讲解或代码注释，欢迎随时提问！
