import pymysql
from config import Config  # 导入配置文件
from werkzeug.security import generate_password_hash  # 用于密码加密

def connect_db():
    # 连接到 MySQL 服务器（不指定数据库）
    connection = pymysql.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
    return connection


def create_database_and_tables():
    # 连接到 MySQL 服务器
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
            print(f"数据库 '{Config.DB_NAME}' 已创建或已存在。")

            # 切换到目标数据库
            cursor.execute(f"USE {Config.DB_NAME}")

            # 创建 users 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    `group` VARCHAR(50) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Table 'users' created or already exists.")

            # 创建 assets 表（根据新需求调整字段）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id INT AUTO_INCREMENT PRIMARY KEY,
                    asset_name VARCHAR(255) NOT NULL,
                    chinese_name VARCHAR(255),
                    thumbnail VARCHAR(255),
                    asset_type VARCHAR(50) NOT NULL,
                    project VARCHAR(255) NOT NULL,
                    asset_path VARCHAR(255),
                    remarks TEXT,
                    creator VARCHAR(255) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by VARCHAR(255),
                    design_path VARCHAR(255),
                    model_path VARCHAR(255),
                    texture_path VARCHAR(255),
                    rig_path VARCHAR(255),
                    actionlib_path VARCHAR(255)
                );
            """)
            print("Table 'assets' created or already exists.")

            # 检查是否存在超级管理员用户
            cursor.execute("SELECT * FROM users WHERE username = 'superadmin'")
            superadmin = cursor.fetchone()

            if not superadmin:
                # 如果没有超级管理员用户，则创建一个
                hashed_password = generate_password_hash('yourpassword')  # 加密密码
                cursor.execute("""
                    INSERT INTO users (username, password, `group`)
                    VALUES (%s, %s, %s)
                """, ('superadmin', hashed_password, 'superadmin'))
                print("超级管理员用户 'superadmin' 已创建。")
            else:
                print("超级管理员用户 'superadmin' 已存在。")

        # 提交更改
        connection.commit()
    finally:
        # 关闭连接
        connection.close()


def add_collumn_to_table(field_name: str):
    # 连接到 MySQL 服务器
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 切换到目标数据库
            cursor.execute(f"USE {Config.DB_NAME}")
            cursor.execute(f"""
                ALTER TABLE assets
                ADD COLUMN {field_name} VARCHAR(255)
            """)
            print(f"字段 'assets.{field_name}' 已添加。")
        # 提交更改
        connection.commit()
    finally:
        # 关闭连接
        connection.close()






if __name__ == "__main__":
    create_database_and_tables()
    #add_collumn_to_table('')