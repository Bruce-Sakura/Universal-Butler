import mysql.connector

def connect_database():
    try:
        db = mysql.connector.connect(
            host="192.168.1.2",  # 数据库服务器地址
            user="root",          # 数据库用户名
            passwd="1234",        # 数据库密码
            database="MyHome"     # 使用的数据库名称
        )
        cursor = db.cursor(dictionary=True)  # 创建字典类型的游标（这样查询结果会以字典的形式返回）
        print("Connected to MyHome...")
        return db, cursor  # 返回数据库连接和游标
    except mysql.connector.Error as err:
        print("Connection to database Error: " + str(err))
        return None, None  # 如果连接失败，返回 None
