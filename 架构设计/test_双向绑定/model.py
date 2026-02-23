from pydantic import BaseModel, Field
from beartype import beartype
from PyQt5.QtCore import pyqtSignal, QObject 

class Project(BaseModel):
    name: str = Field(..., title="项目名称")
    description: str = Field(..., title="项目描述")
    frame_rate: int = Field(..., title="帧率")







class Project_data(QObject):
    name_changed = pyqtSignal(Project)
    description_changed = pyqtSignal(Project)
    frame_rate_changed = pyqtSignal(Project)

    @beartype
    def __init__(self, project: Project):
        super().__init__()
        self._project = project
        
    @property
    def project(self) -> Project:
        return self._project
