"""Module for executing sqlite queries"""

import sqlite3
from src.InputOutput.output import print_string


def execute_query(query, param=None):
    """execute queries"""

    sqlite_connection = sqlite3.connect('News_Analyzer.db')
    record = False
    try:
        cursor = sqlite_connection.cursor()
        if param:
            cursor.execute(query, param)
        else:
            cursor.execute(query)
        record = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print_string("Error while connecting to sqlite" + error.sqlite_errorname+ query)
        record = False
    finally:
        if sqlite_connection:
            sqlite_connection.close()
    return record


def execute_insert_query(query, param):
    """execute queries"""

    sqlite_connection = sqlite3.connect('News_Analyzer.db')
    record = False
    try:
        cursor = sqlite_connection.cursor()
        cursor.execute(query, param)
        record = cursor.lastrowid
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print_string("Error while connecting to sqlite" + error.sqlite_errorname+query)
        record = False
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            #print("The SQLite connection is closed")
    return record