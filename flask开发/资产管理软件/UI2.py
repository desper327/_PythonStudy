import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QAbstractItemView, QComboBox, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QRadioButton, QButtonGroup
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

class AssetManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D资产管理系统")

        # 数据库连接
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('assets.db')
        if not self.db.open():
            print("无法打开数据库")
            return

        # 创建表（如果不存在）
        self.create_tables()

        # UI组件
        self.projectComboBox = QComboBox()
        self.load_projects()

        self.assetTypeGroup = QButtonGroup()
        self.characterRadio = QRadioButton("角色")
        self.propRadio = QRadioButton("道具")
        self.sceneRadio = QRadioButton("场景")
        self.assetTypeGroup.addButton(self.characterRadio, 0)
        self.assetTypeGroup.addButton(self.propRadio, 1)
        self.assetTypeGroup.addButton(self.sceneRadio, 2)

        self.searchLineEdit = QLineEdit()
        self.searchButton = QPushButton("搜索")
        self.searchButton.clicked.connect(self.search_assets)

        self.assetTable = QTableView()
        self.assetTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.assetTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.assetTable.clicked.connect(self.show_remarks)

        self.remarksTextEdit = QTextEdit()
        self.remarksTextEdit.setReadOnly(False)
        self.remarksTextEdit.textChanged.connect(self.save_remarks)

        # 按钮
        self.newProjectButton = QPushButton("新增项目")
        self.newProjectButton.clicked.connect(self.add_project)
        self.deleteProjectButton = QPushButton("删除项目")
        self.deleteProjectButton.clicked.connect(self.delete_project)

        self.newAssetButton = QPushButton("新增资产")
        self.newAssetButton.clicked.connect(self.add_asset)
        self.deleteAssetButton = QPushButton("删除资产")
        self.deleteAssetButton.clicked.connect(self.delete_asset)
        self.copyAssetButton = QPushButton("复制资产")
        self.copyAssetButton.clicked.connect(self.copy_asset)

        # 布局
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.projectComboBox)
        topLayout.addWidget(self.newProjectButton)
        topLayout.addWidget(self.deleteProjectButton)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.characterRadio)
        leftLayout.addWidget(self.propRadio)
        leftLayout.addWidget(self.sceneRadio)
        leftLayout.addWidget(self.searchLineEdit)
        leftLayout.addWidget(self.searchButton)
        leftLayout.addWidget(self.newAssetButton)
        leftLayout.addWidget(self.deleteAssetButton)
        leftLayout.addWidget(self.copyAssetButton)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(self.assetTable)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.remarksTextEdit)

        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(mainLayout)
        layout.addLayout(rightLayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_assets()

    def create_tables(self):
        query = self.db.exec("CREATE TABLE IF NOT EXISTS projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT)")
        query = self.db.exec("CREATE TABLE IF NOT EXISTS assets (asset_id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, asset_type TEXT, thumbnail TEXT, asset_name TEXT, chinese_name TEXT, remarks TEXT, FOREIGN KEY(project_id) REFERENCES projects(project_id))")

    def load_projects(self):
        self.projectComboBox.clear()
        query = self.db.exec("SELECT project_id, project_name FROM projects")
        while query.next():
            project_id = query.value(0)
            project_name = query.value(1)
            self.projectComboBox.addItem(project_name, project_id)

    def load_assets(self):
        project_id = self.projectComboBox.currentData()
        if project_id is None:
            return

        model = QSqlTableModel()
        model.setTable("assets")
        model.setSort(1, Qt.AscendingOrder)
        model.setFilter(f"project_id = {project_id}")
        model.select()
        self.assetTable.setModel(model)

    def search_assets(self):
        keyword = self.searchLineEdit.text()
        if keyword:
            project_id = self.projectComboBox.currentData()
            if project_id is None:
                return
            filter_str = f"project_id = {project_id} AND (asset_name LIKE '%{keyword}%' OR chinese_name LIKE '%{keyword}%')"
            model = QSqlTableModel()
            model.setTable("assets")
            model.setFilter(filter_str)
            model.select()
            self.assetTable.setModel(model)
        else:
            self.load_assets()

    def show_remarks(self, index):
        asset_id = self.assetTable.model().data(self.assetTable.model().index(index.row(), 0))
        query = self.db.exec(f"SELECT remarks FROM assets WHERE asset_id = {asset_id}")
        if query.next():
            remarks = query.value(0)
            self.remarksTextEdit.setText(remarks)

    def save_remarks(self):
        selectedModelIndex = self.assetTable.selectionModel().selectedRows()
        if not selectedModelIndex:
            return
        row = selectedModelIndex[0].row()
        asset_id = self.assetTable.model().data(self.assetTable.model().index(row, 0))
        remarks = self.remarksTextEdit.toPlainText()
        query = self.db.exec(f"UPDATE assets SET remarks = '{remarks}' WHERE asset_id = {asset_id}")

    def add_project(self):
        # 弹出对话框输入项目名称
        pass

    def delete_project(self):
        # 确认删除项目及其资产
        pass

    def add_asset(self):
        # 弹出对话框输入资产信息
        pass

    def delete_asset(self):
        # 确认删除选中的资产
        pass

    def copy_asset(self):
        # 复制选中的资产
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AssetManagementWindow()
    window.show()
    sys.exit(app.exec_())