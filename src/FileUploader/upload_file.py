"""Module for uploading file"""
import logging

from flask import flash, request, render_template

from src.FeedIngester.ingester_feed import upload_file_to_s3
from src.FileUploader.file_uploader_impl import get_user_file_ids, is_allowed_file_extension, get_file_by_file_id
from src.InputOutput.output import print_string
from src.TextAnalysis.text_analyzer_impl import analyze_file
from src.Thread import Thread
from src.app import app

# @Input parameters - document to upload
# Response -
# 200 - Successful
# 400 - Bad Request
# 404 - File not found
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/upload', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files or request.files['file'].filename == '':
            #flash('No file part')
            return 'No file', 404

        file = request.files['file']
        if file and is_allowed_file_extension(file.filename):
            # thread1 = Thread(upload_file_to_s3, (fileToS3, ), lambda _: None, ())
            # thread1.start()
            # thread1.stop()
            # thread1.stop_event.set()
            # # upload_file_to_s3(file)
            #
            # #analyze_file(file, file_id)
            # #implement threading
            #
            # thread2 = Thread(analyze_file, (fileAnalyze, fileAnalyze.filename), lambda _: None, ())
            # thread2.start()
            # thread2.stop()
            # thread2.stop_event.set()

            analyze_file(file, file.filename)

        return render_template('upload.html', file_id=file.filename)

    except ValueError:
        # Invalid token
        print_string("couldn't verify user")
        return 'Unauthorized', 401


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
    try:
        if not file_id or file_id not in get_user_file_ids():
            flash('File not found')
            return 'File not found', 404

        #file = get_file_by_file_id(file_id, user_id)
        thread = Thread(get_file_by_file_id, (file_id, ), lambda res: res[0], ())
        thread.start()
        thread.stop()
        file = thread.join()
        thread.stop_event.set()
        return file, 200

    except ValueError:
        # Invalid token
        print_string("couldn't verify user")
        return 'Unauthorized', 401





