import sys
sys.path.append(r'D:\TD_Depot\Python\Lib\3.11\.venv\Lib\site-packages')

from flask import Flask, request, render_template, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 flash 消息的加密密钥

# MySQL 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',  # 替换为你的 MySQL 用户名
    'password': '123456',  # 替换为你的 MySQL 密码
    'database': 'MyTestData'  # 你的数据库名称
}

# 创建数据库连接
def create_db_connection():
    try:
        conn = pymysql.connect(**db_config)
        return conn
    except pymysql.Error as err:
        print(f"Error: {err}")
        return None

# 创建用户
def create_user(name, password):
    conn = create_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        query = "INSERT INTO users (name, password) VALUES (%s, %s)"
        cursor.execute(query, (name, password))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except pymysql.Error as err:
        print(f"Error: {err}")
        return False

# 首页：显示表单
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 处理表单提交
@app.route('/create_user', methods=['POST'])
def handle_create_user():
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        flash('Name and password are required!', 'error')
        return redirect(url_for('index'))

    if create_user(name, password):
        flash('User created successfully!', 'success')
    else:
        flash('Failed to create user.', 'error')

    return redirect(url_for('index'))

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)