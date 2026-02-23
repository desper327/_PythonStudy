from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Asset(db.Model):
    __tablename__ = 'assets'
    asset_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asset_name = db.Column(db.String(255), nullable=False)  # 修改为 255
    chinese_name = db.Column(db.String(255))  # 修改为 255
    thumbnail = db.Column(db.String(255))  # 修改为 255
    asset_type = db.Column(db.String(50), nullable=False)
    project = db.Column(db.String(255), nullable=False)  # 修改为 255
    asset_path = db.Column(db.String(255))  # 新增字段
    remarks = db.Column(db.Text)  # 保留备注字段
    creator = db.Column(db.String(255), nullable=False)  # 修改为 255
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    updated_by = db.Column(db.String(255))  # 修改为 255

    # 新增字段
    design_path = db.Column(db.String(255))  # 设定图路径
    model_path = db.Column(db.String(255))  # 模型路径
    texture_path = db.Column(db.String(255))  # 贴图路径
    rig_path = db.Column(db.String(255))  # 绑定路径
    actionlib_path = db.Column(db.String(255))  # 新增字段


print(dir(db))