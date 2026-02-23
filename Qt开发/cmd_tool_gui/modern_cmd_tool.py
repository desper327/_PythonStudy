# -*- coding: utf-8 -*-
import sys
import os
import json
import subprocess
import locale
import codecs
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTextEdit, QLineEdit, QScrollArea, 
                             QSizePolicy, QFileDialog, QMessageBox,
                             QDialog, QFormLayout, QDialogButtonBox,
                             QTabWidget, QGridLayout, QToolButton, QToolTip,
                             QTabBar, QStylePainter, QStyleOptionTab, QStyle)
from PySide6.QtCore import Qt, QProcess, Signal, Slot, QSize
from PySide6.QtGui import QFont, QIcon, QColor, QPalette, QPainterPath

# 导入样式
from styles import (COLORS, GLOBAL_STYLE, get_tab_style, get_button_style, 
                   get_command_button_style, RUN_BUTTON_STYLE, STOP_BUTTON_STYLE, 
                   CLEAR_BUTTON_STYLE, BROWSE_BUTTON_STYLE, ADD_BUTTON_STYLE, 
                   DELETE_BUTTON_STYLE, DIR_EDIT_STYLE, COMMAND_LABEL_STYLE,LABEL_FONT, 
                   STATUS_LABEL_STYLE, OUTPUT_TEXT_STYLE, darken_color, SIZES)

# 设置Python默认编码为UTF-8
if sys.platform == 'win32':
    # 设置Windows控制台编码为UTF-8
    os.system('chcp 65001')
    # 设置Python的默认编码
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    # 设置区域设置
    try:
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Chinese_China.936')
        except locale.Error:
            pass

class CommandRunner(QProcess):
    """命令执行器，在单独进程中处理命令执行"""
    commandOutput = Signal(str)
    commandError = Signal(str)
    commandFinished = Signal(int, QProcess.ExitStatus)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.readyReadStandardOutput.connect(self.readStandardOutput)
        self.readyReadStandardError.connect(self.readStandardError)
        self.finished.connect(self.onFinished)
        # 设置进程输出编码
        self.setProcessChannelMode(QProcess.MergedChannels)
        
        # 设置进程环境变量
        env = QProcess.systemEnvironment()
        if sys.platform == 'win32':
            env.append("PYTHONIOENCODING=utf-8")
            env.append("LANG=zh_CN.UTF-8")
            env.append("PYTHONLEGACYWINDOWSSTDIO=utf-8")
        self.setEnvironment(env)

    def execute(self, command):
        """执行给定命令"""
        if sys.platform == 'win32':
            # 使用PowerShell而不是cmd，PowerShell默认支持UTF-8
            ps_command = (
                "$OutputEncoding = [System.Text.Encoding]::UTF8; "
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
                "[Console]::InputEncoding = [System.Text.Encoding]::UTF8; "
                "chcp 65001 | Out-Null; "
                f"{command}"
            )
            self.start('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', ps_command])
        else:
            self.start('/bin/bash', ['-c', command])

    def readStandardOutput(self):
        """读取和处理标准输出"""
        try:
            # 尝试多种解码方式
            data_bytes = self.readAllStandardOutput().data()
            
            # 尝试不同编码
            for encoding in ['utf-8', 'gbk', 'cp936', 'iso-8859-1']:
                try:
                    data = data_bytes.decode(encoding)
                    self.commandOutput.emit(data)
                    return
                except UnicodeDecodeError:
                    continue
            
            # 如果所有编码都失败，使用替换模式
            data = data_bytes.decode('utf-8', errors='replace')
            self.commandOutput.emit(data)
            
        except Exception as e:
            self.commandError.emit(f"解码错误: {str(e)}")

    def readStandardError(self):
        """读取和处理标准错误"""
        try:
            # 尝试多种解码方式
            data_bytes = self.readAllStandardError().data()
            
            # 尝试不同编码
            for encoding in ['utf-8', 'gbk', 'cp936', 'iso-8859-1']:
                try:
                    data = data_bytes.decode(encoding)
                    self.commandError.emit(data)
                    return
                except UnicodeDecodeError:
                    continue
            
            # 如果所有编码都失败，使用替换模式
            data = data_bytes.decode('utf-8', errors='replace')
            self.commandError.emit(data)
            
        except Exception as e:
            self.commandError.emit(f"解码错误: {str(e)}")

    def onFinished(self, exit_code, exit_status):
        """处理进程完成"""
        self.commandFinished.emit(exit_code, exit_status)


class ConfigManager:
    """配置管理器，处理JSON配置文件"""
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".cmd_tool_gui")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.commands_file = "commands_config.json"
        self.ensure_config_dir()
        
    def ensure_config_dir(self):
        """确保配置目录存在"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def load_commands_config(self):
        """加载命令配置文件"""
        try:
            if os.path.exists(self.commands_file):
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 如果配置文件不存在，返回空配置
                return {"panels": [], "settings": {}}
        except Exception as e:
            print(f"Error loading commands configuration: {e}")
            return {"panels": [], "settings": {}}
    
    def save_custom_commands(self, panel_id, commands):
        """保存自定义命令到配置文件"""
        try:
            config = self.load_commands_config()
            
            # 查找自定义命令面板
            for panel in config["panels"]:
                if panel["id"] == panel_id:
                    panel["commands"] = commands
                    break
            
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def add_custom_command(self, panel_id, command_data):
        """添加自定义命令"""
        try:
            config = self.load_commands_config()
            
            # 查找自定义命令面板
            for panel in config["panels"]:
                if panel["id"] == panel_id:
                    panel["commands"].append(command_data)
                    break
            
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error adding custom command: {e}")
            return False
    
    def delete_custom_command(self, panel_id, command_name):
        """删除自定义命令"""
        try:
            config = self.load_commands_config()
            
            # 查找自定义命令面板
            for panel in config["panels"]:
                if panel["id"] == panel_id:
                    panel["commands"] = [cmd for cmd in panel["commands"] if cmd["name"] != command_name]
                    break
            
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error deleting custom command: {e}")
            return False


class CommandButton(QPushButton):
    """自定义命令按钮类"""
    
    def __init__(self, name, command, description, color="#2196F3", parent=None):
        super().__init__(name, parent)
        self.command = command
        self.description = description
        
        # 设置工具提示样式
        QToolTip.setFont(QFont('Microsoft YaHei UI', 9))
        
        # 设置工具提示内容
        tooltip_text = f"命令: {command}\n描述: {description}"
        self.setToolTip(tooltip_text)
        
        # 应用样式
        self.setStyleSheet(get_command_button_style(color))
        self.setMinimumSize(150, 40)
        
        



class CommandPanel(QWidget):
    """命令面板基类"""
    
    def __init__(self, panel_config, parent=None):
        super().__init__(parent)
        self.panel_config = panel_config
        self.process = CommandRunner()
        self.process.commandOutput.connect(self.updateOutput)
        self.process.commandError.connect(self.updateError)
        self.process.commandFinished.connect(self.onCommandFinished)
        self.current_working_dir = os.path.expanduser("~")
        self.current_command = ""
        
        self.setupUI()
        
    def setupUI(self):
        """设置UI组件"""
        self.layout = QVBoxLayout(self)
        
        # 工作目录选择
        dirLayout = QHBoxLayout()
        dirLabel = QLabel("工作目录:")
        dirLabel.setStyleSheet(LABEL_FONT)
        self.dirEdit = QLineEdit(self.current_working_dir)
        self.dirEdit.setMinimumWidth(480)
        self.dirEdit.setMaximumWidth(800)
        self.dirEdit.setMinimumHeight(int(SIZES["input_height"][:-2]))
        self.dirEdit.setFont(QFont("Microsoft YaHei UI", 11))
        self.dirEdit.setStyleSheet(DIR_EDIT_STYLE)
        browseDirButton = QPushButton("浏览")
        browseDirButton.setMinimumWidth(100)
        browseDirButton.setMinimumHeight(int(SIZES["button_height"][:-2]))
        browseDirButton.setFont(QFont("Microsoft YaHei UI", 11))
        browseDirButton.clicked.connect(self.browseDirectory)
        browseDirButton.setStyleSheet(BROWSE_BUTTON_STYLE)
        
        dirLayout.addWidget(dirLabel)
        dirLayout.addWidget(self.dirEdit, 1)
        dirLayout.addWidget(browseDirButton)
        
        # 命令按钮区域
        self.buttonsScrollArea = QScrollArea()
        self.buttonsScrollArea.setWidgetResizable(True)
        self.buttonsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.buttonsWidget = QWidget()
        self.buttonsLayout = QGridLayout(self.buttonsWidget)
        self.buttonsLayout.setSpacing(12)
        self.buttonsLayout.setContentsMargins(10, 10, 10, 10)
        
        # 加载命令按钮
        self.loadCommandButtons()
        
        self.buttonsScrollArea.setWidget(self.buttonsWidget)
        
        # 输出区域
        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setFont(QFont("Consolas", 10))
        self.outputText.setStyleSheet(OUTPUT_TEXT_STYLE)
        
        # 控制按钮
        controlLayout = QHBoxLayout()
        controlLayout.setSpacing(10)
        
        self.runButton = QPushButton("运行")
        self.runButton.setEnabled(False)
        self.runButton.setMinimumWidth(100)
        self.runButton.setMinimumHeight(int(SIZES["button_height"][:-2]))
        self.runButton.setStyleSheet(RUN_BUTTON_STYLE)
        self.runButton.clicked.connect(self.runCommand)
        
        self.stopButton = QPushButton("停止")
        self.stopButton.setEnabled(False)
        self.stopButton.setMinimumWidth(100)
        self.stopButton.setMinimumHeight(int(SIZES["button_height"][:-2]))
        self.stopButton.setStyleSheet(STOP_BUTTON_STYLE)
        self.stopButton.clicked.connect(self.stopCommand)
        
        self.clearButton = QPushButton("清除")
        self.clearButton.setMinimumWidth(100)
        self.clearButton.setMinimumHeight(int(SIZES["button_height"][:-2]))
        self.clearButton.setStyleSheet(CLEAR_BUTTON_STYLE)
        self.clearButton.clicked.connect(self.clearOutput)
        
        controlLayout.addWidget(self.runButton)
        controlLayout.addWidget(self.stopButton)
        controlLayout.addWidget(self.clearButton)
        controlLayout.addStretch(1)
        
        # 状态标签
        self.statusLabel = QLabel("就绪")
        self.statusLabel.setStyleSheet(STATUS_LABEL_STYLE)
        
        # 命令显示
        self.commandLabel = QLabel("选择一个命令按钮来执行")
        self.commandLabel.setStyleSheet(COMMAND_LABEL_STYLE)
        self.commandLabel.setMinimumHeight(36)
        
        # 添加组件到布局
        self.layout.addLayout(dirLayout)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.buttonsScrollArea)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.commandLabel)
        self.layout.addSpacing(10)
        self.layout.addLayout(controlLayout)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.outputText, 1)
        self.layout.addWidget(self.statusLabel)
        
    def loadCommandButtons(self):
        """加载命令按钮"""
        # 清除现有按钮
        while self.buttonsLayout.count():
            item = self.buttonsLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 获取配置中的命令
        commands = self.panel_config.get("commands", [])
        
        # 创建命令按钮
        row, col = 0, 0
        max_cols = 4  # 每行最多3个按钮，使按钮更大
        
        for cmd_data in commands:
            name = cmd_data.get("name", "")
            command = cmd_data.get("command", "")
            description = cmd_data.get("description", "")
            color = cmd_data.get("color", "#2196F3")
            
            button = CommandButton(name, command, description, color)
            # 使用lambda函数时需要使用默认参数来捕获当前值
            button.clicked.connect(lambda checked=False, cmd=command, desc=description: self.selectCommand(cmd, desc))
            
            self.buttonsLayout.addWidget(button, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # 添加空白空间
        self.buttonsLayout.setRowStretch(row + 1, 1)
        
    def selectCommand(self, command, description):
        """选择命令"""
        self.current_command = command
        self.commandLabel.setText(f"$ {command}")
        self.commandLabel.setToolTip(description)
        self.runButton.setEnabled(True)
        
    def browseDirectory(self):
        """浏览工作目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择工作目录",
            self.current_working_dir,
            QFileDialog.ShowDirsOnly
        )
        if dir_path:
            self.current_working_dir = dir_path
            self.dirEdit.setText(dir_path)
            
    def runCommand(self):
        """运行选中的命令"""
        command = self.current_command
        
        if not command:
            return
            
        self.outputText.append(f"$ {command}\n")
        self.statusLabel.setText("正在运行...")
        self.runButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        
        # 在执行命令前更改工作目录
        os.chdir(self.current_working_dir)
        self.process.execute(command)
        
    def stopCommand(self):
        """停止当前命令执行"""
        self.process.kill()
        
    def updateOutput(self, output):
        """用命令输出更新输出文本区域"""
        self.outputText.append(output)
        
    def updateError(self, error):
        """用命令错误更新输出文本区域"""
        self.outputText.append(f"<span style='color:#ff6d67;'>{error}</span>")
        
    def clearOutput(self):
        """清除输出文本区域"""
        self.outputText.clear()
        
    def onCommandFinished(self, exit_code, exit_status):
        """处理命令完成"""
        status = "完成" if exit_code == 0 else f"失败 (退出代码: {exit_code})"
        self.statusLabel.setText(status)
        self.runButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.outputText.append("\n")


class CustomCommandPanel(CommandPanel):
    """自定义命令面板"""
    
    def __init__(self, panel_config, parent=None):
        super().__init__(panel_config, parent)
        self.config_manager = ConfigManager()
        
    def setupUI(self):
        """设置UI组件"""
        super().setupUI()
        
        # 添加自定义命令区域
        customLayout = QHBoxLayout()
        customLayout.setSpacing(10)
        
        self.cmdNameEdit = QLineEdit()
        self.cmdNameEdit.setPlaceholderText("命令名称")
        self.cmdNameEdit.setStyleSheet(DIR_EDIT_STYLE)
        self.cmdNameEdit.setMinimumHeight(int(SIZES["input_height"][:-2]))
        
        self.cmdEdit = QLineEdit()
        self.cmdEdit.setPlaceholderText("命令内容")
        self.cmdEdit.setStyleSheet(DIR_EDIT_STYLE)
        self.cmdEdit.setMinimumHeight(int(SIZES["input_height"][:-2]))
        
        self.cmdDescEdit = QLineEdit()
        self.cmdDescEdit.setPlaceholderText("命令描述")
        self.cmdDescEdit.setStyleSheet(DIR_EDIT_STYLE)
        self.cmdDescEdit.setMinimumHeight(int(SIZES["input_height"][:-2]))
        
        addButton = QPushButton("添加命令")
        addButton.clicked.connect(self.addCommand)
        addButton.setStyleSheet(ADD_BUTTON_STYLE)
        addButton.setMinimumWidth(100)
        addButton.setMinimumHeight(int(SIZES["button_height"][:-2]))
        
        deleteButton = QPushButton("删除命令")
        deleteButton.clicked.connect(self.deleteCommand)
        deleteButton.setStyleSheet(DELETE_BUTTON_STYLE)
        deleteButton.setMinimumWidth(100)
        deleteButton.setMinimumHeight(int(SIZES["button_height"][:-2]))
        
        customLayout.addWidget(self.cmdNameEdit)
        customLayout.addWidget(self.cmdEdit)
        customLayout.addWidget(self.cmdDescEdit)
        customLayout.addWidget(addButton)
        customLayout.addWidget(deleteButton)
        
        # 插入到布局中
        self.layout.insertLayout(1, customLayout)
        self.layout.insertSpacing(2, 10)
        
    def addCommand(self):
        """添加自定义命令"""
        name = self.cmdNameEdit.text()
        command = self.cmdEdit.text()
        description = self.cmdDescEdit.text()
        
        if not name or not command:
            QMessageBox.warning(self, "警告", "请输入命令名称和命令内容。")
            return
        
        # 创建命令数据
        command_data = {
            "name": name,
            "command": command,
            "description": description or "自定义命令",
            "color": "#9C27B0"  # 默认颜色
        }
        
        # 添加到配置
        if self.config_manager.add_custom_command("custom", command_data):
            # 重新加载按钮
            self.panel_config = self.config_manager.load_commands_config()["panels"][-1]
            self.loadCommandButtons()
            
            # 清除输入字段
            self.cmdNameEdit.clear()
            self.cmdEdit.clear()
            self.cmdDescEdit.clear()
        else:
            QMessageBox.critical(self, "错误", "添加命令失败。")
    
    def deleteCommand(self):
        """删除自定义命令"""
        name = self.cmdNameEdit.text()
        
        if not name:
            QMessageBox.warning(self, "警告", "请输入要删除的命令名称。")
            return
        
        # 从配置中删除
        if self.config_manager.delete_custom_command("custom", name):
            # 重新加载按钮
            self.panel_config = self.config_manager.load_commands_config()["panels"][-1]
            self.loadCommandButtons()
            
            # 清除输入字段
            self.cmdNameEdit.clear()
            self.cmdEdit.clear()
            self.cmdDescEdit.clear()
        else:
            QMessageBox.critical(self, "错误", "删除命令失败。")


class HorizontalTextTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDrawBase(False)  # 不绘制基础线
        self.setExpanding(False)  # 不扩展填充
        
    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        if self.parent() and hasattr(self.parent(), 'tabPosition') and self.parent().tabPosition() == QTabWidget.West:
            return QSize(int(SIZES["tab_width"][:-2]), int(SIZES["tab_height"][:-2]))
        return size
    
    def paintEvent(self, event):
        painter = QStylePainter(self)
        
        # 设置背景颜色
        background_color = QColor(COLORS["background"])
        painter.fillRect(event.rect(), background_color)
        
        # 自定义绘制每个标签
        for i in range(self.count()):
            # 确定标签矩形
            rect = self.tabRect(i)
            
            # 创建圆角矩形路径
            path = QPainterPath()
            path.addRoundedRect(rect.adjusted(8, 5, -5, -5), 8, 8)
            
            # 设置颜色
            if i == self.currentIndex():
                # 选中的标签
                painter.fillPath(path, QColor(COLORS["accent"]))
                text_color = QColor(COLORS["text_selected"])
            else:
                # 未选中的标签
                painter.fillPath(path, QColor(COLORS["background_secondary"]))
                text_color = QColor(COLORS["text"])
            
            # 绘制文本
            painter.setPen(text_color)
            text = self.tabText(i)
            text_rect = rect.adjusted(20, 0, -10, 0)  # 文本边距
            
            # 设置字体
            font = painter.font()
            font.setPointSizeF(int(SIZES["font_size_large"][:-2]))
            if i == self.currentIndex():
                font.setBold(True)
            else:
                font.setBold(False)
            painter.setFont(font)
            
            # 绘制文本
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, text)


class MainWindow(QMainWindow):
    """主应用窗口"""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_commands_config()
        
        self.setWindowTitle("现代命令工具")
        self.setMinimumSize(1000, 700)
        self.setupUI()
        self.applyColorTheme()
        
    def setupUI(self):
        """设置主UI组件"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建水平布局，左侧是标签页，右侧是内容区域
        main_layout = QHBoxLayout(central_widget)
        
        # 创建标签页组件
        self.tabs = QTabWidget()
        # 设置自定义TabBar
        self.tabs.setTabBar(HorizontalTextTabBar())
        # 根据配置设置标签页位置
        tab_position = self.config["settings"].get("tab_position", "left")
        if tab_position == "left":
            self.tabs.setTabPosition(QTabWidget.West)
        
        # 从配置创建面板
        for panel_config in self.config["panels"]:
            panel_id = panel_config.get("id", "")
            panel_name = panel_config.get("name", "")
            
            if panel_id == "custom":
                panel = CustomCommandPanel(panel_config)
            else:
                panel = CommandPanel(panel_config)
                
            self.tabs.addTab(panel, panel_name)
        
        main_layout.addWidget(self.tabs)
        
        # 主界面背景色
        central_widget.setStyleSheet("background: #23202e;")
        
    def setTheme(self, theme_name):
        """设置应用主题"""
        theme = self.config["settings"].get(f"{theme_name}_theme", {})
        if not theme:
            return
            
        palette = QPalette()
        
        if theme_name == "dark":
            bg_color = QColor(theme.get("background", "#2d2d2d"))
            text_color = QColor(theme.get("text", "#ffffff"))
            button_color = QColor(theme.get("button", "#3a3a3a"))
            accent_color = QColor(theme.get("accent", "#2196F3"))
            
            palette.setColor(QPalette.Window, bg_color)
            palette.setColor(QPalette.WindowText, text_color)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, text_color)
            palette.setColor(QPalette.Button, button_color)
            palette.setColor(QPalette.ButtonText, text_color)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, accent_color)
            palette.setColor(QPalette.Highlight, accent_color)
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # 使用默认调色板
            QApplication.setPalette(QApplication.style().standardPalette())
            return
            
        QApplication.setPalette(palette)
    
    def applyColorTheme(self):
        """应用自定义颜色主题"""
        # 应用标签页样式
        self.tabs.setStyleSheet(get_tab_style())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置全局字体为微软雅黑
    font = QFont("Microsoft YaHei UI", 11)
    app.setFont(font)
    
    # 设置全局控件样式（现代扁平风格）
    app.setStyleSheet(GLOBAL_STYLE)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())