"""Module for operating on the Document table"""

from src.database.Query_Execution import execute_query, execute_insert_query
from src.InputOutput.output import print_string
import requests
from flask import send_file


def create_documents_table():
    """create Document table and insert sample values"""

    create_document_table = '''CREATE TABLE IF NOT EXISTS document (
                                doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                doc_name TEXT NOT NULL,
                                user_id INTEGER,
                                doc_link TEXT NOT NULL,
                                doc_text_link TEXT,
                                sentiment TEXT,
                                date_uploaded timestamp,
                                date_deleted TEXT,
                                file_size INTEGER NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES users(user_id));'''

    record = execute_query(create_document_table)
    if not record == False:
        print_string("Document table not created")

    row_count = execute_query('''SELECT COUNT(*) from document''')[0][0]
    if row_count == 0:
        document_table_insert = '''INSERT INTO document (doc_name,user_id,doc_link,file_size) VALUES
                                                        ('doc1',1,'doc1@link1.com',200),
                                                        ('doc2',1,'doc2@link2.com',300),
                                                        ('doc3',2,'doc3@link3.com',200)'''

        if execute_query(document_table_insert) == False:
            print_string("Insert failed in document table")

def insert_doc_link(doc_name,user_id,doc_link,file_size):
    document_table_insert = '''INSERT INTO document (doc_name,user_id,doc_link,file_size) VALUES
                                                        (?,?,?,?)'''
    id = execute_insert_query(document_table_insert,(doc_name, user_id, doc_link, file_size))
    if id == False:
        print_string("Insert failed in document table")
        return False
    return id

def update_doc_sentiment(file_id, senti):
    query = '''UPDATE document SET sentiment = ? where doc_id = ?'''
    if execute_query(query,(senti, file_id)) == False:
        print_string("Couldn't update file record sentiment")
        return False
    print_string("sentiment of file updated successfully")
    return True

def fetch_all_user_file_ids(user_id):
    query = '''SELECT doc_id from document where user_id = ?'''
    records = execute_query(query,user_id)
    if records == False:
        print_string("Unable to get file ids for the user " + str(user_id))
        return False
    return records

def get_file(file_id, user_id):
    query = '''SELECT doc_link from document where user_id = ? AND doc_id = ?'''
    url = execute_query(query, user_id, file_id)
    if url == False:
        print_string("File not found")
        return False
    return download_file(url)

def get_text_of_file(file_id):
    query = '''SELECT doc_text_link from document where doc_id = ?'''
    url = execute_query(query, file_id)
    if url == False:
        print_string("File not found")
        return False
    return requests.get(url).content

def download_file(url):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    headers = {'Content-Disposition': f'attachment; filename={file_name}'}
    return send_file(response.content, as_attachment=True, attachment_filename=file_name, mimetype='application/octet-stream', headers=headers)
