"""Module for file analysis"""
from flask import request, render_template

from src.FileUploader.file_uploader_impl import get_user_file_ids
from src.TextAnalysis.text_analyzer_impl import get_definition, get_paragraphs_by_sentiment, get_paragraphs_by_keywords, \
    get_document_summary, get_file_info
from google.oauth2 import id_token
from google.auth.transport import requests
from src.InputOutput.output import print_string
from src.app import app
from src.Thread import Thread
from src.database.Document import get_text_of_file


# @Input parameters - keywords to match the paragraphs
# Response -
# 200 - Successful - list of paragraphs
# 400 - Bad Request
# 500 - Internal Server Error
@app.route('/paragraphsByKeyword/<keyword>', methods=['GET'])
def paragraphs_by_keywords(keyword):
    #paragraphs = get_paragraphs_by_keywords(keyword)

    thread = Thread(get_paragraphs_by_keywords, (keyword,), lambda res: res[0], ())
    thread.start()
    thread.stop()
    paragraphs = thread.join()
    thread.stop_event.set()
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

    thread.stop()
    paragraphs = thread.join()
    thread.stop_event.set()
    return paragraphs, 200


# @Input parameters - keywords to
# Response -
# 200 - Successful - definition of the keyword
# 400 - Bad Request - keyword not found
# 500 - Internal Server Error
@app.route('/keywordDefinition', methods=['POST'])
def get_keyword_definition():
    keyword = request.form['keyword']
    # keyword = args.get('keyword')
    definition = get_definition(keyword)

    # thread = Thread(get_definition, (keyword,), lambda res: res[0], ())
    # thread.start()
    #
    # thread.stop()
    # definition = thread.join()
    # thread.stop_event.set()
    if definition:
        return render_template('search.html', definition=keyword+definition)
    return render_template('search.html')

# @Input parameters - file id of the file to summarize
# Response -
# 200 - Successful - summary of the file
# 400 - Bad Request - file not found
# 500 - Internal Server Error
@app.route('/documentSummary/<string:file_id>',methods=['GET'])
def document_summary(file_id):
    # summary = get_document_summary(file_id)
    text = get_text_of_file(file_id)
    thread = Thread(get_document_summary, (text,), lambda res: res[0], ())
    thread.start()

    thread.stop()
    summary = thread.join()
    thread.stop_event.set()
    if summary:
        return summary, 200
    return 'Unable to find document', 400
@app.route('/file_analysis', methods=['POST'])
def analyze_complete_file():
    file_id = request.form['fileId']
    if not file_id or file_id not in get_user_file_ids():
        return render_template('analyze.html', not_found=True)
    name, link, sentiment, date, size, summary, keywords = get_file_info(file_id)
    return render_template('analyze.html', file_analyzed=True, name=name, link=link, date_uploaded=date, size=size,keywords=keywords, summary=summary, sentiment=sentiment)

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

