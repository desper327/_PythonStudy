import os,sys
sys.path.append(r'D:\TD_Depot\Python\Lib\3.11\.venv\Lib\site-packages')


from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User, Asset
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)#'app'
app.config.from_object(Config)
db.init_app(app)


# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_THUMBNAILS_FOLDER']):
    os.makedirs(app.config['UPLOAD_THUMBNAILS_FOLDER'])


# 创建数据库和表
with app.app_context():
    db.create_all()
    # 检查是否存在超级管理员用户
    superadmin = User.query.filter_by(username='superadmin').first()
    if not superadmin:
        # 如果没有超级管理员用户，则创建一个
        superadmin = User(
            username='superadmin',
            password=generate_password_hash('yourpassword'),  # 设置密码
            group='superadmin'
        )
        db.session.add(superadmin)
        db.session.commit()
        print(f"Added superadmin user: {superadmin}")
    else:
        print("Superadmin user already exists.")


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']




# 首页（登录页面）
@app.route('/')
def index():
    return render_template('login.html')

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['group'] = user.group
        print(session, '登录成功')  # 调试信息
        return redirect(url_for('assets'))  # 登录成功后跳转到资产管理页面
    return render_template('login.html', error='Invalid credentials')  # 登录失败返回登录页面并显示错误信息

# 用户退出
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 用户修改密码
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        user = User.query.get(session['user_id'])
        if check_password_hash(user.password, old_password):
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return redirect(url_for('assets'))
        return render_template('change_password.html', error='Invalid old password')

    return render_template('change_password.html')

# 资产管理页面
@app.route('/assets')
def assets():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    # 获取过滤参数
    project = request.args.get('project', '')
    asset_type = request.args.get('asset_type', '')
    search_type = request.args.get('search_type', 'asset_name')
    search_value = request.args.get('search_value', '')

    # 构建查询
    query = Asset.query
    if project:
        query = query.filter(Asset.project == project)
    if asset_type:
        query = query.filter(Asset.asset_type == asset_type)
    if search_value:
        if search_type == 'asset_name':
            query = query.filter(Asset.asset_name.contains(search_value))
        elif search_type == 'chinese_name':
            query = query.filter(Asset.chinese_name.contains(search_value))

    assets = query.all()
    projects = db.session.query(Asset.project).distinct().all()
    return render_template('assets.html', assets=assets, projects=[p[0] for p in projects], selected_project=project, selected_asset_type=asset_type, search_value=search_value, search_type=search_type)

# 添加资产
@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if session['group'] not in ['superadmin', 'admin']:
        return jsonify({'message': 'Permission denied'}), 403  # 非管理员用户不允许添加资产


    if request.method == 'POST':
        # 处理表单提交
        asset_name = request.form.get('asset_name')
        chinese_name = request.form.get('chinese_name')
        asset_type = request.form.get('asset_type')
        project = request.form.get('project')
        asset_path = Config.DEPOT_FOLDER +'/'+project+'/'+asset_name  # 修改为 asset_path
        remarks = request.form.get('remarks')
        design_path = asset_path + '/design' 
        model_path = asset_path +'/model'
        texture_path = asset_path +'/texture'
        rig_path = asset_path +'/rig'
        actionlib_path = asset_path +'/actionlib'  # 新增字段

        # 检查资产名是否已存在（忽略大小写）
        existing_asset = Asset.query.filter(Asset.asset_name.ilike(asset_name)).first()
        if existing_asset:

            return redirect(url_for('add_asset'))

        # 创建资产
        asset = Asset(
            asset_name=asset_name,
            chinese_name=chinese_name,
            asset_type=asset_type,
            project=project,
            asset_path=asset_path,  # 修改为 asset_path
            remarks=remarks,
            creator=session.get('username'),
            design_path=design_path,  # 修改为 design_path
            model_path=model_path,
            texture_path=texture_path,
            rig_path=rig_path,
            actionlib_path=actionlib_path,  # 新增字段
        )

        #创建文件夹
        for path in [asset_path, design_path, model_path, texture_path, rig_path, actionlib_path]:
            if not os.path.exists(path):
                os.makedirs(path)

        # 处理缩略图
        thumbnail = request.files.get('thumbnail')  # 修改为 request.files，得到的是一个文件对象，可以操作保存到指定路径

        if thumbnail and allowed_file(thumbnail.filename):
            # 创建资产名文件夹
            asset_thumbnail_folder = os.path.join(app.config['UPLOAD_THUMBNAILS_FOLDER'], secure_filename(asset_name))
            if not os.path.exists(asset_thumbnail_folder):
                os.makedirs(asset_thumbnail_folder)

            # 生成缩略图文件名
            filename = f"{secure_filename(asset_name)}-1.{thumbnail.filename.rsplit('.', 1)[1].lower()}"
            file_path = os.path.join(asset_thumbnail_folder, filename)

            # 保存缩略图，操作对象，存到了static下的路径
            thumbnail.save(file_path)

            # 将缩略图路径保存到数据库，存文件路径字符串，到数据库
            asset.thumbnail = file_path.replace('static', '').replace('\\','/')  # 保存到数据库的路径，去掉static前缀,不能有反斜杠


        db.session.add(asset)
        db.session.commit()
        return redirect(url_for('assets'))

    projects = db.session.query(Asset.project).distinct().all()
    return render_template('add_asset.html', projects=[p[0] for p in projects])

# 编辑资产
@app.route('/edit_asset/<int:asset_id>', methods=['GET', 'POST'])
def edit_asset(asset_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if session['group'] not in ['superadmin', 'admin']:
        return jsonify({'message': 'Permission denied'}), 403  # 非管理员用户不允许编辑资产

    asset = Asset.query.get(asset_id)
    if request.method == 'POST':
        # 处理表单提交
        asset.asset_name = request.form.get('asset_name')
        asset.chinese_name = request.form.get('chinese_name')
        asset.asset_type = request.form.get('asset_type')
        asset.project = request.form.get('project')
        asset.asset_path = request.form.get('asset_path')  # 修改为 asset_path
        asset.thumbnail = request.form.get('thumbnail')
        asset.remarks = request.form.get('remarks')
        asset.design_path = request.form.get('design_path')  # 修改为 design_path
        asset.model_path = request.form.get('model_path')
        asset.texture_path = request.form.get('texture_path')
        asset.rig_path = request.form.get('rig_path')
        asset.actionlib_path = request.form.get('actionlib_path')  # 新增字段
        asset.updated_by = session.get('username')
        db.session.commit()
        return redirect(url_for('assets'))

    return render_template('edit_asset.html', asset=asset)

# 获取资产详情
@app.route('/get_asset_details/<int:asset_id>')
def get_asset_details(asset_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401  # 未登录用户不允许访问

    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'message': 'Asset not found'}), 404

    return jsonify({
        'asset_id': asset.asset_id,
        'design_path': asset.design_path,
        'model_path': asset.model_path,
        'texture_path': asset.texture_path,
        'rig_path': asset.rig_path,
        'remarks': asset.remarks,
        'creator': asset.creator,
        'created_at': asset.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': asset.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_by': asset.updated_by,
        'actionlib_path': asset.actionlib_path  # 新增动作库路径
    })


# 删除资产
@app.route('/delete_asset/<int:asset_id>')
def delete_asset(asset_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if session['group'] not in ['superadmin', 'admin']:
        return jsonify({'message': 'Permission denied'}), 403  # 非管理员用户不允许删除资产

    asset = Asset.query.get(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return redirect(url_for('assets'))

# 用户管理页面
@app.route('/users')
def users():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if session['group'] not in ['superadmin', 'admin']:
        return jsonify({'message': 'Permission denied'}), 403  # 非管理员用户不允许访问

    # 获取搜索关键字
    search_query = request.args.get('search', '')

    # 获取排序参数
    sort_column = request.args.get('sort', 'username')
    sort_order = request.args.get('order', 'asc')

    # 构建查询
    query = User.query
    if search_query:
        query = query.filter(User.username.contains(search_query))

    # 排序
    if sort_order == 'asc':
        query = query.order_by(getattr(User, sort_column).asc())
    else:
        query = query.order_by(getattr(User, sort_column).desc())

    users = query.all()
    return render_template('users.html', users=users, search_query=search_query, sort_order='desc' if sort_order == 'asc' else 'asc')

# 添加用户
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if session['group'] not in ['superadmin']:
        return jsonify({'message': 'Permission denied'}), 403  # 非超级管理员用户不允许添加用户

    if request.method == 'POST':
        # 处理表单提交
        username = request.form.get('username')
        password = request.form.get('password')
        group = request.form.get('group')

        # 创建用户
        user = User(
            username=username,
            password=generate_password_hash(password),
            group=group
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))

    return render_template('add_user.html')

# 编辑用户
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if session['group'] not in ['superadmin']:
        return jsonify({'message': 'Permission denied'}), 403  # 非超级管理员用户不允许编辑用户

    user = User.query.get(user_id)
    if request.method == 'POST':
        # 处理表单提交
        user.username = request.form.get('username')
        user.password = generate_password_hash(request.form.get('password'))
        user.group = request.form.get('group')
        db.session.commit()
        return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)

# 删除用户
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 未登录用户重定向到登录页面

    if session['group'] not in ['superadmin']:
        return jsonify({'message': 'Permission denied'}), 403  # 非超级管理员用户不允许删除用户

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

if __name__ == '__main__':
    # with app.test_request_context():
    #     print(app.url_map)  # 打印所有路由
    #app.run("192.168.112.10","27279",debug=True)
    app.run("127.0.0.1","5000",debug=True)