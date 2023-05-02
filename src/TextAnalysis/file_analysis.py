"""Module for file analysis"""
import threading

from flask import request, render_template, abort
from flask_login import current_user

from src.FileUploader.file_uploader_impl import get_user_file_ids
from src.TextAnalysis.text_analyzer_impl import get_definition, \
    get_paragraphs_by_sentiment, get_paragraphs_by_keywords, \
    get_document_summary, get_file_info
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
    """ search for paragraphs with given keywords"""
    paragraphs = get_paragraphs_by_keywords(keyword)
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
    """ search for paragraphs with given sentiment"""
    args = request.args
    sentiment = args.get('sentiment')
    if sentiment not in ['positive', 'negative', 'neutral']:
        return 'No such sentiment', 400
    paragraphs = get_paragraphs_by_sentiment(sentiment)
    return paragraphs, 200


# @Input parameters - keywords to
# Response -
# 200 - Successful - definition of the keyword
# 400 - Bad Request - keyword not found
# 500 - Internal Server Error
@app.route('/keywordDefinition', methods=['POST'])
def get_keyword_definition():
    """ get the definition of a keyword"""
    keyword = request.form['keyword']
    # keyword = args.get('keyword')
    definition = get_definition(keyword)
    if definition:
        return render_template('search.html', definition=keyword+definition, user=current_user.id)
    return render_template('search.html', user=current_user.id)

# @Input parameters - file id of the file to summarize
# Response -
# 200 - Successful - summary of the file
# 400 - Bad Request - file not found
# 500 - Internal Server Error
@app.route('/documentSummary',methods=['POST'])
def document_summary():
    """get the summary of the document"""
    file_id = request.form['file_id']
    text = get_text_of_file(file_id)
    summary = get_document_summary(text)
    if summary:
        return summary, 200
    return 'Unable to find document', 400
@app.route('/file_analysis', methods=['POST'])
def analyze_complete_file():
    """ analyse the file - calculate keywords, summary, sentiment"""
    if 'fileId' not in request.form:
        abort(400, 'File ID not found')
    file_id = request.form['fileId']
    if not file_id or file_id not in get_user_file_ids():
        return render_template('analyze.html', not_found=True)
    try:
        name, link, sentiment, date, size, summary, keywords = get_file_info(file_id)
        return render_template('analyze.html', file_analyzed=True, name=name, link=link, date_uploaded=date, size=size,keywords=keywords, summary=summary, sentiment=sentiment, user=current_user.id)
    except Exception as e:
        raise Exception(500, str(e))



