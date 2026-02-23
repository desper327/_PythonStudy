from view import  MyView
from model import Project
from PyQt5.QtCore import pyqtSignal, QObject 
import PyQt5.QtWidgets as QtWidgets
import sys

class MyController:
    def __init__(self):
        self.view = MyView()
        self.model= Project(name="项目1", description="项目1描述", frame_rate=25)
        # self.view.bind_signal()
        self.bind_signal()
    
    def run(self):
        self.view.show()

    def bind_signal(self):
        print("bind_view_signal")
        self.view.proj_combo.currentIndexChanged.connect(self.proj_changed_signal)
        self.view.proj_edit1.textChanged.connect(self.proj_edit1_changed_signal)
        self.view.proj_edit2.textChanged.connect(self.proj_edit2_changed_signal)
        self.view.proj_edit3.textChanged.connect(self.proj_edit3_changed_signal)

        print("bind_model_signal")
        self.model.name.subscribe(self.model_name_changed_signal)

    def proj_changed_signal(self, index):
        print("proj_changed_signal")
        self.view.proj_edit1.setText(self.view.proj_combo.currentText())
        self.view.proj_edit2.setText(self.view.proj_combo.currentText())
        self.view.proj_edit3.setText(self.view.proj_combo.currentText())

    def proj_edit1_changed_signal(self, text):
        self.view.proj_edit2.setText(text)
        self.view.proj_edit3.setText(text)

    def proj_edit2_changed_signal(self, text):
        self.view.proj_edit1.setText(text)
        self.view.proj_edit3.setText(text)

    def proj_edit3_changed_signal(self, text):
        self.view.proj_edit1.setText(text)
        self.view.proj_edit2.setText(text)






    # def bind_signal(self):
    #     for k,v in self.view.bind_dict.items():
    #         self.view.bind_dict[k].connect(getattr(self, k))




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = MyController()
    controller.run()
    sys.exit(app.exec_())