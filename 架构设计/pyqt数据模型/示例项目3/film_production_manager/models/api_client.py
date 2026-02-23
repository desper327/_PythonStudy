"""
API客户端模块
负责与后端服务进行网络通信，获取项目数据
"""
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("警告: requests模块未安装，API功能将使用模拟数据")
REQUESTS_AVAILABLE = False
from .data_models import Project, Episode, Scene, Shot, Task, FileInfo, ProductionStage, TaskStatus


class APIClient:
    """API客户端类，处理所有网络请求"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api", timeout: int = 30):
        """
        初始化API客户端
        
        Args:
            base_url: API基础URL
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = None
        
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            
            # 配置重试策略
            retry_strategy = Retry(
                total=3,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["HEAD", "GET", "OPTIONS"],
                backoff_factor=1
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)
            
            # 设置默认请求头
            self.session.headers.update({
                'Content-Type': 'application/json',
                'User-Agent': 'FilmProductionManager/1.0'
            })
        else:
            print("API客户端将使用模拟数据模式")
    
    def set_auth_token(self, token: str):
        """设置认证令牌"""
        if self.session:
            self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发起HTTP请求的通用方法
        
        Args:
            method: HTTP方法
            endpoint: API端点
            **kwargs: 其他请求参数
            
        Returns:
            响应数据字典
            
        Raises:
            requests.RequestException: 网络请求异常
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if not REQUESTS_AVAILABLE or not self.session:
            # 使用模拟数据
            time.sleep(0.5)  # 模拟网络延迟
            return self._get_mock_response(endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            
            # 模拟网络延迟（实际项目中应移除）
            time.sleep(0.5)
            
            return response.json()
            
        except Exception as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def get_projects(self) -> List[Project]:
        """
        获取所有项目列表
        
        Returns:
            项目列表
        """
        try:
            if REQUESTS_AVAILABLE and self.session:
                # 实际API调用
                data = self._make_request('GET', '/projects')
            else:
                # 模拟数据
                data = self._get_mock_projects_data()
            
            projects = []
            for project_data in data.get('projects', []):
                project = self._parse_project_data(project_data)
                projects.append(project)
            
            return projects
            
        except Exception as e:
            print(f"获取项目列表失败: {e}")
            return []
    
    def get_project_details(self, project_id: str) -> Optional[Project]:
        """
        获取项目详细信息
        
        Args:
            project_id: 项目ID
            
        Returns:
            项目对象或None
        """
        try:
            if REQUESTS_AVAILABLE and self.session:
                # 实际API调用
                data = self._make_request('GET', f'/projects/{project_id}')
            else:
                # 模拟数据
                data = self._get_mock_project_details(project_id)
            
            if data:
                return self._parse_project_data(data)
            return None
            
        except Exception as e:
            print(f"获取项目详情失败: {e}")
            return None
    
    def get_tasks_by_filters(self, project_id: str, episode_id: str = None, 
                           scene_id: str = None, shot_id: str = None, 
                           stage: ProductionStage = None) -> List[Task]:
        """
        根据过滤条件获取任务列表
        
        Args:
            project_id: 项目ID
            episode_id: 集ID（可选）
            scene_id: 场ID（可选）
            shot_id: 镜头ID（可选）
            stage: 制作阶段（可选）
            
        Returns:
            任务列表
        """
        try:
            params = {'project_id': project_id}
            if episode_id:
                params['episode_id'] = episode_id
            if scene_id:
                params['scene_id'] = scene_id
            if shot_id:
                params['shot_id'] = shot_id
            if stage:
                params['stage'] = stage.value
            
            if REQUESTS_AVAILABLE and self.session:
                # 实际API调用
                data = self._make_request('GET', '/tasks', params=params)
            else:
                # 模拟数据
                data = self._get_mock_tasks_data(params)
            
            tasks = []
            for task_data in data.get('tasks', []):
                task = self._parse_task_data(task_data)
                tasks.append(task)
            
            return tasks
            
        except Exception as e:
            print(f"获取任务列表失败: {e}")
            return []
    
    def get_file_info(self, file_id: str) -> Optional[FileInfo]:
        """
        获取文件信息
        
        Args:
            file_id: 文件ID
            
        Returns:
            文件信息对象或None
        """
        try:
            if REQUESTS_AVAILABLE and self.session:
                # 实际API调用
                data = self._make_request('GET', f'/files/{file_id}')
            else:
                # 模拟数据
                data = self._get_mock_file_info(file_id)
            
            if data:
                return self._parse_file_data(data)
            return None
            
        except Exception as e:
            print(f"获取文件信息失败: {e}")
            return None
    
    def update_task_status(self, task_id: str, status: TaskStatus, progress: float = None) -> bool:
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            progress: 进度（0.0-1.0）
            
        Returns:
            是否成功
        """
        try:
            data = {'status': status.value}
            if progress is not None:
                data['progress'] = progress
            
            if REQUESTS_AVAILABLE and self.session:
                # 实际API调用
                result = self._make_request('PUT', f'/tasks/{task_id}', json=data)
            else:
                # 模拟成功
                print(f"任务 {task_id} 状态更新为: {status.value}")
            
            return True
            
        except Exception as e:
            print(f"更新任务状态失败: {e}")
            return False
    
    def _parse_project_data(self, data: Dict[str, Any]) -> Project:
        """解析项目数据"""
        episodes = []
        for ep_data in data.get('episodes', []):
            episode = self._parse_episode_data(ep_data)
            episodes.append(episode)
        
        return Project(
            project_id=data['project_id'],
            project_name=data['project_name'],
            description=data.get('description', ''),
            created_time=datetime.fromisoformat(data['created_time']),
            episodes=episodes,
            metadata=data.get('metadata', {})
        )
    
    def _parse_episode_data(self, data: Dict[str, Any]) -> Episode:
        """解析集数据"""
        scenes = []
        for scene_data in data.get('scenes', []):
            scene = self._parse_scene_data(scene_data)
            scenes.append(scene)
        
        return Episode(
            episode_id=data['episode_id'],
            episode_name=data['episode_name'],
            episode_number=data['episode_number'],
            description=data.get('description', ''),
            scenes=scenes,
            metadata=data.get('metadata', {})
        )
    
    def _parse_scene_data(self, data: Dict[str, Any]) -> Scene:
        """解析场数据"""
        shots = []
        for shot_data in data.get('shots', []):
            shot = self._parse_shot_data(shot_data)
            shots.append(shot)
        
        return Scene(
            scene_id=data['scene_id'],
            scene_name=data['scene_name'],
            scene_number=data['scene_number'],
            description=data.get('description', ''),
            shots=shots,
            metadata=data.get('metadata', {})
        )
    
    def _parse_shot_data(self, data: Dict[str, Any]) -> Shot:
        """解析镜头数据"""
        tasks = []
        for task_data in data.get('tasks', []):
            task = self._parse_task_data(task_data)
            tasks.append(task)
        
        return Shot(
            shot_id=data['shot_id'],
            shot_name=data['shot_name'],
            shot_number=data['shot_number'],
            description=data.get('description', ''),
            duration=data.get('duration', 0.0),
            frame_start=data.get('frame_start', 1),
            frame_end=data.get('frame_end', 1),
            frame_rate=data.get('frame_rate', 24.0),
            tasks=tasks,
            metadata=data.get('metadata', {})
        )
    
    def _parse_task_data(self, data: Dict[str, Any]) -> Task:
        """解析任务数据"""
        files = []
        for file_data in data.get('files', []):
            file_info = self._parse_file_data(file_data)
            files.append(file_info)
        
        return Task(
            task_id=data['task_id'],
            task_name=data['task_name'],
            stage=ProductionStage(data['stage']),
            status=TaskStatus(data['status']),
            assignee=data['assignee'],
            created_time=datetime.fromisoformat(data['created_time']),
            due_time=datetime.fromisoformat(data['due_time']) if data.get('due_time') else None,
            completed_time=datetime.fromisoformat(data['completed_time']) if data.get('completed_time') else None,
            description=data.get('description', ''),
            priority=data.get('priority', 1),
            progress=data.get('progress', 0.0),
            files=files,
            metadata=data.get('metadata', {})
        )
    
    def _parse_file_data(self, data: Dict[str, Any]) -> FileInfo:
        """解析文件数据"""
        return FileInfo(
            file_id=data['file_id'],
            file_name=data['file_name'],
            file_path=data['file_path'],
            file_size=data['file_size'],
            file_type=data['file_type'],
            created_time=datetime.fromisoformat(data['created_time']),
            modified_time=datetime.fromisoformat(data['modified_time']),
            version=data.get('version', '1.0'),
            description=data.get('description', '')
        )
    
    def _get_mock_response(self, endpoint: str) -> Dict[str, Any]:
        """根据端点返回模拟响应数据"""
        if endpoint.startswith('/projects') and '/' not in endpoint[10:]:
            return self._get_mock_projects_data()
        elif endpoint.startswith('/projects/') and endpoint.count('/') == 2:
            project_id = endpoint.split('/')[-1]
            return self._get_mock_project_details(project_id)
        elif endpoint.startswith('/tasks'):
            return self._get_mock_tasks_data({})
        elif endpoint.startswith('/files/'):
            file_id = endpoint.split('/')[-1]
            return self._get_mock_file_info(file_id)
        else:
            return {}
    
    # 以下为模拟数据方法，实际项目中应移除
    def _get_mock_projects_data(self) -> Dict[str, Any]:
        """获取模拟项目数据"""
        return {
            "projects": [
                {
                    "project_id": "proj_001",
                    "project_name": "《魔法森林》动画电影",
                    "description": "一部关于魔法森林冒险的3D动画电影",
                    "created_time": "2024-01-01T00:00:00",
                    "episodes": [],
                    "metadata": {"budget": 5000000, "target_audience": "family"}
                },
                {
                    "project_id": "proj_002", 
                    "project_name": "《未来都市》系列动画",
                    "description": "科幻题材的系列动画作品",
                    "created_time": "2024-02-01T00:00:00",
                    "episodes": [],
                    "metadata": {"season": 1, "episodes_count": 12}
                }
            ]
        }
    
    def _get_mock_project_details(self, project_id: str) -> Dict[str, Any]:
        """获取模拟项目详情"""
        if project_id == "proj_001":
            return {
                "project_id": "proj_001",
                "project_name": "《魔法森林》动画电影",
                "description": "一部关于魔法森林冒险的3D动画电影",
                "created_time": "2024-01-01T00:00:00",
                "episodes": [
                    {
                        "episode_id": "ep_001",
                        "episode_name": "第一集：森林的秘密",
                        "episode_number": "01",
                        "description": "主角发现魔法森林的入口",
                        "scenes": [
                            {
                                "scene_id": "sc_001",
                                "scene_name": "开场场景",
                                "scene_number": "001",
                                "description": "主角在家中的日常生活",
                                "shots": [
                                    {
                                        "shot_id": "sh_001",
                                        "shot_name": "主角起床镜头",
                                        "shot_number": "001",
                                        "description": "主角从床上起来",
                                        "duration": 3.5,
                                        "frame_start": 1,
                                        "frame_end": 84,
                                        "frame_rate": 24.0,
                                        "tasks": [
                                            {
                                                "task_id": "task_001",
                                                "task_name": "角色动画制作",
                                                "stage": "动画",
                                                "status": "进行中",
                                                "assignee": "张三",
                                                "created_time": "2024-11-01T09:00:00",
                                                "due_time": "2024-11-20T18:00:00",
                                                "description": "制作主角起床的动画序列",
                                                "priority": 3,
                                                "progress": 0.6,
                                                "files": [
                                                    {
                                                        "file_id": "file_001",
                                                        "file_name": "character_animation_v1.ma",
                                                        "file_path": "/projects/proj_001/animation/character_animation_v1.ma",
                                                        "file_size": 2048576,
                                                        "file_type": "maya",
                                                        "created_time": "2024-11-01T10:00:00",
                                                        "modified_time": "2024-11-15T16:30:00",
                                                        "version": "1.3",
                                                        "description": "角色动画文件"
                                                    }
                                                ],
                                                "metadata": {"complexity": "medium"}
                                            }
                                        ],
                                        "metadata": {}
                                    }
                                ],
                                "metadata": {}
                            }
                        ],
                        "metadata": {}
                    }
                ],
                "metadata": {"budget": 5000000, "target_audience": "family"}
            }
        return None
    
    def _get_mock_tasks_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取模拟任务数据"""
        return {
            "tasks": [
                {
                    "task_id": "task_001",
                    "task_name": "角色动画制作",
                    "stage": "动画",
                    "status": "进行中",
                    "assignee": "张三",
                    "created_time": "2024-11-01T09:00:00",
                    "due_time": "2024-11-20T18:00:00",
                    "description": "制作主角起床的动画序列",
                    "priority": 3,
                    "progress": 0.6,
                    "files": [],
                    "metadata": {"complexity": "medium"}
                }
            ]
        }
    
    def _get_mock_file_info(self, file_id: str) -> Dict[str, Any]:
        """获取模拟文件信息"""
        return {
            "file_id": file_id,
            "file_name": "character_animation_v1.ma",
            "file_path": f"/projects/files/{file_id}.ma",
            "file_size": 2048576,
            "file_type": "maya",
            "created_time": "2024-11-01T10:00:00",
            "modified_time": "2024-11-15T16:30:00",
            "version": "1.3",
            "description": "角色动画文件"
        }
    
    def get_mock_mode_status(self) -> bool:
        """获取是否为模拟模式"""
        return not REQUESTS_AVAILABLE or not self.session