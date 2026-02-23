# 这个类继承自QObject，可以发射信号通知数据变化

from typing import List, Optional
from PySide6.QtCore import QObject, Signal
from .data_models import Project,Stage,Episode,Scene,Shot


class A_model(QObject):
    # 定义信号
    projects_changed = Signal(list)
    current_project_changed = Signal(Project)
    stages_changed = Signal(list)
    current_stage_changed = Signal(Stage)
    episodes_changed = Signal(Episode)
    scenes_changed = Signal(Scene)
    shots_changed = Signal(Shot)
    current_eps_changed = Signal(Episode)
    current_sc_changed = Signal(Scene)
    current_shot_changed = Signal(Shot)
    mytask_changed = Signal(bool)
    
    def __init__(self):
        super().__init__()
        self._projects: List[Project] = []
        self._current_project: Optional[Project] = None
        self._stages: List[Stage] = []
        self._current_stage: Optional[Stage] = None
        self._episodes: Optional[List[Episode]] = None
        self._current_eps = None
        self._scenes: Optional[List[Scene]] = None
        self._current_sc = None
        self._shots: Optional[List[Shot]] = None
        self._current_shot = None
        self._mytask = False

    @property
    def projects(self):
        return self._projects
    
    @projects.setter
    def projects(self, projects: List[Project]):
        if self._projects != projects:
            self._projects = sorted(projects,key=lambda project: project.project_full_name)
            print([project.project_full_name for project in self._projects])
            self.projects_changed.emit(self._projects)
        
    @property
    def current_project(self):
        return self._current_project

    @current_project.setter
    def current_project(self,project:Project):
        if self._current_project != project:
            self._current_project = project
            self.current_project_changed.emit(self._current_project)
    
    @property
    def stages(self):
        return self._stages
    
    @stages.setter
    def stages(self, stages: List[Stage]):
        if self._stages != stages:
            self._stages = sorted(stages,key=lambda stage: stage.entity)
            self.stages_changed.emit(self._stages)
    
    @property
    def current_stage(self):
        return self._current_stage
    
    @current_stage.setter
    def current_stage(self, stage: Stage):
        if self._current_stage != stage:
            self._current_stage = stage
            self.current_stage_changed.emit(self._current_stage)

    @property
    def episodes(self):
        return self._episodes
    
    @episodes.setter
    def episodes(self,episodes:List[Episode]):
        if self._episodes != episodes:
            self._episodes = sorted(episodes,key=lambda episode: episode.eps_entity)
            self.episodes_changed.emit(self._episodes)

    @property
    def scenes(self):
        return self._scenes
    
    @scenes.setter
    def scenes(self,scenes:List[Scene]):
        if self._scenes != scenes:
            self._scenes = sorted(scenes,key=lambda scene: scene.sc_entity)
            self.scenes_changed.emit(self._scenes)

    @property
    def shots(self):
        return self._shots
    
    @shots.setter
    def shots(self,shots:List[Shot]):
        if self._shots != shots:
            self._shots = sorted(shots,key=lambda shot: shot.shot_entity)
            self.shots_changed.emit(self._shots)

    @property
    def current_eps(self):
        return self._current_eps
    
    @current_eps.setter
    def current_eps(self,eps:Episode):
        if self._current_eps != eps:
            self._current_eps = eps
            self.current_eps_changed.emit(self._current_eps)

    @property
    def current_sc(self):
        return self._current_sc
    
    @current_sc.setter
    def current_sc(self,sc:Scene):
        if self._current_sc != sc:
            self._current_sc = sc
            self.current_sc_changed.emit(self._current_sc)
    
    @property
    def current_shot(self):
        return self._current_shot
    
    @current_shot.setter
    def current_shot(self,shot:Shot):
        if self._current_shot != shot:
            self._current_shot = shot
            self.current_shot_changed.emit(self._current_shot)

    @property
    def mytask(self):
        return self._mytask
    
    @mytask.setter
    def mytask(self,mytask:bool):
        if self._mytask != mytask:
            self._mytask = mytask
            self.mytask_changed.emit(self._mytask)
    