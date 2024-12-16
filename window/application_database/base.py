import os
import sqlite3

def create_connection(db_file):
    if not os.path.exists(db_file):
        print(f"The file {db_file} does not exist")
        print(f"Creating database {db_file}")
        create_database(db_file)
    else:
        print(f"Connecting to {db_file}...")

    connection = sqlite3.connect(db_file)
    return connection

def create_database(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Start_location STRING NOT NULL)
    ''')
    connection.commit() # update db
    connection.close() # close db
    print(f"Database {db_file} created successfully")


def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        cursor.execute("INSERT INTO applications (Name, Start_location) VALUES (?,?)", data)