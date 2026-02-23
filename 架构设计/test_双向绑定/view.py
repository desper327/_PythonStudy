import PyQt5.QtWidgets as QtWidgets

class MyView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.bind_signal()

    def init_ui(self):
        self.setWindowTitle('双向绑定')
        self.resize(300, 200)
        self.proj_combo = QtWidgets.QComboBox()
        self.proj_combo.addItems(['项目1', '项目2', '项目3'])
        self.proj_edit1 = QtWidgets.QLineEdit()
        self.proj_edit1.setText('项目1')
        self.proj_edit2 = QtWidgets.QLineEdit()
        self.proj_edit2.setText('项目2')
        self.proj_edit3 = QtWidgets.QLineEdit()
        self.proj_edit3.setText('项目3')
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.proj_combo, 0, 0, 1, 2)
        self.layout.addWidget(self.proj_edit1, 1, 0, 1, 2)
        self.layout.addWidget(self.proj_edit2, 2, 0, 1, 2)
        self.layout.addWidget(self.proj_edit3, 3, 0, 1, 2)
        self.setLayout(self.layout)


    # def bind_signal(self):
    #     self.bind_dict={"proj_changed_signal" : self.proj_combo.currentIndexChanged, 
    #                 "proj_edit1_changed_signal" : self.proj_edit1.textChanged, 
    #                 "proj_edit2_changed_signal" : self.proj_edit2.textChanged, 
    #                 "proj_edit3_changed_signal" : self.proj_edit3.textChanged}
        