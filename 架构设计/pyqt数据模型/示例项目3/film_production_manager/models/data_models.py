"""
数据模型定义
包含项目、集、场、镜头、阶段等核心数据结构
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class ProductionStage(Enum):
    """制作阶段枚举"""
    ANIMATION = "动画"
    KEY_FRAME = "原画"
    LIGHTING = "灯光"
    VFX = "特效"
    SOLVING = "解算"
    COMPOSITING = "合成"
    RENDERING = "渲染"


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "待开始"
    IN_PROGRESS = "进行中"
    REVIEW = "审核中"
    APPROVED = "已批准"
    REJECTED = "已拒绝"
    COMPLETED = "已完成"


@dataclass
class FileInfo:
    """文件信息数据类"""
    file_id: str
    file_name: str
    file_path: str
    file_size: int
    file_type: str
    created_time: datetime
    modified_time: datetime
    version: str = "1.0"
    description: str = ""
    
    def __post_init__(self):
        """初始化后处理"""
        if isinstance(self.created_time, str):
            self.created_time = datetime.fromisoformat(self.created_time)
        if isinstance(self.modified_time, str):
            self.modified_time = datetime.fromisoformat(self.modified_time)


@dataclass
class Task:
    """任务数据类"""
    task_id: str
    task_name: str
    stage: ProductionStage
    status: TaskStatus
    assignee: str
    created_time: datetime
    due_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    description: str = ""
    priority: int = 1  # 1-5, 5为最高优先级
    progress: float = 0.0  # 0.0-1.0
    files: List[FileInfo] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后处理"""
        if isinstance(self.created_time, str):
            self.created_time = datetime.fromisoformat(self.created_time)
        if isinstance(self.due_time, str):
            self.due_time = datetime.fromisoformat(self.due_time)
        if isinstance(self.completed_time, str):
            self.completed_time = datetime.fromisoformat(self.completed_time)
        if isinstance(self.stage, str):
            self.stage = ProductionStage(self.stage)
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)


@dataclass
class Shot:
    """镜头数据类"""
    shot_id: str
    shot_name: str
    shot_number: str
    description: str = ""
    duration: float = 0.0  # 秒
    frame_start: int = 1
    frame_end: int = 1
    frame_rate: float = 24.0
    tasks: List[Task] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def total_frames(self) -> int:
        """总帧数"""
        return self.frame_end - self.frame_start + 1
    
    def get_tasks_by_stage(self, stage: ProductionStage) -> List[Task]:
        """根据阶段获取任务"""
        return [task for task in self.tasks if task.stage == stage]


@dataclass
class Scene:
    """场数据类"""
    scene_id: str
    scene_name: str
    scene_number: str
    description: str = ""
    shots: List[Shot] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        all_tasks = []
        for shot in self.shots:
            all_tasks.extend(shot.tasks)
        return all_tasks
    
    def get_tasks_by_stage(self, stage: ProductionStage) -> List[Task]:
        """根据阶段获取所有任务"""
        all_tasks = []
        for shot in self.shots:
            all_tasks.extend(shot.get_tasks_by_stage(stage))
        return all_tasks


@dataclass
class Episode:
    """集数据类"""
    episode_id: str
    episode_name: str
    episode_number: str
    description: str = ""
    scenes: List[Scene] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        all_tasks = []
        for scene in self.scenes:
            all_tasks.extend(scene.get_all_tasks())
        return all_tasks
    
    def get_tasks_by_stage(self, stage: ProductionStage) -> List[Task]:
        """根据阶段获取所有任务"""
        all_tasks = []
        for scene in self.scenes:
            all_tasks.extend(scene.get_tasks_by_stage(stage))
        return all_tasks


@dataclass
class Project:
    """项目数据类"""
    project_id: str
    project_name: str
    description: str = ""
    created_time: datetime = field(default_factory=datetime.now)
    episodes: List[Episode] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后处理"""
        if isinstance(self.created_time, str):
            self.created_time = datetime.fromisoformat(self.created_time)
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        all_tasks = []
        for episode in self.episodes:
            all_tasks.extend(episode.get_all_tasks())
        return all_tasks
    
    def get_tasks_by_stage(self, stage: ProductionStage) -> List[Task]:
        """根据阶段获取所有任务"""
        all_tasks = []
        for episode in self.episodes:
            all_tasks.extend(episode.get_tasks_by_stage(stage))
        return all_tasks
    
    def get_project_statistics(self) -> Dict[str, Any]:
        """获取项目统计信息"""
        all_tasks = self.get_all_tasks()
        total_tasks = len(all_tasks)
        
        if total_tasks == 0:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "in_progress_tasks": 0,
                "pending_tasks": 0,
                "completion_rate": 0.0,
                "stage_statistics": {}
            }
        
        completed_tasks = len([t for t in all_tasks if t.status == TaskStatus.COMPLETED])
        in_progress_tasks = len([t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS])
        pending_tasks = len([t for t in all_tasks if t.status == TaskStatus.PENDING])
        
        # 按阶段统计
        stage_stats = {}
        for stage in ProductionStage:
            stage_tasks = self.get_tasks_by_stage(stage)
            stage_completed = len([t for t in stage_tasks if t.status == TaskStatus.COMPLETED])
            stage_stats[stage.value] = {
                "total": len(stage_tasks),
                "completed": stage_completed,
                "completion_rate": stage_completed / len(stage_tasks) if stage_tasks else 0.0
            }
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": completed_tasks / total_tasks,
            "stage_statistics": stage_stats
        }