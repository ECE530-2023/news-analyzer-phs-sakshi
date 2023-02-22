"""Module for file analysis"""
from flask import Flask, request, flash
from src.TextAnalysis.text_analyzer_impl import get_definition, get_paragraphs_by_sentiment, get_paragraphs_by_keywords
from src.FileUploader.file_uploader_impl import is_allowed_file_extension
from text_analyzer_impl import analyze_file
app = Flask(__name__)


# @Input parameters - document to analyze
# Response -
# 200 - Successful
# 400 - Bad Request
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/analyze', methods=['GET'])
def analyze_document():
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file part')
        return 'No file', 400
    file = request.files['file']

    if file and is_allowed_file_extension(file.filename):
        analyze_file(file)
        return '', 200
    return '', 500

# @Input parameters - keywords to match the paragraphs
# Response -
# 200 - Successful - list of paragraphs
# 400 - Bad Request
# 500 - Internal Server Error
@app.route('/paragraphsByKeyword', methods=['GET'])
def get_paragraphs_by_keywords():
    args = request.args
    sentiment = args.get('keyword')
    paragraphs = get_paragraphs_by_keywords(sentiment)
    if paragraphs:
        return paragraphs, 200
    return 'Keyword not found', 400


# @Input parameters - sentiment to match the paragraphs
# Response -
# 200 - Successful - list of paragraphs
# 400 - Bad Request
# 500 - Internal Server Error
@app.route('/paragraphsBySentiment', methods=['GET'])
def get_paragraphs_by_sentiment():
    args = request.args
    sentiment = args.get('sentiment')
    if sentiment not in ['positive','negative','neutral']:
        return 'No such sentiment', 400
    paragraphs = get_paragraphs_by_sentiment(sentiment)
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
    definition = get_definition(keyword)
    if definition:
        return definition, 200
    return 'Error - Keyword not found', 400


# @Input parameters - file id of the file to summarize
# Response -
# 200 - Successful - summary of the file
# 400 - Bad Request - file not found
# 500 - Internal Server Error
@app.route('/documentSummary',methods=['GET'])
def get_document_summary():
    file = request.files['file']
    summary = get_document_summary(file)
    if summary:
        return summary, 200
    return 'Unable to find document', 400

