"""
创建测试数据脚本
用于快速创建测试用户和群组
"""
from app import create_app
from models import User, Group, GroupMember
from models.user import db


def create_test_users():
    """创建测试用户"""
    print('\n创建测试用户...')
    
    test_users = [
        {
            'username': 'admin',
            'password': '123456',
            'nickname': '管理员',
            'email': 'admin@chatroom.com'
        },
        {
            'username': 'user1',
            'password': '123456',
            'nickname': '张三',
            'email': 'zhangsan@example.com'
        },
        {
            'username': 'user2',
            'password': '123456',
            'nickname': '李四',
            'email': 'lisi@example.com'
        },
        {
            'username': 'user3',
            'password': '123456',
            'nickname': '王五',
            'email': 'wangwu@example.com'
        }
    ]
    
    created_users = []
    
    for user_data in test_users:
        # 检查用户是否已存在
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if existing_user:
            print(f'  ⚠️  用户 {user_data["username"]} 已存在，跳过')
            created_users.append(existing_user)
            continue
        
        # 创建用户
        user = User(
            username=user_data['username'],
            nickname=user_data['nickname'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        
        db.session.add(user)
        created_users.append(user)
        print(f'  ✅ 创建用户: {user_data["username"]} ({user_data["nickname"]})')
    
    db.session.commit()
    print(f'\n✅ 共创建 {len([u for u in created_users if u.id])} 个用户')
    
    return created_users


def create_test_groups(users):
    """创建测试群组"""
    print('\n创建测试群组...')
    
    if len(users) < 2:
        print('  ⚠️  用户数量不足，跳过创建群组')
        return []
    
    test_groups = [
        {
            'name': '技术交流群',
            'description': '讨论技术问题，分享编程经验',
            'type': 'public',
            'owner': users[0]
        },
        {
            'name': '闲聊群',
            'description': '随便聊聊，放松心情',
            'type': 'public',
            'owner': users[0]
        }
    ]
    
    created_groups = []
    
    for group_data in test_groups:
        # 检查群组是否已存在
        existing_group = Group.query.filter_by(name=group_data['name']).first()
        if existing_group:
            print(f'  ⚠️  群组 {group_data["name"]} 已存在，跳过')
            created_groups.append(existing_group)
            continue
        
        # 创建群组
        group = Group(
            name=group_data['name'],
            description=group_data['description'],
            type=group_data['type'],
            owner_id=group_data['owner'].id
        )
        db.session.add(group)
        db.session.flush()  # 获取group.id
        
        # 添加群主为成员
        owner_member = GroupMember(
            group_id=group.id,
            user_id=group_data['owner'].id,
            role='owner'
        )
        db.session.add(owner_member)
        
        # 添加其他用户为成员
        for user in users[1:]:
            member = GroupMember(
                group_id=group.id,
                user_id=user.id,
                role='member'
            )
            db.session.add(member)
        
        created_groups.append(group)
        print(f'  ✅ 创建群组: {group_data["name"]} (成员: {len(users)}人)')
    
    db.session.commit()
    print(f'\n✅ 共创建 {len([g for g in created_groups if g.id])} 个群组')
    
    return created_groups


def main():
    """主函数"""
    print('=' * 50)
    print('  Flask聊天室 - 创建测试数据')
    print('=' * 50)
    
    # 创建应用
    app, socketio = create_app()
    
    with app.app_context():
        try:
            # 创建测试用户
            users = create_test_users()
            
            # 创建测试群组
            groups = create_test_groups(users)
            
            print('\n' + '=' * 50)
            print('  测试数据创建完成！')
            print('=' * 50)
            print('\n测试账号信息：')
            print('-' * 50)
            print('用户名        密码      昵称')
            print('-' * 50)
            print('admin        123456    管理员')
            print('user1        123456    张三')
            print('user2        123456    李四')
            print('user3        123456    王五')
            print('-' * 50)
            print('\n提示：所有测试账号密码均为 123456')
            print('请使用这些账号登录测试聊天功能！\n')
            
        except Exception as e:
            print(f'\n❌ 错误: {str(e)}')
            db.session.rollback()


if __name__ == '__main__':
    main()
