"""Create a database"""

from src.database.Document import create_documents_table
from src.database.Users import create_users_table
from src.database.Query_Execution import execute_query
from src.database.Paragraphs import create_paragraphs_table
from src.InputOutput.output import print_string
from src.database.Keywords import create_table_keywords


def create_database():
    """create the database"""

    print_string("Database created and Successfully Connected to SQLite")
    sqlite_select_query = "select sqlite_version();"
    record = execute_query(sqlite_select_query)
    print_string("SQLite Database Version is: " + str(record))


def start_database():
    """ create database and all tables"""
    create_database()
    create_users_table()
    create_documents_table()
    create_paragraphs_table()
    create_table_keywords()



