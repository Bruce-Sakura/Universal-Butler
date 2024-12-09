import cv2
import face_recognition
import mysql.connector
import numpy as np

def retrieve_faces_from_db():
    """
    从数据库中检索所有的已知面部编码（存储为 BLOB 格式）。
    """
    connection = mysql.connector.connect(
        host="localhost",  # 数据库地址
        user="your_username",  # 数据库用户名
        password="your_password",  # 数据库密码
        database="your_database"  # 数据库名称
    )
    cursor = connection.cursor()

    cursor.execute("SELECT Surname, Forename, face FROM Users")
    known_face_encodings = []
    known_face_names = []

    # 获取查询结果
    for row in cursor.fetchall():
        surname, forename, face_encoding_blob = row

        # 将 BLOB 数据转换为 NumPy 数组
        np_array = np.frombuffer(face_encoding_blob, dtype=np.float64)

        # 添加到已知面部编码列表
        known_face_encodings.append(np_array)
        known_face_names.append(f"{surname} {forename}")

    cursor.close()
    connection.close()

    return known_face_encodings, known_face_names

def recognize_face_in_frame(frame):
    """
    从当前帧中识别面部，并与数据库中的已知面部进行匹配
    """
    known_face_encodings, known_face_names = retrieve_faces_from_db()

    # 提取当前帧中的面部编码
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    recognized_name = "Unknown"
    if face_locations:
        for face_encoding in face_encodings:
            # 比较扫描到的面部与已知面部
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                recognized_name = known_face_names[first_match_index]

    return recognized_name

# 示例：使用摄像头捕获图像并识别
def capture_and_recognize():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access webcam")
        return

    ret, frame = cap.read()
    if ret:
        recognized_name = recognize_face_in_frame(frame)
        print(f"Recognized: {recognized_name}")

    cap.release()
