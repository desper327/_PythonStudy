"""
增强版应用程序入口 - 支持异步任务处理的任务管理器
演示如何使用QThreadPool和QRunnable实现非阻塞的用户界面
"""
import sys
from PyQt5.QtWidgets import QApplication
from controllers.enhanced_main_controller import EnhancedMainController


def main():
    """主函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("增强版任务管理器")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("PyQt异步编程学习项目")
    
    print("=" * 70)
    print("🚀 增强版任务管理器 - 支持异步任务处理")
    print("=" * 70)
    print("🎯 架构特点:")
    print("   1. 使用QThreadPool + QRunnable实现线程池")
    print("   2. 异步处理耗时操作，避免UI阻塞")
    print("   3. 完整的进度反馈和错误处理机制")
    print("   4. 支持网络请求、文件I/O、重计算等异步操作")
    print("   5. 优雅的信号槽跨线程通信")
    print()
    print("💡 线程池 vs 传统QThread的优势:")
    print("   ✅ 自动管理线程生命周期")
    print("   ✅ 线程复用，提高性能")
    print("   ✅ 内置任务队列管理")
    print("   ✅ 防止线程泄漏")
    print("   ✅ 代码更简洁清晰")
    print("=" * 70)
    
    try:
        # 创建增强版主控制器
        controller = EnhancedMainController()
        
        # 显示主窗口
        controller.show()
        
        print("✨ 应用程序启动成功！")
        print()
        print("🔧 请在界面中测试以下功能:")
        print("   📝 基础任务管理:")
        print("      - 添加/删除/更新任务")
        print("      - 状态变更和统计")
        print()
        print("   🌐 异步操作演示:")
        print("      - 获取远程任务 (模拟网络请求)")
        print("      - 同步任务到服务器 (模拟API调用)")
        print("      - 导出任务数据 (模拟文件I/O)")
        print("      - 执行重计算 (模拟CPU密集型操作)")
        print()
        print("   📊 观察以下特性:")
        print("      - UI始终保持响应，不会冻结")
        print("      - 实时进度条和状态反馈")
        print("      - 多个异步任务可以并发执行")
        print("      - 完整的错误处理和用户提示")
        print("      - 控制台输出显示详细的执行流程")
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
