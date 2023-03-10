import sqlite3
from src.InputOutput.output import print_string

def execute_query(query):
    sqlite_connection = sqlite3.connect('SQLite_Python.db')
    record = False
    try:
        cursor = sqlite_connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print_string("Error while connecting to sqlite", error,query)
        record = False
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            #print("The SQLite connection is closed")
    return record






