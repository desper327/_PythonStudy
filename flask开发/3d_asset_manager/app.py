from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# 数据库文件路径
DATABASE = os.path.join(PROJECT_DIR,'3d_assets.db')

# 确保 static/thumbnails 目录存在
THUMBNAILS_DIR = os.path.join(PROJECT_DIR,'static', 'thumbnails')
if not os.path.exists(THUMBNAILS_DIR):
    os.makedirs(THUMBNAILS_DIR)

# 初始化数据库
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            Chinese_name TEXT,
            thumbnail TEXT,
            model_path TEXT,
            bind_path TEXT,
            texture_path TEXT,
            description TEXT
        )
        ''')
        conn.commit()

# 获取所有资产
def get_assets():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM assets')
        assets = cursor.fetchall()
    assets = [(a[0], a[1], a[2], a[3].replace('\\', '/'), a[4].replace('\\', '/'), a[5].replace('\\', '/'), a[6].replace('\\', '/'), a[7].replace('\\', '/')) for a in assets]
    print('assets',assets)
    return assets


# 添加资产
def add_asset(name, Chinese_name, thumbnail, model_path, bind_path, texture_path, description):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO assets (name, Chinese_name, thumbnail, model_path, bind_path, texture_path, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, Chinese_name, thumbnail, model_path, bind_path, texture_path, description))
        conn.commit()

# 更新资产
def update_asset(asset_id, name, Chinese_name, thumbnail, model_path, bind_path, texture_path, description):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE assets
        SET name = ?, Chinese_name = ?, thumbnail = ?, model_path = ?, bind_path = ?, texture_path = ?, description = ?
        WHERE id = ?
        ''', (name, Chinese_name, thumbnail, model_path, bind_path, texture_path, description, asset_id))
        conn.commit()

# 删除资产
def delete_asset(asset_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
        conn.commit()

# 列出路径下的文件
def list_files(path):
    try:
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except FileNotFoundError:
        return []

# 主界面
@app.route('/')
def index():
    assets = get_assets()
    return render_template('index.html', assets=assets)

# 添加资产
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        Chinese_name=request.form['Chinese_name']
        thumbnail = request.files['thumbnail']
        model_path = request.form['model_path']
        bind_path = request.form['bind_path']
        texture_path = request.form['texture_path']
        description = request.form['description']

        # 保存缩略图
        if thumbnail:
            thumbnail_path = os.path.join(THUMBNAILS_DIR, thumbnail.filename)
            thumbnail.save(thumbnail_path)
            thumbnail_url = f"thumbnails/{thumbnail.filename}"
        else:
            thumbnail_url = None

        add_asset(name, Chinese_name,thumbnail_url, model_path, bind_path, texture_path, description)
        return redirect(url_for('index'))
    return render_template('edit.html', asset=None)

# 编辑资产
@app.route('/edit/<int:asset_id>', methods=['GET', 'POST'])
def edit(asset_id):
    if request.method == 'POST':
        name = request.form['name']
        Chinese_name=request.form['Chinese_name']
        thumbnail = request.files['thumbnail']
        model_path = request.form['model_path']
        bind_path = request.form['bind_path']
        texture_path = request.form['texture_path']
        description = request.form['description']

        # 保存缩略图
        if thumbnail:
            thumbnail_path = os.path.join(THUMBNAILS_DIR, thumbnail.filename)
            thumbnail.save(thumbnail_path)
            thumbnail_url = f"thumbnails/{thumbnail.filename}"
        else:
            thumbnail_url = None

        update_asset(asset_id, name, Chinese_name,thumbnail_url, model_path, bind_path, texture_path, description)
        return redirect(url_for('index'))

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM assets WHERE id = ?', (asset_id,))
        asset = cursor.fetchone()
    return render_template('edit.html', asset=asset)

# 删除资产
@app.route('/delete/<int:asset_id>')
def delete(asset_id):
    delete_asset(asset_id)
    return redirect(url_for('index'))

# 将 list_files 函数注册为模板全局函数
@app.context_processor
def utility_processor():
    return dict(list_files=list_files)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)