import sys,os

sys.path.append(os.environ["Yplug"]+"/utils")
from Yenv_config import *

import pymysql
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Boolean, Text, DateTime, func
from sqlalchemy.orm import sessionmaker, relationship,declarative_base

import enum

Yprint("Hello, world!")


#连接数据库
DB_USER = 'zy' 
DB_PASSWORD = 'zhangyang'
DB_HOST = 'localhost'
DB_NAME = 'forza_tray'  # 数据库名称
# 数据库连接URL格式: mysql+pymysql://用户名:密码@服务器地址:端口/数据库名
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)()



Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"

class ActivityType(enum.Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    RUN_PROGRAM = "run_program"
    ERROR = "error"
    SYSTEM_EVENT = "system_event"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100))
    department = Column(String(50))
    role = Column(Enum(UserRole), default=UserRole.USER)
    ip_address = Column(String(45))
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserActivity(Base):
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # 关联用户ID
    username = Column(String(50), nullable=False)  # 用户名（冗余存储便于查询）
    activity_type = Column(Enum(ActivityType), nullable=False)
    program_name = Column(String(200))  # 运行的程序名称
    program_path = Column(String(500))  # 程序完整路径
    is_success = Column(Boolean, default=True)  # 是否成功运行
    error_message = Column(Text)  # 错误信息
    additional_info = Column(Text)  # 额外信息（JSON格式）
    ip_address = Column(String(45))  # 用户IP地址
    timestamp = Column(DateTime, default=func.now())  # 活动时间戳





#查询数据
# result = session.query(User).all()
# for row in result:
#     print(row.id, row.username, row.email, row.department, row.role, row.ip_address, row.last_login, row.created_at, row.updated_at)
# result = session.query(UserActivity).all()
# for row in result:
#     print(row.id, row.user_id, row.username, row.activity_type, row.program_name, row.program_path, row.is_success, row.error_message, row.additional_info, row.ip_address, row.timestamp)

# result=session.query(User).filter(User.username.like("%zhang%"))#.all()
# #Yprint(result)
# for row in result:
#     print(row.username,row.email)

# result=session.query(User).filter(User.username=="zhangyang").first()
# Yprint(result)
# for row in result:
#     print(row.username)

# result=session.query(User).filter(User.username!="liu").all()
# Yprint(result)
# for row in result:
#     print(row.username, row.email)


result=session.query(User.username).filter(User.username.contains("zhang")).all()
#result=session.query(User.username).distinct().all()
for row in result:
    print(row)
    #print(row.username, row.email)

# #新增数据
# user = User(username="zhangyang", email="zhangyang@163.com", department="IT", role=UserRole.ADMIN, ip_address="127.0.0.1", last_login=func.now())
# session.add(user)
# session.commit()

# #修改数据
# user = session.query(User).filter_by(username="zhangyang").first()
# user.email = "zhangyang@qq.com"
# session.commit()

#更新数据
# session.query(User).filter_by(username="zhangyang").update({"email": "zhangyang@fox.com"})
# session.commit()

# #删除数据
# user = session.query(User).filter_by(id=1).first()
# session.delete(user)
# session.commit() 

# #创建表
# Yprint(Base.metadata.create_all(bind=engine))

# #删除表
# Yprint(Base.metadata.drop_all(bind=engine))
