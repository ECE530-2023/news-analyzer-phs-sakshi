"""Module for operating on users table"""

from src.database.Query_Execution import execute_query
from src.InputOutput.output import print_string


def create_users_table():
    """create and and sample values to users table"""
    create_users_table = '''CREATE TABLE IF NOT EXISTS users (
                                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    permission_set TEXT NOT NULL,
                                    email TEXT NOT NULL);'''

    record = execute_query(create_users_table)
    if execute_query(create_users_table) == False:
        print_string("Users table not created")

    row_count = execute_query('''SELECT COUNT(*) from users''')[0][0]
    if row_count == 0:
        users_table_insert = '''INSERT INTO users (permission_set,email) VALUES 
                                                  ('RW','peter.parker@zylker.com'),
                                                  ('RW','peter.p@zylker.com'),
                                                  ('RW', 'john.smith@domain.com'),
                                                  ('RW', ' jonathandsouza@siestasalesmart')'''

        if execute_query(users_table_insert) == False:
            print_string("Insert failed in users table")



def addUser(email):
    query = '''INSERT OR IGNORE INTO users (permission_set,email) VALUES ('RW',?)'''
    execute_query(query, (email, ))
