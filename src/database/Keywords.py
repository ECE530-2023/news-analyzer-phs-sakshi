"""Module for operating on Keywords table"""

from Query_Execution import execute_query, execute_insert_query
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

def insert_keywords(keyword,para_id,doc_id,definition):
    insert_keywords_query = ''' INSERT OR IGNORE INTO KEYWORDS (keyword, para_id,doc_id,definition) 
                                VALUES(?,?,?,?)'''
    if execute_query(insert_keywords_query,(keyword,para_id,doc_id,definition)) == False:
        print_string("Insert failed in keyword table")

def insert_keywords(keyword,doc_id,definition):
    insert_keywords_query = ''' INSERT OR IGNORE INTO KEYWORDS (keyword,doc_id,definition) 
                                VALUES(?,?,?)'''
    id = execute_insert_query(insert_keywords_query,(keyword,doc_id,definition))
    if id == False:
        print_string("Insert failed in keyword table")
        return False
    return id