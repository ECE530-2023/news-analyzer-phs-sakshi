"""Module for operating on Keywords table"""

from src.database.Query_Execution import execute_query, execute_insert_query
from src.InputOutput.output import print_string


def create_table_keywords():
    """create the Keywords table"""

    create_table_keywords = ''' CREATE TABLE IF NOT EXISTS keywords (
                                keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                keyword TEXT NOT NULL UNIQUE,
                                para_id INTEGER,
                                doc_id INTEGER,
                                definition TEXT NOT NULL,
                                FOREIGN KEY (para_id) REFERENCES paragraphs(para_id),
                                FOREIGN KEY (doc_id) REFERENCES document(doc_name));'''

    record = execute_query(create_table_keywords)
    if not record:
        print_string("Cannot create keywords table")


def insert_keywords_by_para(keyword, para_id, doc_id, definition):
    """ insert the keywords into the keywords table based on paragraph"""

    insert_keywords_query = ''' INSERT OR IGNORE INTO keywords (keyword, para_id,doc_id,definition) 
                                VALUES(?,?,?,?)'''
    return execute_query(insert_keywords_query, (keyword, para_id, doc_id, definition))


def insert_keywords(keyword, doc_id, definition):
    """ insert keywords in the table"""

    insert_keywords_query = ''' INSERT OR IGNORE INTO keywords (keyword,doc_id,definition) 
                                VALUES(?,?,?)'''
    return execute_insert_query(insert_keywords_query, (keyword, doc_id, definition))


def get_keywords_by_file_name(file_name):
    """ get all the keywords associated to a file"""

    query = '''SELECT keyword from keywords where doc_id = ?'''
    result = execute_query(query, (file_name, ))
    return [x[0] for x in result]       # result is a list of tuples - get keywords (at index 0) from all tuples
