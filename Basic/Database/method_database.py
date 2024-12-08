import mysql.connector
import json
from datetime import datetime

# 用来处理数据库里时间格式的
def convert_datetime(obj):
    # 转换 datetime 对象为字符串
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError("Type not serializable")

# 获取书籍数据
def select_table_library(db, cursor):
    if db is None or cursor is None:
        print("Database connection is not established. Cannot query the table.")
        return

    try:
        # 执行查询
        cursor.execute("SELECT ID,Name,Author,Location,Amount FROM Library")
        results = cursor.fetchall()
        json_results = json.dumps(results, indent=5, ensure_ascii=False)
        # print(json_results)
        return json_results

    except mysql.connector.Error as err:
        print("Error querying Library table: " + str(err))

# 获取物品数据
def select_table_Items(db, cursor):
    if db is None or cursor is None:
        print("Database connection is not established. Cannot query the table.")
        return

    try:
        # 执行查询
        cursor.execute("SELECT ID,Name,Time FROM Items")
        results = cursor.fetchall()
        json_results = json.dumps(results, indent=3, ensure_ascii=False, default=convert_datetime)
        # print(json_results)
        return json_results

    except mysql.connector.Error as err:
        print("Error querying Library table: " + str(err))

# 获取用户名密码


"""
测试用的
if __name__ == '__main__':
    # 连接数据库
    db, cursor = connect_database()

    # 查询 Library 表
    select_table_library(db, cursor)

    select_table_Items(db, cursor)

    # 关闭连接
    if db is not None:
        cursor.close()
        db.close()
        print("Database connection closed.")    
"""