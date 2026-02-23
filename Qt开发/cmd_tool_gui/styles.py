#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
样式定义模块 - 集中管理应用程序的所有UI样式
"""

# 尺寸定义
SIZES = {
    "button_height": "20px",
    "input_height": "20px",
    "border_radius": "8px",
    "padding_horizontal": "16px",
    "padding_vertical": "8px",
    "margin": "6px",
    "font_size_normal": "11pt",
    "font_size_large": "12pt",
    "font_size_small": "10pt",
    "icon_size": "16px",
    "tab_height": "60px",
    "tab_width": "140px"
}

# 颜色定义
COLORS = {
    "background": "#23202e",
    "background_secondary": "#2a2636",
    "background_input": "#343044",
    "border": "#443f5a",
    "text": "#d8d8d8",
    "text_secondary": "#a0a0a0",
    "text_selected": "#ffffff",
    "accent": "#6a0dad",
    "accent_hover": "#560a8b",
    "accent_pressed": "#4a0777",
    "accent_light": "#9370db",
    "success": "#4CAF50",
    "success_hover": "#45a049",
    "success_pressed": "#3d8b40",
    "danger": "#f44336",
    "danger_hover": "#d32f2f",
    "danger_pressed": "#b71c1c",
    "info": "#2196F3",
    "info_hover": "#1976D2",
    "info_pressed": "#1565C0",
    "disabled_bg": "#555555",
    "disabled_text": "#999999",
    "highlight": "#9c27b0"
}

# 全局样式
GLOBAL_STYLE = f"""
    QWidget {{
        font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif;
        font-size: {SIZES["font_size_normal"]};
        color: {COLORS["text"]};
    }}
    QMainWindow, QDialog {{
        background: {COLORS["background"]};
    }}
    QLineEdit, QTextEdit {{
        background: {COLORS["background_input"]};
        border: 1.5px solid {COLORS["border"]};
        border-radius: {SIZES["border_radius"]};
        padding: {SIZES["padding_vertical"]} {SIZES["padding_horizontal"]};
        min-height: {SIZES["input_height"]};
        font-size: {SIZES["font_size_normal"]};
        color: {COLORS["text"]};
        selection-background-color: {COLORS["accent"]};
        selection-color: {COLORS["text_selected"]};
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid {COLORS["accent_light"]};
        background: {COLORS["background_secondary"]};
    }}
    QPushButton {{
        background: {COLORS["accent"]};
        color: {COLORS["text_selected"]};
        border: none;
        border-radius: {SIZES["border_radius"]};
        padding: {SIZES["padding_vertical"]} {SIZES["padding_horizontal"]};
        min-height: {SIZES["button_height"]};
        font-size: {SIZES["font_size_normal"]};
        font-weight: 600;
    }}
    QPushButton:hover {{
        background: {COLORS["accent_hover"]};
    }}
    QPushButton:pressed {{
        background: {COLORS["accent_pressed"]};
    }}
    QPushButton:disabled {{
        background: {COLORS["disabled_bg"]};
        color: {COLORS["disabled_text"]};
    }}
    QLabel {{
        color: {COLORS["text"]};
        font-size: {SIZES["font_size_normal"]};
    }}
    QScrollArea {{
        border: none;
        background: transparent;
    }}
    QTextEdit {{
        background: {COLORS["background_secondary"]};
        color: {COLORS["text"]};
        font-family: 'Consolas', 'Microsoft YaHei UI', monospace;
        font-size: {SIZES["font_size_normal"]};
        border-radius: {SIZES["border_radius"]};
        border: 1.5px solid {COLORS["border"]};
        padding: {SIZES["padding_vertical"]} {SIZES["padding_horizontal"]};
    }}
    QScrollBar:vertical {{
        border: none;
        background: {COLORS["background_secondary"]};
        width: 10px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLORS["border"]};
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLORS["accent"]};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        border: none;
        background: {COLORS["background_secondary"]};
        height: 10px;
        margin: 0px;
    }}
    QScrollBar::handle:horizontal {{
        background: {COLORS["border"]};
        min-width: 20px;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {COLORS["accent"]};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    QToolTip {{
        background-color: {COLORS["background_secondary"]};
        color: {COLORS["text"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 4px;
        padding: 6px;
        opacity: 220;
    }}
"""

# 标签页样式
def get_tab_style():
    return f"""
        QTabWidget::pane {{
            border: none;
            background: {COLORS["background"]};
            border-radius: 0px;
        }}
        QTabWidget::tab-bar:left {{
            alignment: left;
            width: {SIZES["tab_width"]};
            background: {COLORS["background"]};
        }}
        QTabBar::tab:left {{
            background: {COLORS["background_secondary"]};
            color: {COLORS["text"]};
            border: none;
            border-radius: {SIZES["border_radius"]};
            min-height: {SIZES["tab_height"]};
            padding: 0 18px;
            margin: 8px 0 8px 10px;
            font-size: {SIZES["font_size_large"]};
            width: 130px;
            text-align: left;
            font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif;
        }}
        QTabBar::tab:left:selected {{
            background: {COLORS["accent"]};
            color: {COLORS["text_selected"]};
            font-weight: bold;
        }}
        QTabBar::tab:left:hover:!selected {{
            background: {COLORS["border"]};
            color: {COLORS["accent_light"]};
        }}
        /* 移除指示器 */
        QTabBar::indicator {{
            width: 0;
            height: 0;
            background: transparent;
        }}
        QTabWidget::pane {{
            top: 0;
            border: none;
        }}
        QTabBar::tear {{
            width: 0;
            height: 0;
            background: transparent;
        }}
        QTabBar::scroller {{
            width: 0;
            height: 0;
        }}
    """

# 按钮样式
def get_button_style(color, hover_color, pressed_color):
    return f"""
        QPushButton {{
            background-color: {color};
            color: {COLORS["text_selected"]};
            border-radius: {SIZES["border_radius"]};
            padding: {SIZES["padding_vertical"]} {SIZES["padding_horizontal"]};
            min-height: {SIZES["button_height"]};
            font-weight: 600;
            font-size: {SIZES["font_size_normal"]};
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {pressed_color};
        }}
        QPushButton:disabled {{
            background-color: {COLORS["disabled_bg"]};
            color: {COLORS["disabled_text"]};
        }}
    """

# 预定义按钮样式
RUN_BUTTON_STYLE = get_button_style(COLORS["success"], COLORS["success_hover"], COLORS["success_pressed"])
STOP_BUTTON_STYLE = get_button_style(COLORS["danger"], COLORS["danger_hover"], COLORS["danger_pressed"])
CLEAR_BUTTON_STYLE = get_button_style(COLORS["info"], COLORS["info_hover"], COLORS["info_pressed"])
BROWSE_BUTTON_STYLE = get_button_style(COLORS["accent"], COLORS["accent_hover"], COLORS["accent_pressed"])
ADD_BUTTON_STYLE = get_button_style(COLORS["success"], COLORS["success_hover"], COLORS["success_pressed"])
DELETE_BUTTON_STYLE = get_button_style(COLORS["danger"], COLORS["danger_hover"], COLORS["danger_pressed"])

# 命令按钮样式
def get_command_button_style(color):
    dark_color = darken_color(color, 0.9)
    return f"""
        QPushButton {{
            background-color: {color};
            color: {COLORS["text_selected"]};
            border-radius: {SIZES["border_radius"]};
            padding: 10px;
            font-weight: 600;
            text-align: center;
            font-size: {SIZES["font_size_normal"]};
            min-height: 20px;
            min-width: 140px;
            border: 1px solid {COLORS["border"]};
        }}
        QPushButton:hover {{
            background-color: {dark_color};
            border: 1px solid {COLORS["accent_light"]};
        }}
        QPushButton:pressed {{
            background-color: {darken_color(dark_color, 0.9)};
        }}
    """

# 工作目录输入框样式
DIR_EDIT_STYLE = f"""
    color: {COLORS["text"]};
    background-color: {COLORS["background_input"]};
    border: 1.5px solid {COLORS["border"]};
    border-radius: {SIZES["border_radius"]};
    padding: {SIZES["padding_vertical"]} {SIZES["padding_horizontal"]};
    min-height: {SIZES["input_height"]};
    font-size: {SIZES["font_size_normal"]};
    selection-background-color: {COLORS["accent"]};
    selection-color: {COLORS["text_selected"]};
"""

# 命令标签样式
COMMAND_LABEL_STYLE = f"""
    color: {COLORS["text"]};
    padding: 10px {SIZES["padding_horizontal"]};
    background-color: {COLORS["background_input"]};
    border-radius: {SIZES["border_radius"]};
    font-family: 'Consolas', 'Microsoft YaHei UI', monospace;
    font-size: {SIZES["font_size_normal"]};
    min-height: 24px;
    border-left: 3px solid {COLORS["accent"]};
"""
LABEL_FONT=f"""
    font-size: {SIZES["font_size_normal"]};
    font-weight: 600;
    color:{COLORS["text"]}
"""

# 状态标签样式
STATUS_LABEL_STYLE = f"""
    color: {COLORS["text_secondary"]};
    padding: 5px;
    font-size: {SIZES["font_size_small"]};
"""

# 输出文本区域样式
OUTPUT_TEXT_STYLE = f"""
    background-color: {COLORS["background_secondary"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: {SIZES["border_radius"]};
    padding: 10px;
    selection-background-color: {COLORS["accent"]};
    font-family: 'Consolas', 'Microsoft YaHei UI', monospace;
    font-size: {SIZES["font_size_normal"]};
"""

# 辅助函数
def darken_color(hex_color, factor=0.8):
    """使颜色变暗"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f"#{r:02x}{g:02x}{b:02x}"

def lighten_color(hex_color, factor=1.2):
    """使颜色变亮"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    return f"#{r:02x}{g:02x}{b:02x}" 