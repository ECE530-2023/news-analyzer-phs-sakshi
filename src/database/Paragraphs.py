"""Module for operating on Paragraphs table"""

from Query_Execution import execute_query
from src.InputOutput.output import print_string

def create_paragraphs_table():
    """create paragraphs table"""
    create_paragraph_table = ''' CREATE TABLE IF NOT EXISTS paragraphs(
                                para_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                doc_id INTEGER NOT NULL,
                                sentiment TEXT,
                                FOREIGN KEY(doc_id) REFERENCES document(doc_id));'''
    record = execute_query(create_paragraph_table)
    if record == False:
        print_string("Paragraphs table not created")
