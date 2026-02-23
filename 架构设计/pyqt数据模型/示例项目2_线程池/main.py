"""
异步任务管理器 - 使用QThread处理耗时任务
演示如何使用工作线程实现非阻塞的用户界面
"""
import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController


def main():
    """主函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("异步任务管理器")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("PyQt异步编程学习项目")
    
    print("=" * 70)
    print("🚀 异步任务管理器 - 使用QThread处理耗时任务")
    print("=" * 70)
    print("🎯 架构特点:")
    print("   1. 使用QThread创建工作线程")
    print("   2. 异步处理耗时操作，避免UI阻塞")
    print("   3. 简单的信号槽机制")
    print("   4. 不使用线程池，直接管理线程")
    print("   5. 适合简单的异步任务需求")
    print()
    print("💡 QThread vs QThreadPool:")
    print("   🔹 QThread: 直接创建线程，适合简单场景")
    print("   🔹 QThreadPool: 线程池管理，适合复杂场景")
    print("   🔹 本示例使用QThread，代码更简单直观")
    print("=" * 70)
    
    try:
        # 创建异步控制器
        controller = MainController()
        
        # 显示主窗口
        controller.show()
        
        print("✨ 应用程序启动成功！")
        print()
        print("🔧 请在界面中测试以下功能:")
        print("   📝 基础任务管理:")
        print("      - 添加/删除/更新任务")
        print("      - 状态变更和统计")
        print()
        print("   🔄 异步操作特性:")
        print("      - 添加包含'验证'、'远程'、'网络'的任务名称")
        print("      - 删除'重要'或'关键'任务")
        print("      - 将任务标记为'已完成'")
        print("      - 清空所有任务")
        print()
        print("   📊 观察以下特性:")
        print("      - UI始终保持响应，不会冻结")
        print("      - 耗时操作在后台线程执行")
        print("      - 控制台显示详细的线程执行信息")
        print("      - 主线程和工作线程的清晰分工")
        print()
        print("   🧵 线程执行流程:")
        print("      1. 主线程接收用户操作")
        print("      2. 创建QThread工作线程")
        print("      3. 工作线程执行耗时任务")
        print("      4. 通过信号返回结果到主线程")
        print("      5. 主线程更新UI界面")
        print("=" * 70)
        
        # 启动事件循环
        exit_code = app.exec_()
        
        # 应用程序退出时清理资源
        print("\n🧹 正在清理资源...")
        controller.cleanup()
        print("✅ 资源清理完成")
        
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"❌ 应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
