"""Module for uploading file"""
from flask import Flask, flash, request
from src.FeedIngester.ingester_feed import ingest_file
from src.FileUploader.file_uploader_impl import get_user_file_ids, is_allowed_file_extension, get_file_by_file_id
from src.TextAnalysis.text_analyzer_impl import analyze_file


app = Flask(__name__)


# @Input parameters - document to upload
# Response -
# 200 - Successful
# 400 - Bad Request
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file part')
        return 'No file', 400
    file = request.files['file']

    if file and is_allowed_file_extension(file.filename):
        ingest_file(file)
        analyze_file(file)
        return '', 200
    return '', 500


# @Input parameters - document to upload
# Response -
# 200 - Successful
# 400 - Bad Request
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/download', methods=['GET'])
def download_document():
    args = request.args
    file_id = args.get('fileId')
    if not file_id or file_id not in get_user_file_ids:
        flash('No file part')
        return 'No file', 400
    file = get_file_by_file_id(file_id)
    return file, 200




