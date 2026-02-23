"""
检查所有依赖是否已安装
"""

print("=" * 50)
print("检查 Python 依赖包安装情况")
print("=" * 50)

dependencies = {
    '后端核心': [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_socketio', 'Flask-SocketIO'),
        ('flask_cors', 'Flask-CORS'),
    ],
    '后端工具': [
        ('pymysql', 'PyMySQL'),
        ('jwt', 'PyJWT'),
        ('bcrypt', 'bcrypt'),
        ('dotenv', 'python-dotenv'),
        ('socketio', 'python-socketio'),
    ],
    '前端依赖': [
        ('PySide6', 'PySide6'),
        ('requests', 'requests'),
    ],
    'Python标准库': [
        ('hashlib', 'hashlib（密码加密）'),
        ('secrets', 'secrets（安全随机数）'),
    ]
}

total = 0
success = 0
failed_packages = []

for category, packages in dependencies.items():
    print(f"\n【{category}】")
    for module_name, package_name in packages:
        total += 1
        try:
            __import__(module_name)
            print(f"  ✅ {package_name}")
            success += 1
        except ImportError:
            print(f"  ❌ {package_name} - 未安装")
            failed_packages.append(package_name)

print("\n" + "=" * 50)
print(f"检查完成：{success}/{total} 个包已安装")
print("=" * 50)

if failed_packages:
    print("\n❌ 缺少以下依赖包：")
    for pkg in failed_packages:
        print(f"   - {pkg}")
    print("\n请运行以下命令安装：")
    print("   pip install " + " ".join(failed_packages))
else:
    print("\n✅ 所有依赖包已安装！可以启动项目了。")
