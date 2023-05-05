"""Module for operating on the Document table"""

import requests
import io
from flask import send_file
from src.database.Keywords import get_keywords_by_file_name
from src.database.Query_Execution import execute_query, execute_insert_query
from src.InputOutput.output import print_string


def create_documents_table():
    """create Document table and insert sample values"""

    create_document_table = '''CREATE TABLE IF NOT EXISTS documents (
                                doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                doc_name TEXT NOT NULL,
                                doc_link TEXT NOT NULL,
                                doc_text TEXT,
                                sentiment TEXT,
                                date_uploaded timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                date_deleted TEXT,
                                file_size INTEGER NOT NULL,
                                summary TEXT
                                );'''

    record = execute_query(create_document_table)
    if not record:
        print_string("Document table not created")


def insert_doc(doc_name, doc_link, doc_text, sentiment, file_size, summary):
    """ insert a document into the document table"""

    document_table_insert = '''INSERT INTO documents (doc_name,doc_link,doc_text,sentiment, file_size, summary) VALUES
                                                        (?,?,?,?,?,?)'''
    id = execute_insert_query(document_table_insert, (doc_name, doc_link, doc_text, sentiment, file_size, summary))
    if not id:
        print_string("Insert failed in document table")
        return False
    return id


def update_doc_sentiment(file_id, senti):
    """ update the sentiment of a document"""

    query = '''UPDATE documents SET sentiment = ? where doc_id = ?'''
    if not execute_query(query, (senti, file_id)):
        print_string("Couldn't update file record sentiment")
        return False
    return True


def fetch_all_user_file_ids():
    """ get all the files related to a user id"""
    query = '''SELECT doc_name from documents'''
    records = execute_query(query)
    return set([x[0] for x in records])  # the results are returned as list of tuples - get the file ids from the tuples.


def get_file(file_id):
    """ get file from database"""
    query = '''SELECT doc_link from documents where doc_name = ?'''  # get the link of the document
    url = execute_query(query, (file_id,))
    if url == False:
        print_string("File not found")
        return False
    return download_file([x[0] for x in url][0])  # download the document from the link


def get_text_of_file(file_id):
    """ get the text extracted from the file"""

    query = '''SELECT doc_text from documents where doc_name = ?'''
    res = execute_query(query, (file_id,))[0]
    return res


def get_summary_of_file(file_id):
    """ get the summary of the file"""

    query = '''SELECT summary from documents where doc_name = ?'''
    res = execute_query(query, (file_id,))[0]  # take the first result
    return res[0]


def download_file(url):
    """ download the file given the url of where it is stored"""

    response = requests.get(url)
    file_name = url.split('/')[-1]
    file_data = io.BytesIO(response.content)
    return send_file(file_data, as_attachment=True, download_name=file_name,
                     mimetype='application/octet-stream')  # send the file as an attachment


def get_file_by_id(file_id):
    """ get the file information given the name for the file"""

    query = '''SELECT doc.doc_name, doc.doc_link,doc.sentiment, doc.date_uploaded,doc.file_size,doc.summary FROM documents AS doc where doc.doc_name = ?'''
    result = execute_query(query, (file_id,))[0]
    keywords = get_keywords_by_file_name(file_id)  # get the keywords associated with the file
    val = [x for x in result]
    val.append(keywords)
    return val
