import sqlite3

# 连接到数据库（如果不存在，将自动创建）
conn = sqlite3.connect('MyStudy\\资产管理软件\\assets.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        chinese_name TEXT,
        thumbnail TEXT,
        notes TEXT
    )
''')

conn.commit()
conn.close()
print("数据库和表已成功创建！")
