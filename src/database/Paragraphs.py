"""Module for operating on Paragraphs table"""

from src.database.Query_Execution import execute_query, execute_insert_query
from src.InputOutput.output import print_string


def create_paragraphs_table():
    """create paragraphs table"""
    create_paragraph_table = ''' CREATE TABLE IF NOT EXISTS paragraphs(
                                para_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                doc_id INTEGER NOT NULL,
                                sentiment TEXT,
                                paragraph TEXT NOT NULL,
                                FOREIGN KEY(doc_id) REFERENCES document(doc_id));'''
    record = execute_query(create_paragraph_table)
    if record == False:
        print_string("Paragraphs table not created")


def insert_paragraph(doc_id, para, sentiment=None):
    insert_para_query = '''INSERT INTO paragraphs (doc_id, sentiment, paragraph) VALUES (?,?,?)'''

    id = execute_insert_query(insert_para_query, (doc_id, sentiment, para))
    if id == False:
        print_string("Insert failed in keyword table")
        return False
    return id


def update_para_sentiment(file_id, senti, para_id):
    query = '''UPDATE paragraphs SET sentiment = ? where doc_id = ? AND para_id = ?'''
    if execute_query(query, (senti, file_id, para_id)) == False:
        print_string("Couldn't update file record sentiment")
        return False
    print_string("sentiment of file updated successfully")
    return True


def get_para_by_sentiment(senti):
    query = '''SELECT paragraph from paragraphs where sentiment = ? '''
    paras = execute_query(query, senti)
    return paras if paras else []

def get_para_by_keyword(keyword):
    query = '''SELECT paragraph from paragraphs where para_id in 
                    (SELECT para_id from KEYWORDS where keyword = ?)'''
    paras = execute_query(query, keyword)
    return paras if paras else []
