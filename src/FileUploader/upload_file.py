"""Module for uploading file"""
from flask import flash, request
from src.FeedIngester.ingester_feed import upload_file_to_s3
from src.FileUploader.file_uploader_impl import get_user_file_ids, is_allowed_file_extension, get_file_by_file_id
from src.InputOutput.output import print_string
from src.TextAnalysis.text_analyzer_impl import analyze_file
from google.oauth2 import id_token
from google.auth.transport import requests
from __main__ import app
from src.Thread import Thread

# @Input parameters - document to upload
# Response -
# 200 - Successful
# 400 - Bad Request
# 404 - File not found
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files or request.files['file'].filename == '':
        #flash('No file part')
        return 'No file', 404
    file = request.files['file']

    if file and is_allowed_file_extension(file.filename):
        file_id = upload_file_to_s3(file)
        #analyze_file(file, file_id)
        #implement threading
        thread = Thread(analyze_file, (file, file_id), lambda _: None, ())
        thread.start()
        return '', 200
    return '', 500


# @Input parameters - document to upload
# Response -
# 200 - Successful
# 400 - Bad Request
# 404 - File not found
# 401 - Unauthorized
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/download', methods=['GET'])
def download_document():
    args = request.args
    file_id = args.get('fileId')
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request())
        user_id = idinfo['sub']
        if not file_id or file_id not in get_user_file_ids(user_id):
            flash('File not found')
            return 'File not found', 404
        #file = get_file_by_file_id(file_id, user_id)
        thread = Thread(get_file_by_file_id, (file_id, user_id), lambda res: res[0], ())
        thread.start()
        file = thread.join()
        return file, 200

    except ValueError:
        # Invalid token
        print_string("couldn't verify user")
        return 'Unauthorized', 401





