import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QFileDialog, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# 数据库路径
DB_FILE = 'MyStudy\\资产管理软件\\assets.db'

class AssetManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('3D资产管理工具')
        self.resize(800, 600)

        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        self.initUI()
        self.load_data()

    def initUI(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['缩略图', '名称', '中文名', '备注'])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.table.cellChanged.connect(self.update_data)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        btn_import = QPushButton('导入资产', self)
        btn_import.clicked.connect(self.import_asset)
        layout.addWidget(btn_import)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        self.table.setRowCount(0)
        self.cursor.execute('SELECT id, thumbnail, name, chinese_name, notes FROM assets')
        for row_id, thumbnail, name, chinese_name, notes in self.cursor.fetchall():
            row = self.table.rowCount()
            self.table.insertRow(row)

            # 缩略图
            pixmap = QPixmap(thumbnail).scaled(64, 64, Qt.KeepAspectRatio)
            thumbnail_item = QTableWidgetItem()
            #thumbnail_item.set(pixmap)
            thumbnail_item.setData(Qt.DecorationRole, pixmap)
            self.table.setItem(row, 0, thumbnail_item)

            # 名称、中文名、备注
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(chinese_name))
            self.table.setItem(row, 3, QTableWidgetItem(notes))

    def update_data(self, row, column):
        id = row + 1
        if column == 1:
            value = self.table.item(row, column).text()
            self.cursor.execute('UPDATE assets SET name=? WHERE id=?', (value, id))
        elif column == 2:
            value = self.table.item(row, column).text()
            self.cursor.execute('UPDATE assets SET chinese_name=? WHERE id=?', (value, id))
        elif column == 3:
            value = self.table.item(row, column).text()
            self.cursor.execute('UPDATE assets SET notes=? WHERE id=?', (value, id))
        self.conn.commit()

    def import_asset(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(self, '选择资产文件夹')
        if folder_path:
            thumbnail_path = f'{folder_path}/thumbnail.jpg'
            print(thumbnail_path)
            # 使用 FFmpeg 生成缩略图（假设资产是一个视频文件）
            import subprocess
            subprocess.run(['ffmpeg', '-i', f'{folder_path}/材质练习.mov', '-vf', 'scale=64:64', thumbnail_path])

            # 插入到数据库
            self.cursor.execute('INSERT INTO assets (name, thumbnail, notes) VALUES (?, ?, ?)',
                                ('New Asset', thumbnail_path, ''))
            self.conn.commit()
            self.load_data()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AssetManager()
    window.show()
    sys.exit(app.exec_())
