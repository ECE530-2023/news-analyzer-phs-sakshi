"""Module for file analysis"""
from flask import request, flash
from src.TextAnalysis.text_analyzer_impl import get_definition, get_paragraphs_by_sentiment, get_paragraphs_by_keywords, \
    get_document_summary
from src.FileUploader.file_uploader_impl import get_user_file_ids
from text_analyzer_impl import analyze_file
from google.oauth2 import id_token
from google.auth.transport import requests
from src.InputOutput.output import print_string
from __main__ import app
from src.Thread import Thread

# @Input parameters - document to analyze
# Response -
# 200 - Successful
# 400 - Bad Request
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/analyze/<string:file_id>', methods=['GET'])
def analyze_document(file_id):
    user_id = get_user_id()
    if not file_id or file_id not in get_user_file_ids(user_id):
        flash('File not found')
        return 'File not found', 400
    #file = analyze_file(file_id, user_id)

    thread = Thread(analyze_file, (file_id, user_id), lambda res: res[0], ())
    thread.start()
    file = thread.join()
    return file, 200

# @Input parameters - keywords to match the paragraphs
# Response -
# 200 - Successful - list of paragraphs
# 400 - Bad Request
# 500 - Internal Server Error
@app.route('/paragraphsByKeyword/<string : keyword>', methods=['GET'])
def paragraphs_by_keywords(keyword):
    #paragraphs = get_paragraphs_by_keywords(keyword)

    thread = Thread(get_paragraphs_by_keywords, (keyword,), lambda res: res[0], ())
    thread.start()
    paragraphs = thread.join()
    if paragraphs:
        return paragraphs, 200
    return 'Keyword not found', 400


# @Input parameters - sentiment to match the paragraphs
# Response -
# 200 - Successful - list of paragraphs
# 400 - Bad Request
# 500 - Internal Server Error
@app.route('/paragraphsBySentiment', methods=['GET'])
def paragraphs_by_sentiment():
    args = request.args
    sentiment = args.get('sentiment')
    if sentiment not in ['positive', 'negative', 'neutral']:
        return 'No such sentiment', 400
    #paragraphs = get_paragraphs_by_sentiment(sentiment)

    thread = Thread(get_paragraphs_by_sentiment, (sentiment,), lambda res: res[0], ())
    thread.start()
    paragraphs = thread.join()
    return paragraphs, 200


# @Input parameters - keywords to
# Response -
# 200 - Successful - definition of the keyword
# 400 - Bad Request - keyword not found
# 500 - Internal Server Error
@app.route('/keywordDefinition',methods=['GET'])
def get_keyword_definition():
    args = request.args
    keyword = args.get('keyword')
    #definition = get_definition(keyword)

    thread = Thread(get_definition, (keyword,), lambda res: res[0], ())
    thread.start()
    definition = thread.join()

    if definition:
        return definition, 200
    return 'Error - Keyword not found', 400


# @Input parameters - file id of the file to summarize
# Response -
# 200 - Successful - summary of the file
# 400 - Bad Request - file not found
# 500 - Internal Server Error
@app.route('/documentSummary/<string:file_id>',methods=['GET'])
def document_summary(file_id):
    #summary = get_document_summary(file_id)

    thread = Thread(get_document_summary, (file_id,), lambda res: res[0], ())
    thread.start()
    summary = thread.join()
    if summary:
        return summary, 200
    return 'Unable to find document', 400


def get_user_id():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        idinfo = id_token.verify_oauth2_token(token, requests.Request())
        user_id = idinfo['sub']
        return user_id
    except ValueError:
        # Invalid token
        print_string("couldn't verify user")
        return 'Unauthorized', 401