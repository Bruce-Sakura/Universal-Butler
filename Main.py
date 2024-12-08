import Database_control.Connection  # 直接从 Connection.py 导入
import Database_control.Load_face

def connect_to_db():
    print("Database starting...")
    try:
        connection = Database_control.Connection.DatabaseConnection.connect_to_db()
        if connection:
            print("Database connection established successfully.")
        else:
            print("Failed to establish database connection.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


if __name__ == '__main__':
    connection = connect_to_db()  # 连接数据库



    if (connection != None):
        # 如果连接成功，加载脸部数据
        known_face_encodings, known_face_names = Database_control.Load_face.Load_face(connection)


