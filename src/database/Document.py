"""Module for operating on the Document table"""
from src.database.Keywords import get_keywords_by_file_name
from src.database.Query_Execution import execute_query, execute_insert_query
from src.InputOutput.output import print_string
import requests
import io
from flask import send_file


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
    if not record == False:
        print_string("Document table not created")

    # row_count = execute_query('''SELECT COUNT(*) from document''')[0][0]
    # if row_count == 0:
    #     document_table_insert = '''INSERT INTO document (doc_name,user_id,doc_link,file_size) VALUES
    #                                                     ('doc1','doc1@link1.com',200),
    #                                                     ('doc2','doc2@link2.com',300),
    #                                                     ('doc3','doc3@link3.com',200)'''
    #
    #     if execute_query(document_table_insert) == False:
    #         print_string("Insert failed in document table")

def insert_doc(doc_name,doc_link,doc_text,sentiment, file_size, summary):
    document_table_insert = '''INSERT INTO documents (doc_name,doc_link,doc_text,sentiment, file_size, summary) VALUES
                                                        (?,?,?,?,?,?)'''
    id = execute_insert_query(document_table_insert, (doc_name, doc_link, doc_text, sentiment, file_size,summary))
    if id == False:
        print_string("Insert failed in document table")
        return False
    return id

def update_doc_sentiment(file_id, senti):
    query = '''UPDATE documents SET sentiment = ? where doc_id = ?'''
    if execute_query(query,(senti, file_id)) == False:
        print_string("Couldn't update file record sentiment")
        return False
    print_string("sentiment of file updated successfully")
    return True

def fetch_all_user_file_ids():
    query = '''SELECT doc_name from documents'''
    records = execute_query(query)
    return [x[0] for x in records]

def get_file(file_id):
    query = '''SELECT doc_link from documents where doc_name = ?'''
    url = execute_query(query, (file_id, ))
    if url == False:
        print_string("File not found")
        return False
    return download_file([x[0] for x in url][0])

def get_text_of_file(file_id):
    query = '''SELECT doc_text from documents where doc_name = ?'''
    return execute_query(query, file_id)

def download_file(url):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    file_data = io.BytesIO(response.content)
    return send_file(file_data, as_attachment=True, download_name=file_name, mimetype='application/octet-stream')

def get_file_by_id(file_id):
    query = '''SELECT doc.doc_name, doc.doc_link,doc.sentiment, doc.date_uploaded,doc.file_size,doc.summary FROM documents AS doc where doc.doc_name = ?'''
    result = execute_query(query, (file_id, ))[0]
    keywords = get_keywords_by_file_name(file_id)
    val = [x for x in result]
    val.append(keywords)
    return val