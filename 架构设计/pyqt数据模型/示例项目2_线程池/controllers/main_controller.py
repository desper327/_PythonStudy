"""
异步控制器 - 使用QThread处理耗时任务
直接创建工作线程处理耗时操作，避免UI阻塞
"""
import time
import json
from typing import Dict, Any
from PyQt5.QtCore import QObject
from models.data_models import Task, TaskStatus
from models.task_repository import TaskRepository
from views.main_view import MainView
from utils.worker_thread import get_simple_task_manager


class MainController(QObject):
    """异步控制器 - 使用QThread处理耗时操作"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化数据仓库
        self.repository = TaskRepository()
        
        # 初始化视图
        self.view = MainView()
        
        # 获取简单任务管理器
        self.task_manager = get_simple_task_manager()
        
        # 连接信号和槽
        self.connect_signals()
        
        # 添加示例数据
        self.add_sample_data()
        
        # 初始化UI统计信息
        self.update_ui_statistics()
        
        print("[MainController] 异步控制器初始化完成")
    
    def connect_signals(self):
        """连接信号和槽"""
        
        # ========== 基础任务管理信号 ==========
        self.view.add_task_requested.connect(self.handle_add_task)
        self.view.delete_task_requested.connect(self.handle_delete_task)
        self.view.update_task_status_requested.connect(self.handle_update_task_status)
        self.view.clear_all_requested.connect(self.handle_clear_all)
        
        # ========== 仓库信号 -> UI更新槽函数 ==========
        self.repository.task_added.connect(self.on_task_added_update_ui)
        self.repository.task_removed.connect(self.on_task_removed_update_ui)
        self.repository.task_updated.connect(self.on_task_updated_update_ui)
        self.repository.tasks_cleared.connect(self.on_tasks_cleared_update_ui)
        
        # ========== 任务管理器信号 ==========
        self.task_manager.task_started.connect(self.on_async_task_started)
        self.task_manager.task_finished.connect(self.on_async_task_finished)
        self.task_manager.task_failed.connect(self.on_async_task_failed)
        self.task_manager.task_progress.connect(self.on_async_task_progress)
    
    # ========== 基础任务管理方法 ==========
    
    def handle_add_task(self, task_data: dict):
        """
        处理添加任务请求 - 可能包含异步验证
        
        Args:
            task_data: 包含任务信息的字典
        """
        try:
            # 检查是否需要异步验证
            if self.should_validate_async(task_data):
                self.validate_and_add_task_async(task_data)
            else:
                # 直接添加任务
                self.add_task_sync(task_data)
                
        except Exception as e:
            self.view.show_message("错误", f"添加任务失败：{str(e)}", "error")
            print(f"[MainController] 添加任务失败: {e}")
    
    def should_validate_async(self, task_data: dict) -> bool:
        """判断是否需要异步验证"""
        name = task_data.get('name', '').lower()
        return '远程' in name or '网络' in name or 'api' in name or '验证' in name
    
    def validate_and_add_task_async(self, task_data: dict):
        """异步验证并添加任务"""
        
        def validation_task():
            """验证任务函数 - 在子线程中执行"""
            print(f"[Worker Thread] 开始验证任务: {task_data.get('name')}")
            
            # 模拟验证过程
            time.sleep(6)  # 模拟网络验证延迟
            
            # 模拟验证逻辑
            name = task_data.get('name', '')
            if len(name) > 50:
                raise ValueError("任务名称过长")
            
            # 模拟检查重复
            existing_tasks = self.repository.get_all_tasks()
            for task in existing_tasks:
                if task.name.lower() == name.lower():
                    raise ValueError(f"任务名称 '{name}' 已存在")
            
            print(f"[Worker Thread] 验证完成: {name}")
            return {"validated": True, "message": "验证通过", "task_data": task_data}
        
        def on_validation_success(result):
            """验证成功回调 - 在主线程中执行"""
            try:
                validated_task_data = result["task_data"]
                self.add_task_sync(validated_task_data)
                self.view.show_message("成功", "任务验证通过并添加成功！")
                print(f"[Main Thread] 验证成功，任务已添加")
            except Exception as e:
                self.view.show_message("错误", f"添加任务失败：{str(e)}", "error")
        
        def on_validation_error(error):
            """验证失败回调 - 在主线程中执行"""
            self.view.show_message("验证失败", f"任务验证失败：{error}", "error")
            print(f"[Main Thread] 验证失败: {error}")
        
        # 启动异步验证任务
        task_id = self.task_manager.run_task(
            validation_task,
            task_id="validate_task",
            on_finished=on_validation_success,
            on_error=on_validation_error
        )
        
        self.view.show_message("信息", "正在验证任务信息，请稍候...")
        print(f"[MainController] 启动验证任务: {task_id}")
    
    def add_task_sync(self, task_data: dict):
        """同步添加任务"""
        task = self.repository.add_task(task_data)
        print(f"[MainController] 同步添加任务: {task.name}")
    
    def handle_delete_task(self, index: int):
        """处理删除任务请求"""
        try:
            task = self.repository.get_task_by_index(index)
            if not task:
                self.view.show_message("错误", "找不到要删除的任务！", "error")
                return
            
            # 检查是否需要异步确认
            if self.should_confirm_delete_async(task):
                self.confirm_and_delete_task_async(index, task)
            else:
                # 直接删除任务
                self.delete_task_sync(index, task)
                
        except Exception as e:
            self.view.show_message("错误", f"删除任务时发生错误：{str(e)}", "error")
            print(f"[MainController] 删除任务失败: {e}")
    
    def should_confirm_delete_async(self, task: Task) -> bool:
        """判断是否需要异步确认删除"""
        return (task.status == TaskStatus.IN_PROGRESS or 
                '重要' in task.name or 
                '关键' in task.name)
    
    def confirm_and_delete_task_async(self, index: int, task: Task):
        """异步确认并删除任务"""
        
        def delete_confirmation_task():
            """删除确认任务 - 在子线程中执行"""
            print(f"[Worker Thread] 开始确认删除: {task.name}")
            
            # 模拟服务器确认延迟
            time.sleep(1.5)
            
            # 模拟确认逻辑
            if task.status == TaskStatus.IN_PROGRESS:
                print(f"[Worker Thread] 确认删除进行中的任务: {task.name}")
            
            print(f"[Worker Thread] 删除确认完成: {task.name}")
            return {"confirmed": True, "message": "删除确认通过", "index": index, "task": task}
        
        def on_confirm_success(result):
            """确认成功回调 - 在主线程中执行"""
            try:
                confirmed_index = result["index"]
                confirmed_task = result["task"]
                self.delete_task_sync(confirmed_index, confirmed_task)
                self.view.show_message("成功", "任务删除确认通过并删除成功！")
                print(f"[Main Thread] 确认成功，任务已删除")
            except Exception as e:
                self.view.show_message("错误", f"删除任务失败：{str(e)}", "error")
        
        def on_confirm_error(error):
            """确认失败回调 - 在主线程中执行"""
            self.view.show_message("确认失败", f"删除确认失败：{error}", "error")
            print(f"[Main Thread] 确认失败: {error}")
        
        # 启动异步确认任务
        task_id = self.task_manager.run_task(
            delete_confirmation_task,
            task_id="confirm_delete",
            on_finished=on_confirm_success,
            on_error=on_confirm_error
        )
        
        self.view.show_message("信息", "正在确认删除操作，请稍候...")
        print(f"[MainController] 启动删除确认任务: {task_id}")
    
    def delete_task_sync(self, index: int, task: Task):
        """同步删除任务"""
        success = self.repository.delete_task(index)
        if success:
            print(f"[MainController] 同步删除任务: {task.name}")
        else:
            raise Exception("删除任务失败")
    
    def handle_update_task_status(self, index: int, status: TaskStatus):
        """处理更新任务状态请求"""
        try:
            task = self.repository.get_task_by_index(index)
            if not task:
                self.view.show_message("错误", "找不到要更新的任务！", "error")
                return
            
            # 检查是否需要异步更新
            if self.should_update_status_async(task, status):
                self.update_task_status_async(index, task, status)
            else:
                # 直接更新状态
                self.update_task_status_sync(index, status)
                
        except Exception as e:
            self.view.show_message("错误", f"更新任务状态时发生错误：{str(e)}", "error")
            print(f"[MainController] 更新任务状态失败: {e}")
    
    def should_update_status_async(self, task: Task, new_status: TaskStatus) -> bool:
        """判断是否需要异步更新状态"""
        return new_status == TaskStatus.COMPLETED
    
    def update_task_status_async(self, index: int, task: Task, status: TaskStatus):
        """异步更新任务状态"""
        
        def status_update_task():
            """状态更新任务 - 在子线程中执行"""
            print(f"[Worker Thread] 开始更新状态: {task.name} -> {status}")
            
            # 模拟服务器通知延迟
            time.sleep(1)
            
            # 模拟状态更新逻辑
            if status == TaskStatus.COMPLETED:
                print(f"[Worker Thread] 处理任务完成: {task.name}")
                return {
                    "updated": True, 
                    "message": "任务完成状态已同步到服务器",
                    "completion_bonus": 10,
                    "index": index,
                    "status": status
                }
            
            return {"updated": True, "message": "状态更新成功", "index": index, "status": status}
        
        def on_update_success(result):
            """更新成功回调 - 在主线程中执行"""
            try:
                updated_index = result["index"]
                updated_status = result["status"]
                self.update_task_status_sync(updated_index, updated_status)
                
                message = result.get('message', '状态更新成功')
                if 'completion_bonus' in result:
                    message += f"，获得奖励积分：{result['completion_bonus']}"
                
                self.view.show_message("成功", message)
                print(f"[Main Thread] 状态更新成功")
            except Exception as e:
                self.view.show_message("错误", f"更新任务状态失败：{str(e)}", "error")
        
        def on_update_error(error):
            """更新失败回调 - 在主线程中执行"""
            self.view.show_message("更新失败", f"状态更新失败：{error}", "error")
            print(f"[Main Thread] 状态更新失败: {error}")
        
        # 启动异步更新任务
        task_id = self.task_manager.run_task(
            status_update_task,
            task_id="update_status",
            on_finished=on_update_success,
            on_error=on_update_error
        )
        
        status_text = self.get_status_text(status)
        self.view.show_message("信息", f"正在更新任务状态为'{status_text}'，请稍候...")
        print(f"[MainController] 启动状态更新任务: {task_id}")
    
    def update_task_status_sync(self, index: int, status: TaskStatus):
        """同步更新任务状态"""
        success = self.repository.update_task(index, {'status': status})
        if not success:
            raise Exception("更新任务状态失败")
    
    def handle_clear_all(self):
        """处理清空所有任务请求"""
        try:
            self.clear_all_tasks_async()
        except Exception as e:
            self.view.show_message("错误", f"清空任务时发生错误：{str(e)}", "error")
            print(f"[MainController] 清空任务失败: {e}")
    
    def clear_all_tasks_async(self):
        """异步清空所有任务"""
        
        def clear_all_task():
            """清空任务 - 在子线程中执行"""
            print("[Worker Thread] 开始清空所有任务")
            
            # 模拟服务器确认延迟
            time.sleep(1)
            
            print("[Worker Thread] 清空确认完成")
            return {"cleared": True, "message": "服务器确认清空所有任务"}
        
        def on_clear_success(result):
            """清空成功回调 - 在主线程中执行"""
            try:
                self.repository.clear_all_tasks()
                self.view.show_message("成功", "所有任务已清空！")
                print("[Main Thread] 清空成功")
            except Exception as e:
                self.view.show_message("错误", f"清空任务失败：{str(e)}", "error")
        
        def on_clear_error(error):
            """清空失败回调 - 在主线程中执行"""
            self.view.show_message("清空失败", f"清空确认失败：{error}", "error")
            print(f"[Main Thread] 清空失败: {error}")
        
        # 启动异步清空任务
        task_id = self.task_manager.run_task(
            clear_all_task,
            task_id="clear_all",
            on_finished=on_clear_success,
            on_error=on_clear_error
        )
        
        self.view.show_message("信息", "正在确认清空操作，请稍候...")
        print(f"[MainController] 启动清空任务: {task_id}")
    
    # ========== 异步任务管理器信号处理 ==========
    
    def on_async_task_started(self, task_id: str):
        """异步任务开始处理"""
        print(f"[MainController] 异步任务开始: {task_id}")
    
    def on_async_task_finished(self, task_id: str, result: Any):
        """异步任务完成处理"""
        print(f"[MainController] 异步任务完成: {task_id}")
    
    def on_async_task_failed(self, task_id: str, error: str):
        """异步任务失败处理"""
        print(f"[MainController] 异步任务失败: {task_id} - {error}")
    
    def on_async_task_progress(self, task_id: str, progress: int, message: str):
        """异步任务进度处理"""
        print(f"[MainController] 异步任务进度: {task_id} - {progress}% - {message}")
    
    # ========== UI更新槽函数 ==========
    
    def on_task_added_update_ui(self, task: Task):
        """槽函数：当仓库添加任务后，更新UI"""
        display_text = self.format_task_display_text(task)
        self.view.add_task_item(display_text, task.id)
        self.update_ui_statistics()
        print(f"[MainController] UI已更新 - 添加任务: {task.name}")
    
    def on_task_removed_update_ui(self, index: int, task: Task):
        """槽函数：当仓库删除任务后，更新UI"""
        self.view.remove_task_item(index)
        self.update_ui_statistics()
        print(f"[MainController] UI已更新 - 删除任务: {task.name} (索引: {index})")
    
    def on_task_updated_update_ui(self, index: int, task: Task):
        """槽函数：当仓库更新任务后，更新UI"""
        display_text = self.format_task_display_text(task)
        self.view.update_task_item(index, display_text)
        self.update_ui_statistics()
        print(f"[MainController] UI已更新 - 更新任务: {task.name} (索引: {index})")
    
    def on_tasks_cleared_update_ui(self):
        """槽函数：当仓库清空所有任务后，更新UI"""
        self.view.clear_task_list()
        self.update_ui_statistics()
        print("[MainController] UI已更新 - 清空所有任务")
    
    # ========== 辅助方法 ==========
    
    def format_task_display_text(self, task: Task) -> str:
        """格式化任务显示文本"""
        status_text = self.get_status_text(task.status)
        created_time = task.created_at.strftime("%m-%d %H:%M")
        
        status_symbol = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅"
        }.get(task.status, "❓")
        
        display_text = f"{status_symbol} [{status_text}] {task.name}"
        
        if task.description:
            desc = task.description[:30] + "..." if len(task.description) > 30 else task.description
            display_text += f" - {desc}"
        
        display_text += f" ({created_time})"
        
        return display_text
    
    def get_status_text(self, status: TaskStatus) -> str:
        """获取状态的中文文本表示"""
        return {
            TaskStatus.PENDING: "待处理",
            TaskStatus.IN_PROGRESS: "进行中",
            TaskStatus.COMPLETED: "已完成"
        }.get(status, "未知")
    
    def update_ui_statistics(self):
        """更新UI中的统计信息"""
        total = self.repository.get_task_count()
        pending = self.repository.get_pending_count()
        in_progress = self.repository.get_in_progress_count()
        completed = self.repository.get_completed_count()
        
        self.view.update_statistics(total, pending, in_progress, completed)
    
    def add_sample_data(self):
        """添加示例数据"""
        sample_tasks = [
            {
                "name": "学习PyQt5异步编程",
                "description": "掌握QThread的使用方法",
                "status": TaskStatus.IN_PROGRESS
            },
            {
                "name": "实现网络验证功能",
                "description": "集成HTTP客户端进行API调用",
                "status": TaskStatus.PENDING
            },
            {
                "name": "优化UI响应性能",
                "description": "使用工作线程避免UI阻塞",
                "status": TaskStatus.COMPLETED
            }
        ]
        
        print("[MainController] 添加示例数据...")
        for task_data in sample_tasks:
            try:
                self.repository.add_task(task_data)
            except Exception as e:
                print(f"[MainController] 添加示例数据失败: {e}")
    
    def show(self):
        """显示主窗口"""
        self.view.show()
        print("[MainController] 异步应用程序已启动")
    
    def cleanup(self):
        """清理资源"""
        # 停止所有活跃任务
        self.task_manager.stop_all_tasks()
        print("[MainController] 资源清理完成")
