"""
增强版主控制器 - 集成异步任务处理能力
演示如何在MVC架构中正确使用线程池处理耗时操作
"""
import time
import json
from typing import List, Dict, Any
from PyQt5.QtCore import QObject
from models.data_models import Task, TaskStatus
from models.task_repository import TaskRepository
from views.enhanced_main_view import EnhancedMainView
from utils.async_task_manager import get_task_manager


class EnhancedMainController(QObject):
    """增强版主控制器 - 支持异步任务处理"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化数据仓库
        self.repository = TaskRepository()
        
        # 初始化增强版视图
        self.view = EnhancedMainView()
        
        # 获取任务管理器
        self.task_manager = get_task_manager()
        
        # 连接信号和槽
        self.connect_signals()
        
        # 添加示例数据
        self.add_sample_data()
        
        # 初始化UI统计信息
        self.update_ui_statistics()
        
        print("[EnhancedController] 增强版控制器初始化完成")
    
    def connect_signals(self):
        """连接视图信号到控制器方法，连接仓库信号到UI更新方法"""
        
        # ========== 基础任务管理信号 ==========
        self.view.add_task_requested.connect(self.handle_add_task)
        self.view.delete_task_requested.connect(self.handle_delete_task)
        self.view.update_task_status_requested.connect(self.handle_update_task_status)
        self.view.clear_all_requested.connect(self.handle_clear_all)
        
        # ========== 异步操作信号 ==========
        self.view.fetch_remote_tasks_requested.connect(self.handle_fetch_remote_tasks)
        self.view.sync_tasks_requested.connect(self.handle_sync_tasks)
        self.view.export_tasks_requested.connect(self.handle_export_tasks)
        
        # ========== 仓库信号 -> UI更新槽函数 ==========
        self.repository.task_added.connect(self.on_task_added_update_ui)
        self.repository.task_removed.connect(self.on_task_removed_update_ui)
        self.repository.task_updated.connect(self.on_task_updated_update_ui)
        self.repository.tasks_cleared.connect(self.on_tasks_cleared_update_ui)
    
    # ========== 基础任务管理方法 ==========
    
    def handle_add_task(self, task_data: dict):
        """
        处理添加任务请求 - 可能包含异步验证
        
        Args:
            task_data: 包含任务信息的字典
        """
        try:
            # 检查是否需要异步验证（例如检查任务名称是否重复）
            if self.should_validate_async(task_data):
                self.validate_and_add_task_async(task_data)
            else:
                # 直接添加任务
                self.add_task_sync(task_data)
                
        except Exception as e:
            self.view.show_message("错误", f"添加任务失败：{str(e)}", "error")
            print(f"[EnhancedController] 添加任务失败: {e}")
    
    def should_validate_async(self, task_data: dict) -> bool:
        """
        判断是否需要异步验证
        
        Args:
            task_data: 任务数据
            
        Returns:
            bool: 是否需要异步验证
        """
        # 示例：如果任务名称包含"远程"或"网络"，则需要异步验证
        name = task_data.get('name', '').lower()
        return '远程' in name or '网络' in name or 'api' in name
    
    def validate_and_add_task_async(self, task_data: dict):
        """
        异步验证并添加任务
        
        Args:
            task_data: 任务数据
        """
        def async_validation():
            """模拟异步验证过程"""
            time.sleep(2)  # 模拟网络验证延迟
            
            # 模拟验证逻辑
            name = task_data.get('name', '')
            if len(name) > 50:
                raise ValueError("任务名称过长")
            
            # 模拟检查重复
            existing_tasks = self.repository.get_all_tasks()
            for task in existing_tasks:
                if task.name.lower() == name.lower():
                    raise ValueError(f"任务名称 '{name}' 已存在")
            
            return {"validated": True, "message": "验证通过"}
        
        def on_validation_success(result):
            """验证成功回调"""
            try:
                self.add_task_sync(task_data)
                self.view.show_message("成功", "任务验证通过并添加成功！")
            except Exception as e:
                self.view.show_message("错误", f"添加任务失败：{str(e)}", "error")
        
        def on_validation_error(error):
            """验证失败回调"""
            self.view.show_message("验证失败", f"任务验证失败：{error}", "error")
        
        # 异步执行验证
        self.task_manager.run_async(
            async_validation,
            task_id="validate_task",
            on_finished=on_validation_success,
            on_error=on_validation_error
        )
        
        self.view.show_message("信息", "正在验证任务信息，请稍候...")
    
    def add_task_sync(self, task_data: dict):
        """
        同步添加任务
        
        Args:
            task_data: 任务数据
        """
        task = self.repository.add_task(task_data)
        print(f"[EnhancedController] 同步添加任务: {task.name}")
    
    def handle_delete_task(self, index: int):
        """
        处理删除任务请求 - 可能包含异步确认
        
        Args:
            index: 要删除的任务索引
        """
        try:
            task = self.repository.get_task_by_index(index)
            if not task:
                self.view.show_message("错误", "找不到要删除的任务！", "error")
                return
            
            # 检查是否需要异步确认（例如重要任务需要服务器确认）
            if self.should_confirm_delete_async(task):
                self.confirm_and_delete_task_async(index, task)
            else:
                # 直接删除任务
                self.delete_task_sync(index, task)
                
        except Exception as e:
            self.view.show_message("错误", f"删除任务时发生错误：{str(e)}", "error")
            print(f"[EnhancedController] 删除任务失败: {e}")
    
    def should_confirm_delete_async(self, task: Task) -> bool:
        """
        判断是否需要异步确认删除
        
        Args:
            task: 任务对象
            
        Returns:
            bool: 是否需要异步确认
        """
        # 示例：进行中的任务或包含"重要"的任务需要异步确认
        return (task.status == TaskStatus.IN_PROGRESS or 
                '重要' in task.name or 
                '关键' in task.name)
    
    def confirm_and_delete_task_async(self, index: int, task: Task):
        """
        异步确认并删除任务
        
        Args:
            index: 任务索引
            task: 任务对象
        """
        def async_delete_confirmation():
            """模拟异步删除确认"""
            time.sleep(1.5)  # 模拟服务器确认延迟
            
            # 模拟服务器确认逻辑
            if task.status == TaskStatus.IN_PROGRESS:
                # 需要额外确认
                return {"confirmed": True, "message": "服务器确认删除进行中的任务"}
            
            return {"confirmed": True, "message": "删除确认通过"}
        
        def on_confirm_success(result):
            """确认成功回调"""
            try:
                self.delete_task_sync(index, task)
                self.view.show_message("成功", "任务删除确认通过并删除成功！")
            except Exception as e:
                self.view.show_message("错误", f"删除任务失败：{str(e)}", "error")
        
        def on_confirm_error(error):
            """确认失败回调"""
            self.view.show_message("确认失败", f"删除确认失败：{error}", "error")
        
        # 异步执行确认
        self.task_manager.run_async(
            async_delete_confirmation,
            task_id="confirm_delete",
            on_finished=on_confirm_success,
            on_error=on_confirm_error
        )
        
        self.view.show_message("信息", "正在确认删除操作，请稍候...")
    
    def delete_task_sync(self, index: int, task: Task):
        """
        同步删除任务
        
        Args:
            index: 任务索引
            task: 任务对象
        """
        success = self.repository.delete_task(index)
        if success:
            print(f"[EnhancedController] 同步删除任务: {task.name}")
        else:
            raise Exception("删除任务失败")
    
    def handle_update_task_status(self, index: int, status: TaskStatus):
        """
        处理更新任务状态请求
        
        Args:
            index: 任务索引
            status: 新的任务状态
        """
        try:
            task = self.repository.get_task_by_index(index)
            if not task:
                self.view.show_message("错误", "找不到要更新的任务！", "error")
                return
            
            # 检查是否需要异步更新（例如状态变更需要通知服务器）
            if self.should_update_status_async(task, status):
                self.update_task_status_async(index, task, status)
            else:
                # 直接更新状态
                self.update_task_status_sync(index, status)
                
        except Exception as e:
            self.view.show_message("错误", f"更新任务状态时发生错误：{str(e)}", "error")
            print(f"[EnhancedController] 更新任务状态失败: {e}")
    
    def should_update_status_async(self, task: Task, new_status: TaskStatus) -> bool:
        """
        判断是否需要异步更新状态
        
        Args:
            task: 任务对象
            new_status: 新状态
            
        Returns:
            bool: 是否需要异步更新
        """
        # 示例：标记为完成的任务需要异步通知
        return new_status == TaskStatus.COMPLETED
    
    def update_task_status_async(self, index: int, task: Task, status: TaskStatus):
        """
        异步更新任务状态
        
        Args:
            index: 任务索引
            task: 任务对象
            status: 新状态
        """
        def async_status_update():
            """模拟异步状态更新"""
            time.sleep(1)  # 模拟服务器通知延迟
            
            # 模拟服务器通知逻辑
            if status == TaskStatus.COMPLETED:
                # 模拟完成任务的额外处理
                return {
                    "updated": True, 
                    "message": "任务完成状态已同步到服务器",
                    "completion_bonus": 10
                }
            
            return {"updated": True, "message": "状态更新成功"}
        
        def on_update_success(result):
            """更新成功回调"""
            try:
                self.update_task_status_sync(index, status)
                message = result.get('message', '状态更新成功')
                if 'completion_bonus' in result:
                    message += f"，获得奖励积分：{result['completion_bonus']}"
                self.view.show_message("成功", message)
            except Exception as e:
                self.view.show_message("错误", f"更新任务状态失败：{str(e)}", "error")
        
        def on_update_error(error):
            """更新失败回调"""
            self.view.show_message("更新失败", f"状态更新失败：{error}", "error")
        
        # 异步执行更新
        self.task_manager.run_async(
            async_status_update,
            task_id="update_status",
            on_finished=on_update_success,
            on_error=on_update_error
        )
        
        status_text = self.get_status_text(status)
        self.view.show_message("信息", f"正在更新任务状态为'{status_text}'，请稍候...")
    
    def update_task_status_sync(self, index: int, status: TaskStatus):
        """
        同步更新任务状态
        
        Args:
            index: 任务索引
            status: 新状态
        """
        success = self.repository.update_task(index, {'status': status})
        if not success:
            raise Exception("更新任务状态失败")
    
    def handle_clear_all(self):
        """处理清空所有任务请求"""
        try:
            # 清空操作通常需要异步确认
            self.clear_all_tasks_async()
        except Exception as e:
            self.view.show_message("错误", f"清空任务时发生错误：{str(e)}", "error")
            print(f"[EnhancedController] 清空任务失败: {e}")
    
    def clear_all_tasks_async(self):
        """异步清空所有任务"""
        def async_clear_all():
            """模拟异步清空确认"""
            time.sleep(1)  # 模拟服务器确认延迟
            return {"cleared": True, "message": "服务器确认清空所有任务"}
        
        def on_clear_success(result):
            """清空成功回调"""
            try:
                self.repository.clear_all_tasks()
                self.view.show_message("成功", "所有任务已清空！")
            except Exception as e:
                self.view.show_message("错误", f"清空任务失败：{str(e)}", "error")
        
        def on_clear_error(error):
            """清空失败回调"""
            self.view.show_message("清空失败", f"清空确认失败：{error}", "error")
        
        # 异步执行清空
        self.task_manager.run_async(
            async_clear_all,
            task_id="clear_all",
            on_finished=on_clear_success,
            on_error=on_clear_error
        )
        
        self.view.show_message("信息", "正在确认清空操作，请稍候...")
    
    # ========== 异步操作处理方法 ==========
    
    def handle_fetch_remote_tasks(self):
        """处理获取远程任务请求"""
        def fetch_from_api():
            """模拟从API获取任务"""
            time.sleep(3)  # 模拟网络延迟
            
            # 模拟API响应
            api_tasks = [
                {
                    "name": f"API任务 {int(time.time()) % 1000}",
                    "description": "从API获取的任务数据",
                    "status": TaskStatus.PENDING
                },
                {
                    "name": f"同步任务 {int(time.time()) % 1000}",
                    "description": "需要处理的重要任务",
                    "status": TaskStatus.IN_PROGRESS
                }
            ]
            
            return {"tasks": api_tasks, "total": len(api_tasks)}
        
        def on_fetch_success(result):
            """获取成功回调"""
            tasks = result.get('tasks', [])
            total = result.get('total', 0)
            
            # 添加获取到的任务
            for task_data in tasks:
                try:
                    self.repository.add_task(task_data)
                except Exception as e:
                    print(f"[EnhancedController] 添加远程任务失败: {e}")
            
            self.view.show_message("成功", f"成功获取并添加了 {total} 个远程任务！")
        
        def on_fetch_error(error):
            """获取失败回调"""
            self.view.show_message("错误", f"获取远程任务失败：{error}", "error")
        
        # 异步获取远程任务
        self.task_manager.run_async(
            fetch_from_api,
            task_id="fetch_remote_tasks",
            on_finished=on_fetch_success,
            on_error=on_fetch_error
        )
        
        print("[EnhancedController] 开始获取远程任务...")
    
    def handle_sync_tasks(self):
        """处理同步任务到服务器请求"""
        def sync_to_server():
            """模拟同步任务到服务器"""
            time.sleep(2.5)  # 模拟网络延迟
            
            # 获取所有任务
            all_tasks = self.repository.get_all_tasks()
            
            # 模拟同步逻辑
            synced_tasks = []
            for task in all_tasks:
                synced_tasks.append({
                    "id": task.id,
                    "name": task.name,
                    "status": task.status.value,
                    "synced_at": time.time()
                })
            
            return {
                "synced_tasks": synced_tasks,
                "total_synced": len(synced_tasks),
                "server_timestamp": time.time()
            }
        
        def on_sync_success(result):
            """同步成功回调"""
            total_synced = result.get('total_synced', 0)
            self.view.show_message("成功", f"成功同步了 {total_synced} 个任务到服务器！")
        
        def on_sync_error(error):
            """同步失败回调"""
            self.view.show_message("错误", f"同步任务失败：{error}", "error")
        
        # 异步同步任务
        self.task_manager.run_async(
            sync_to_server,
            task_id="sync_tasks",
            on_finished=on_sync_success,
            on_error=on_sync_error
        )
        
        print("[EnhancedController] 开始同步任务到服务器...")
    
    def handle_export_tasks(self, file_path: str):
        """
        处理导出任务请求
        
        Args:
            file_path: 导出文件路径
        """
        def export_to_file():
            """模拟导出任务到文件"""
            time.sleep(2)  # 模拟文件I/O延迟
            
            # 获取所有任务
            all_tasks = self.repository.get_all_tasks()
            
            # 转换为可序列化的格式
            export_data = {
                "export_timestamp": time.time(),
                "total_tasks": len(all_tasks),
                "tasks": []
            }
            
            for task in all_tasks:
                export_data["tasks"].append({
                    "id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                })
            
            # 模拟写入文件
            # 在实际应用中，这里会写入真实文件
            # with open(file_path, 'w', encoding='utf-8') as f:
            #     json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return {
                "exported_file": file_path,
                "task_count": len(all_tasks),
                "file_size": len(json.dumps(export_data))
            }
        
        def on_export_success(result):
            """导出成功回调"""
            file_name = result.get('exported_file', 'unknown')
            task_count = result.get('task_count', 0)
            file_size = result.get('file_size', 0)
            
            self.view.show_message(
                "成功", 
                f"成功导出 {task_count} 个任务到文件：{file_name}\n文件大小：{file_size} 字节"
            )
        
        def on_export_error(error):
            """导出失败回调"""
            self.view.show_message("错误", f"导出任务失败：{error}", "error")
        
        # 异步导出任务
        self.task_manager.run_async(
            export_to_file,
            task_id="export_tasks",
            on_finished=on_export_success,
            on_error=on_export_error
        )
        
        print(f"[EnhancedController] 开始导出任务到文件: {file_path}")
    
    # ========== UI更新槽函数 ==========
    
    def on_task_added_update_ui(self, task: Task):
        """槽函数：当仓库添加任务后，更新UI"""
        display_text = self.format_task_display_text(task)
        self.view.add_task_item(display_text, task.id)
        self.update_ui_statistics()
        print(f"[EnhancedController] UI已更新 - 添加任务: {task.name}")
    
    def on_task_removed_update_ui(self, index: int, task: Task):
        """槽函数：当仓库删除任务后，更新UI"""
        self.view.remove_task_item(index)
        self.update_ui_statistics()
        print(f"[EnhancedController] UI已更新 - 删除任务: {task.name} (索引: {index})")
    
    def on_task_updated_update_ui(self, index: int, task: Task):
        """槽函数：当仓库更新任务后，更新UI"""
        display_text = self.format_task_display_text(task)
        self.view.update_task_item(index, display_text)
        self.update_ui_statistics()
        print(f"[EnhancedController] UI已更新 - 更新任务: {task.name} (索引: {index})")
    
    def on_tasks_cleared_update_ui(self):
        """槽函数：当仓库清空所有任务后，更新UI"""
        self.view.clear_task_list()
        self.update_ui_statistics()
        print("[EnhancedController] UI已更新 - 清空所有任务")
    
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
                "description": "掌握QThreadPool和QRunnable的使用方法",
                "status": TaskStatus.IN_PROGRESS
            },
            {
                "name": "实现网络请求功能",
                "description": "集成HTTP客户端进行API调用",
                "status": TaskStatus.PENDING
            },
            {
                "name": "优化UI响应性能",
                "description": "使用线程池避免UI阻塞",
                "status": TaskStatus.COMPLETED
            }
        ]
        
        print("[EnhancedController] 添加示例数据...")
        for task_data in sample_tasks:
            try:
                self.repository.add_task(task_data)
            except Exception as e:
                print(f"[EnhancedController] 添加示例数据失败: {e}")
    
    def show(self):
        """显示主窗口"""
        self.view.show()
        print("[EnhancedController] 增强版应用程序已启动")
    
    def cleanup(self):
        """清理资源"""
        # 等待所有异步任务完成
        self.task_manager.wait_for_done(5000)  # 等待5秒
        print("[EnhancedController] 资源清理完成")
