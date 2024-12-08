import mysql.connector

def connect_database():
    try:
        db = mysql.connector.connect(
            host="192.168.1.2",
            user="root",
            passwd="1234",
            database="MyHome"
        )
        cursor = db.cursor(dictionary=True)
        print("Connected to MyHome...")
        return db, cursor
    except mysql.connector.Error as err:
        print("Connection to database Error: " + str(err))
        return None, None