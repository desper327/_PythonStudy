"""
数据中心 - 管理数据的业务逻辑，包含自定义信号
这个类继承自QObject，可以发射信号通知数据变化
"""
from typing import List, Optional
from Qt.QtCore import QObject, Signal
from .data_models import SignalData,TextData

class DataCenter(QObject):
    """数据中心 - 带有信号的数据管理层"""
    model_signal = Signal(SignalData)  # 任务信号 (任务对象)
    
    def __init__(self):
        super().__init__()
        self._text_data: TextData = TextData()
        self._thread_data: TextData = TextData()

    @property
    def text(self):
        print(f"[Data Center] get 'text': {self._text_data.text}")
        return self._text_data

    @text.setter
    def text(self, value:TextData):
        if value.text != self._text_data.text:
            self._text_data = value
            self.model_signal.emit(SignalData(signal_type="text_changed", params=[value]))  
            print("[Data Center] emit a 'text_changed' signal")
        else:
            print("[Data Center] text not changed")

    @property
    def thread_data(self):
        print(f"[Data Center] get 'thread_data': {self._thread_data.text}")
        return self._thread_data
    
    @thread_data.setter
    def thread_data(self, value:TextData):
        if value.text != self._thread_data.text:
            self._thread_data = value
            self.model_signal.emit(SignalData(signal_type="thread_data_changed", params=[value]))  
            print("[Data Center] emit a 'thread_data_changed' signal")
        else:
            print("[Data Center] thread_data not changed")
    