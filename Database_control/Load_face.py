

def Load_known_faces_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT Surname, Forename, face FROM Users")  # 假设数据库表结构包含姓名和面部编码

    known_face_encodings = []
    known_face_names = []

    # 获取查询结果
    for row in cursor.fetchall():
        surname, forename, face_encoding_blob = row

        if not face_encoding_blob:
            print(f"No face encoding found for {surname} {forename}. Skipping...")
            continue

        try:
            # 将 BLOB 数据转换为 NumPy 数组
            np_array = np.frombuffer(face_encoding_blob, dtype=np.uint8)

            # 解码图像
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            # 使用 face_recognition 获取人脸编码
            face_encoding = face_recognition.face_encodings(image)

            if face_encoding:
                known_face_encodings.append(face_encoding[0])  # 取第一个面部编码
                known_face_names.append(f"{surname} {forename}")
            else:
                print(f"No face detected in encoding for {surname} {forename}. Skipping...")

        except Exception as e:
            print(f"Failed to decode face encoding for {surname} {forename}: {e}")

    cursor.close()
    return known_face_encodings, known_face_names
