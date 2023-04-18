"""Module for operating on Keywords table"""

from src.database.Query_Execution import execute_query, execute_insert_query
from src.InputOutput.output import print_string


def create_table_keywords():
    """create the Keywords table"""

    create_table_keywords = ''' CREATE TABLE IF NOT EXISTS KEYWORDS (
                                keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                keyword TEXT NOT NULL UNIQUE,
                                para_id INTEGER,
                                doc_id INTEGER,
                                definition TEXT NOT NULL,
                                FOREIGN KEY (para_id) REFERENCES paragraphs(para_id),
                                FOREIGN KEY (doc_id) REFERENCES document(doc_id));'''

    record = execute_query(create_table_keywords)
    if record == False:
        print_string("Cannot create keywords table")

def insert_keywords_by_para(keyword,para_id,doc_id,definition):
    insert_keywords_query = ''' INSERT OR IGNORE INTO KEYWORDS (keyword, para_id,doc_id,definition) 
                                VALUES(?,?,?,?)'''
    return execute_query(insert_keywords_query, (keyword, para_id, doc_id, definition))

def insert_keywords(keyword,doc_id,definition):
    insert_keywords_query = ''' INSERT OR IGNORE INTO KEYWORDS (keyword,doc_id,definition) 
                                VALUES(?,?,?)'''
    return execute_insert_query(insert_keywords_query,(keyword,doc_id,definition))