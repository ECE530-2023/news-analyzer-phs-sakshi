"""Module for operating on Keywords table"""

from Query_Execution import execute_query
from src.InputOutput.output import print_string


def create_table_keywords():
    """create the Keywords table"""

    create_table_keywords = ''' CREATE TABLE IF NOT EXISTS KEYWORDS (
                                keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                keyword TEXT NOT NULL,
                                para_id INTEGER,
                                doc_id INTEGER,
                                definition TEXT NOT NULL,
                                FOREIGN KEY (para_id) REFERENCES paragraphs(para_id),
                                FOREIGN KEY (doc_id) REFERENCES document(doc_id));'''

    record = execute_query(create_table_keywords)
    if record == False:
        print_string("Cannot create keywords table")
