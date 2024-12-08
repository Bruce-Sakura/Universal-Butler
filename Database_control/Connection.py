import mysql.connector


class DatabaseConnection:
    @staticmethod
    def connect_to_db():
        try:
            connection = mysql.connector.connect(
                host="192.168.1.2",
                port=3306,
                user="WebServer",
                password="1234",
                database="MyHome"
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None  # 如果连接失败，返回 None

    # @staticmethod
    # def test_connection():
    #     """
    #     每次连接数据库后执行查询
    #     """
    #     connection = DatabaseConnection.connect_to_db()  # 每次需要数据库时再连接
    #     cursor = connection.cursor()
    #
    #     # 执行查询
    #     cursor.execute("SELECT * FROM Connection_test")  # 测试成功
    #
    #     # 获取结果
    #     for row in cursor.fetchall():
    #         if (row[0] == '1'):
    #             print("Connected to MyHome!\n"
    #                   "Enjoy the home AI!\n")
    #
    #     # 关闭连接
    #     cursor.close()
    #     # connection.close()
    #     return connection  # 返回连接对象，以便后续使用
