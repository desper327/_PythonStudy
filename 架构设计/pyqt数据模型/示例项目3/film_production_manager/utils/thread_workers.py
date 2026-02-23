"""
线程工作器模块
提供各种异步任务的线程工作器类
"""
import os
import time
from typing import List, Dict, Any, Optional, Callable
from PySide6.QtCore import QThread, Signal, QObject, QMutex, QWaitCondition
from PySide6.QtWidgets import QApplication

from ..models.api_client import APIClient
from ..models.data_models import Project, Task, FileInfo, ProductionStage


class BaseWorker(QObject):
    """基础工作器类"""
    
    # 通用信号
    started = Signal()  # 开始信号
    finished = Signal()  # 完成信号
    error = Signal(str)  # 错误信号
    progress = Signal(int)  # 进度信号 (0-100)
    status_changed = Signal(str)  # 状态变化信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_cancelled = False
        self._mutex = QMutex()
        self._wait_condition = QWaitCondition()
    
    def cancel(self):
        """取消任务"""
        self._mutex.lock()
        self._is_cancelled = True
        self._wait_condition.wakeAll()
        self._mutex.unlock()
    
    def is_cancelled(self) -> bool:
        """检查是否被取消"""
        self._mutex.lock()
        cancelled = self._is_cancelled
        self._mutex.unlock()
        return cancelled
    
    def emit_progress(self, value: int, status: str = ""):
        """发射进度信号"""
        self.progress.emit(value)
        if status:
            self.status_changed.emit(status)


class ProjectDataWorker(BaseWorker):
    """项目数据获取工作器"""
    
    # 专用信号
    projects_loaded = Signal(list)  # 项目列表加载完成
    project_details_loaded = Signal(object)  # 项目详情加载完成
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.operation_type = None
        self.project_id = None
    
    def load_projects(self):
        """加载项目列表"""
        self.operation_type = "load_projects"
        
    def load_project_details(self, project_id: str):
        """加载项目详情"""
        self.operation_type = "load_project_details"
        self.project_id = project_id
    
    def run(self):
        """执行工作"""
        try:
            self.started.emit()
            
            if self.operation_type == "load_projects":
                self._load_projects()
            elif self.operation_type == "load_project_details":
                self._load_project_details()
            
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"数据加载失败: {str(e)}")
    
    def _load_projects(self):
        """内部方法：加载项目列表"""
        self.emit_progress(10, "正在连接服务器...")
        
        if self.is_cancelled():
            return
        
        self.emit_progress(30, "正在获取项目列表...")
        projects = self.api_client.get_projects()
        
        if self.is_cancelled():
            return
        
        self.emit_progress(80, "正在处理数据...")
        # 模拟处理时间
        time.sleep(0.5)
        
        self.emit_progress(100, "加载完成")
        self.projects_loaded.emit(projects)
    
    def _load_project_details(self):
        """内部方法：加载项目详情"""
        self.emit_progress(10, f"正在获取项目详情...")
        
        if self.is_cancelled():
            return
        
        self.emit_progress(50, "正在解析项目数据...")
        project = self.api_client.get_project_details(self.project_id)
        
        if self.is_cancelled():
            return
        
        self.emit_progress(100, "项目详情加载完成")
        self.project_details_loaded.emit(project)


class TaskDataWorker(BaseWorker):
    """任务数据获取工作器"""
    
    # 专用信号
    tasks_loaded = Signal(list)  # 任务列表加载完成
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.project_id = None
        self.episode_id = None
        self.scene_id = None
        self.shot_id = None
        self.stage = None
    
    def load_tasks(self, project_id: str, episode_id: str = None, 
                   scene_id: str = None, shot_id: str = None, 
                   stage: ProductionStage = None):
        """设置任务加载参数"""
        self.project_id = project_id
        self.episode_id = episode_id
        self.scene_id = scene_id
        self.shot_id = shot_id
        self.stage = stage
    
    def run(self):
        """执行任务加载"""
        try:
            self.started.emit()
            self.emit_progress(10, "正在获取任务列表...")
            
            if self.is_cancelled():
                return
            
            tasks = self.api_client.get_tasks_by_filters(
                project_id=self.project_id,
                episode_id=self.episode_id,
                scene_id=self.scene_id,
                shot_id=self.shot_id,
                stage=self.stage
            )
            
            if self.is_cancelled():
                return
            
            self.emit_progress(100, "任务列表加载完成")
            self.tasks_loaded.emit(tasks)
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"任务加载失败: {str(e)}")


class FileProcessWorker(BaseWorker):
    """文件处理工作器"""
    
    # 专用信号
    file_processed = Signal(object)  # 单个文件处理完成
    all_files_processed = Signal(list)  # 所有文件处理完成
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.file_ids = []
        self.process_function = None
    
    def process_files(self, file_ids: List[str], process_function: Callable = None):
        """设置文件处理参数"""
        self.file_ids = file_ids
        self.process_function = process_function or self._default_file_processor
    
    def run(self):
        """执行文件处理"""
        try:
            self.started.emit()
            processed_files = []
            total_files = len(self.file_ids)
            
            for i, file_id in enumerate(self.file_ids):
                if self.is_cancelled():
                    return
                
                progress = int((i / total_files) * 100)
                self.emit_progress(progress, f"正在处理文件 {i+1}/{total_files}")
                
                # 获取文件信息
                file_info = self.api_client.get_file_info(file_id)
                if file_info:
                    # 处理文件
                    processed_file = self.process_function(file_info)
                    processed_files.append(processed_file)
                    self.file_processed.emit(processed_file)
                
                # 模拟处理时间
                time.sleep(0.1)
            
            self.emit_progress(100, "所有文件处理完成")
            self.all_files_processed.emit(processed_files)
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"文件处理失败: {str(e)}")
    
    def _default_file_processor(self, file_info: FileInfo) -> Dict[str, Any]:
        """默认文件处理器"""
        # 模拟文件读取和处理
        result = {
            "file_id": file_info.file_id,
            "file_name": file_info.file_name,
            "file_size": file_info.file_size,
            "processed_time": time.time(),
            "status": "processed"
        }
        
        # 根据文件类型进行不同处理
        if file_info.file_type == "maya":
            result["maya_version"] = "2024"
            result["scene_objects"] = ["camera", "light", "mesh"]
        elif file_info.file_type == "image":
            result["resolution"] = "1920x1080"
            result["color_space"] = "sRGB"
        
        return result


class BatchTaskWorker(BaseWorker):
    """批量任务处理工作器"""
    
    # 专用信号
    task_completed = Signal(str, bool)  # 单个任务完成 (task_id, success)
    batch_completed = Signal(dict)  # 批量任务完成 (统计信息)
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.tasks = []
        self.operation = None
    
    def update_task_statuses(self, task_updates: List[Dict[str, Any]]):
        """批量更新任务状态"""
        self.tasks = task_updates
        self.operation = "update_statuses"
    
    def run(self):
        """执行批量任务"""
        try:
            self.started.emit()
            
            if self.operation == "update_statuses":
                self._update_task_statuses()
            
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"批量任务处理失败: {str(e)}")
    
    def _update_task_statuses(self):
        """批量更新任务状态"""
        total_tasks = len(self.tasks)
        success_count = 0
        failed_count = 0
        
        for i, task_update in enumerate(self.tasks):
            if self.is_cancelled():
                return
            
            progress = int((i / total_tasks) * 100)
            task_id = task_update.get('task_id')
            self.emit_progress(progress, f"正在更新任务 {i+1}/{total_tasks}")
            
            try:
                success = self.api_client.update_task_status(
                    task_id=task_id,
                    status=task_update.get('status'),
                    progress=task_update.get('progress')
                )
                
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                
                self.task_completed.emit(task_id, success)
                
            except Exception as e:
                failed_count += 1
                self.task_completed.emit(task_id, False)
                print(f"更新任务 {task_id} 失败: {e}")
            
            # 模拟处理时间
            time.sleep(0.1)
        
        # 发送完成统计
        stats = {
            "total": total_tasks,
            "success": success_count,
            "failed": failed_count,
            "success_rate": success_count / total_tasks if total_tasks > 0 else 0
        }
        
        self.emit_progress(100, "批量更新完成")
        self.batch_completed.emit(stats)


class ThreadManager(QObject):
    """线程管理器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_threads = {}
        self.api_client = None
    
    def set_api_client(self, api_client: APIClient):
        """设置API客户端"""
        self.api_client = api_client
    
    def start_project_data_worker(self, worker_id: str = "project_data") -> ProjectDataWorker:
        """启动项目数据工作器"""
        if worker_id in self.active_threads:
            self.stop_worker(worker_id)
        
        thread = QThread()
        worker = ProjectDataWorker(self.api_client)
        worker.moveToThread(thread)
        
        # 连接信号
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        
        # 清理完成后从活动线程中移除
        thread.finished.connect(lambda: self._remove_thread(worker_id))
        
        self.active_threads[worker_id] = {"thread": thread, "worker": worker}
        thread.start()
        
        return worker
    
    def start_task_data_worker(self, worker_id: str = "task_data") -> TaskDataWorker:
        """启动任务数据工作器"""
        if worker_id in self.active_threads:
            self.stop_worker(worker_id)
        
        thread = QThread()
        worker = TaskDataWorker(self.api_client)
        worker.moveToThread(thread)
        
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: self._remove_thread(worker_id))
        
        self.active_threads[worker_id] = {"thread": thread, "worker": worker}
        thread.start()
        
        return worker
    
    def start_file_process_worker(self, worker_id: str = "file_process") -> FileProcessWorker:
        """启动文件处理工作器"""
        if worker_id in self.active_threads:
            self.stop_worker(worker_id)
        
        thread = QThread()
        worker = FileProcessWorker(self.api_client)
        worker.moveToThread(thread)
        
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: self._remove_thread(worker_id))
        
        self.active_threads[worker_id] = {"thread": thread, "worker": worker}
        thread.start()
        
        return worker
    
    def start_batch_task_worker(self, worker_id: str = "batch_task") -> BatchTaskWorker:
        """启动批量任务工作器"""
        if worker_id in self.active_threads:
            self.stop_worker(worker_id)
        
        thread = QThread()
        worker = BatchTaskWorker(self.api_client)
        worker.moveToThread(thread)
        
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: self._remove_thread(worker_id))
        
        self.active_threads[worker_id] = {"thread": thread, "worker": worker}
        thread.start()
        
        return worker
    
    def stop_worker(self, worker_id: str):
        """停止指定工作器"""
        if worker_id in self.active_threads:
            thread_info = self.active_threads[worker_id]
            worker = thread_info["worker"]
            thread = thread_info["thread"]
            
            # 取消工作器
            worker.cancel()
            
            # 等待线程结束
            if thread.isRunning():
                thread.quit()
                thread.wait(3000)  # 等待3秒
                
                if thread.isRunning():
                    thread.terminate()
                    thread.wait(1000)
    
    def stop_all_workers(self):
        """停止所有工作器"""
        worker_ids = list(self.active_threads.keys())
        for worker_id in worker_ids:
            self.stop_worker(worker_id)
    
    def _remove_thread(self, worker_id: str):
        """从活动线程中移除"""
        if worker_id in self.active_threads:
            del self.active_threads[worker_id]
    
    def get_active_workers(self) -> List[str]:
        """获取活动工作器列表"""
        return list(self.active_threads.keys())
    
    def is_worker_active(self, worker_id: str) -> bool:
        """检查工作器是否活动"""
        return worker_id in self.active_threads