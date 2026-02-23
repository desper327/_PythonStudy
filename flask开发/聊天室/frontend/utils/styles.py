"""
UI样式表
现代风格的QSS样式
"""
from config import Config


def get_stylesheet() -> str:
    """
    获取应用样式表（现代风格）
    
    Returns:
        str: QSS样式字符串
    """
    return f"""
    /* ==================== 全局样式 ==================== */
    QWidget {{
        font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
        font-size: 14px;
        color: {Config.TEXT_PRIMARY};
    }}
    
    /* ==================== 按钮样式 ==================== */
    QPushButton {{
        background-color: {Config.PRIMARY_COLOR};
        color: white;
        border: none;
        border-radius: {Config.BORDER_RADIUS};
        padding: 8px 16px;
        font-weight: 500;
    }}
    
    QPushButton:hover {{
        background-color: #40a9ff;
    }}
    
    QPushButton:pressed {{
        background-color: #096dd9;
    }}
    
    QPushButton:disabled {{
        background-color: {Config.BORDER_COLOR};
        color: {Config.TEXT_DISABLED};
    }}
    
    QPushButton#secondaryButton {{
        background-color: white;
        color: {Config.TEXT_PRIMARY};
        border: 1px solid {Config.BORDER_COLOR};
    }}
    
    QPushButton#secondaryButton:hover {{
        color: {Config.PRIMARY_COLOR};
        border-color: {Config.PRIMARY_COLOR};
    }}
    
    QPushButton#dangerButton {{
        background-color: {Config.ERROR_COLOR};
    }}
    
    QPushButton#dangerButton:hover {{
        background-color: #ff4d4f;
    }}
    
    /* ==================== 输入框样式 ==================== */
    QLineEdit, QTextEdit {{
        background-color: white;
        border: 1px solid {Config.BORDER_COLOR};
        border-radius: {Config.BORDER_RADIUS};
        padding: 8px 12px;
    }}
    
    QLineEdit:focus, QTextEdit:focus {{
        border-color: {Config.PRIMARY_COLOR};
        outline: none;
    }}
    
    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: #f5f5f5;
        color: {Config.TEXT_DISABLED};
    }}
    
    /* ==================== 标签样式 ==================== */
    QLabel {{
        color: {Config.TEXT_PRIMARY};
    }}
    
    QLabel#titleLabel {{
        font-size: 24px;
        font-weight: bold;
        color: {Config.PRIMARY_COLOR};
    }}
    
    QLabel#subtitleLabel {{
        font-size: 18px;
        font-weight: 600;
    }}
    
    QLabel#secondaryLabel {{
        color: {Config.TEXT_SECONDARY};
        font-size: 12px;
    }}
    
    /* ==================== 列表样式 ==================== */
    QListWidget {{
        background-color: white;
        border: 1px solid {Config.BORDER_COLOR};
        border-radius: {Config.BORDER_RADIUS};
        outline: none;
    }}
    
    QListWidget::item {{
        padding: 12px;
        border-bottom: 1px solid #f0f0f0;
    }}
    
    QListWidget::item:selected {{
        background-color: #e6f7ff;
        color: {Config.PRIMARY_COLOR};
    }}
    
    QListWidget::item:hover {{
        background-color: #f5f5f5;
    }}
    
    /* ==================== 滚动条样式 ==================== */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: #d9d9d9;
        border-radius: 4px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: #bfbfbf;
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background-color: transparent;
        height: 8px;
        margin: 0px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: #d9d9d9;
        border-radius: 4px;
        min-width: 30px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: #bfbfbf;
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* ==================== Tab标签页样式 ==================== */
    QTabWidget::pane {{
        border: 1px solid {Config.BORDER_COLOR};
        border-radius: {Config.BORDER_RADIUS};
        background-color: white;
    }}
    
    QTabBar::tab {{
        background-color: #f5f5f5;
        border: 1px solid {Config.BORDER_COLOR};
        border-bottom: none;
        padding: 8px 16px;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: white;
        color: {Config.PRIMARY_COLOR};
        font-weight: 600;
    }}
    
    QTabBar::tab:hover {{
        background-color: #fafafa;
    }}
    
    /* ==================== 分组框样式 ==================== */
    QGroupBox {{
        border: 1px solid {Config.BORDER_COLOR};
        border-radius: {Config.BORDER_RADIUS};
        margin-top: 12px;
        padding: 16px;
        background-color: white;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        color: {Config.TEXT_PRIMARY};
        font-weight: 600;
    }}
    
    /* ==================== 菜单样式 ==================== */
    QMenuBar {{
        background-color: white;
        border-bottom: 1px solid {Config.BORDER_COLOR};
    }}
    
    QMenuBar::item {{
        padding: 8px 12px;
        background-color: transparent;
    }}
    
    QMenuBar::item:selected {{
        background-color: #f5f5f5;
    }}
    
    QMenu {{
        background-color: white;
        border: 1px solid {Config.BORDER_COLOR};
        border-radius: {Config.BORDER_RADIUS};
    }}
    
    QMenu::item {{
        padding: 8px 24px;
    }}
    
    QMenu::item:selected {{
        background-color: #f5f5f5;
    }}
    
    /* ==================== 对话框样式 ==================== */
    QDialog {{
        background-color: white;
    }}
    
    QMessageBox {{
        background-color: white;
    }}
    
    /* ==================== 工具提示样式 ==================== */
    QToolTip {{
        background-color: #262626;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 4px 8px;
    }}
    
    /* ==================== 分隔线样式 ==================== */
    QFrame[frameShape="4"], QFrame[frameShape="5"] {{
        color: {Config.BORDER_COLOR};
    }}
    """
