"""
应用程序测试脚本
用于验证各个模块是否能正常导入和运行
"""
import sys
import traceback
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试数据模型
        print("  - 导入数据模型...")
        from models.data_models import Project, Task, ProductionStage, TaskStatus
        print("    ✅ 数据模型导入成功")
        
        # 测试API客户端
        print("  - 导入API客户端...")
        from models.api_client import APIClient
        print("    ✅ API客户端导入成功")
        
        # 测试线程工具
        print("  - 导入线程工具...")
        from utils.thread_workers import ThreadManager, ProjectDataWorker
        print("    ✅ 线程工具导入成功")
        
        # 测试通用组件
        print("  - 导入通用组件...")
        from utils.common_widgets import ProgressWidget, ReportGenerator
        print("    ✅ 通用组件导入成功")
        
        # 测试视图组件
        print("  - 导入视图组件...")
        from views.main_window import MainWindow
        print("    ✅ 视图组件导入成功")
        
        # 测试控制器
        print("  - 导入控制器...")
        from controllers.main_controller import MainController
        print("    ✅ 控制器导入成功")
        
        # 测试配置
        print("  - 导入配置...")
        from config import config
        print("    ✅ 配置导入成功")
        
        return True
        
    except Exception as e:
        print(f"    ❌ 导入失败: {e}")
        traceback.print_exc()
        return False

def test_data_models():
    """测试数据模型"""
    print("\n🧪 测试数据模型...")
    
    try:
        from models.data_models import Project, Episode, Scene, Shot, Task, ProductionStage, TaskStatus
        from datetime import datetime
        
        # 创建测试项目
        project = Project(
            project_id="test_001",
            project_name="测试项目",
            description="这是一个测试项目"
        )
        
        # 创建测试集
        episode = Episode(
            episode_id="ep_001",
            episode_name="第一集",
            episode_number="01"
        )
        
        # 创建测试场
        scene = Scene(
            scene_id="sc_001",
            scene_name="开场",
            scene_number="001"
        )
        
        # 创建测试镜头
        shot = Shot(
            shot_id="sh_001",
            shot_name="主角登场",
            shot_number="001"
        )
        
        # 创建测试任务
        task = Task(
            task_id="task_001",
            task_name="角色动画",
            stage=ProductionStage.ANIMATION,
            status=TaskStatus.IN_PROGRESS,
            assignee="张三",
            created_time=datetime.now()
        )
        
        # 构建层级关系
        shot.tasks.append(task)
        scene.shots.append(shot)
        episode.scenes.append(scene)
        project.episodes.append(episode)
        
        # 测试统计功能
        stats = project.get_project_statistics()
        print(f"  - 项目统计: {stats}")
        
        print("  ✅ 数据模型测试成功")
        return True
        
    except Exception as e:
        print(f"  ❌ 数据模型测试失败: {e}")
        traceback.print_exc()
        return False

def test_api_client():
    """测试API客户端"""
    print("\n🌐 测试API客户端...")
    
    try:
        from models.api_client import APIClient
        
        # 创建API客户端
        client = APIClient()
        
        # 测试获取项目列表（使用模拟数据）
        projects = client.get_projects()
        print(f"  - 获取到 {len(projects)} 个项目")
        
        if projects:
            # 测试获取项目详情
            project_detail = client.get_project_details(projects[0].project_id)
            if project_detail:
                print(f"  - 项目详情: {project_detail.project_name}")
            
            # 测试获取任务列表
            tasks = client.get_tasks_by_filters(projects[0].project_id)
            print(f"  - 获取到 {len(tasks)} 个任务")
        
        print("  ✅ API客户端测试成功")
        return True
        
    except Exception as e:
        print(f"  ❌ API客户端测试失败: {e}")
        traceback.print_exc()
        return False

def test_config():
    """测试配置"""
    print("\n⚙️ 测试配置...")
    
    try:
        from config import config, DevelopmentConfig
        
        print(f"  - 应用名称: {config.APP_NAME}")
        print(f"  - 应用版本: {config.APP_VERSION}")
        print(f"  - API地址: {config.API_BASE_URL}")
        print(f"  - 日志级别: {config.LOG_LEVEL}")
        
        # 测试配置字典
        config_dict = config.get_config_dict()
        print(f"  - 配置项数量: {len(config_dict)}")
        
        print("  ✅ 配置测试成功")
        return True
        
    except Exception as e:
        print(f"  ❌ 配置测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🎬 三维影视制作管理系统 - 测试脚本")
    print("=" * 60)
    
    test_results = []
    
    # 运行各项测试
    test_results.append(("模块导入", test_imports()))
    test_results.append(("数据模型", test_data_models()))
    test_results.append(("API客户端", test_api_client()))
    test_results.append(("配置系统", test_config()))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！程序应该可以正常运行。")
        print("\n运行程序:")
        print("  python main.py")
        print("或者:")
        print("  python run.py")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查相关模块。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)