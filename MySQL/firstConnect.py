import pymysql


#连接数据库
host='localhost'
user='root'
password='123456'
database='MyTestData'
port=3306

connect=pymysql.Connect(host=host,port=port, user=user, password=password, database=database)

#创建表格，表格是数据库中的一个表，相当一是文件夹中的一个表一样
create_tab='''
create table users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
)
'''
#cursor.execute(create_tab)


try:
    with connect.cursor() as cursor:

        user1='zhangsan'
        password1='123456'
        sql1="insert into name_and_password (name, password) values ('%s', '%s')" % (user1, password1)
        cursor.execute(sql1)

        user2='lisi'
        password2='654321'
        sql2="insert into users (name, password) values ('%s', '%s')" % (user2, password2)
        cursor.execute(sql2)

        sel_users="select * from users"
        cursor.execute(sel_users)
        result=cursor.fetchall()
        for row in result:
            print("name=%s, password=%s" % (row[0], row[1]))


        user3='ZZZZZZZ'
        password3='654321'
        sql3="insert into users (name, password) values ('%s', '%s')" % (user3, password3)
        cursor.execute(sql3)

        connect.commit()#最后一定要提交事务，否则数据不会被保存到数据库中

finally:
    connect.close()#关闭连接
    cursor.close()#也要关闭游标
