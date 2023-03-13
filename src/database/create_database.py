"""Create a database"""

from Document import create_documents_table
from Users import create_users_table
from Query_Execution import execute_query
from Paragraphs import create_paragraphs_table
from src.InputOutput.output import print_string


def create_database():
    """create the database"""

    print_string("Database created and Successfully Connected to SQLite")
    sqlite_select_query = "select sqlite_version();"
    record = execute_query(sqlite_select_query)
    print_string("SQLite Database Version is: " + record)


create_database()
create_users_table()
create_documents_table()
create_paragraphs_table()



