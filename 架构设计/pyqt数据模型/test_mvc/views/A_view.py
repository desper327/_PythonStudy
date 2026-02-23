import sys

from PySide6.QtWidgets import QMainWindow
from .piplineTool_3_ui import Ui_MainWindow


class A_view(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.info_html_style = """
        <style>
            .info-root { font-family: "Microsoft YaHei", sans-serif; font-size: 15px; color: #bdbdbd }
            .info-title { font-size: 15px; font-weight: bold; color: #4A90E2; }
            .info-desc { font-size: 15px; color: #bdbdbd; margin: 4px 0 8px 0; }
            .info-small { font-size: 12px;  }
            .info-meta { font-size: 12px; color: #888; margin-top: 4px; }
            .info-meta .author { color: #4A90E2; }
            .info-meta .time { color: #B77B2B; }
            .info-divider { border-bottom: 1px solid #444; margin: 8px 0; }
            a { color: #3399ff; }
        </style>
        """


