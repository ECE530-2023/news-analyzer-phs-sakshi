"""Module for uploading file"""
import io
from flask import flash, request, render_template, redirect, url_for
from flask_login import current_user

from src.FeedIngester.ingester_feed import upload_file_to_s3
from src.FileUploader.file_uploader_impl import get_user_file_ids, \
    is_allowed_file_extension, get_file_by_file_id
from src.InputOutput.output import print_string
from src.TextAnalysis.text_analyzer_impl import analyze_file
from src.app import app

# @Input parameters - document to upload
# Response -
# 200 - Successful
# 400 - Bad Request
# 404 - File not found
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/upload', methods=['POST'])
async def upload_document():
    """ uploads a document to S3 and analyses the file"""
    try:
        files = request.files.getlist('files[]')
        for file in files:
            if file and is_allowed_file_extension(file.filename):
                file_contents = file.read()
                await upload_file_to_s3(io.BytesIO(file_contents), file)
                await analyze_file(io.BytesIO(file_contents), file.filename)
            else:
                raise Exception('inavlid file type')

        return render_template('upload.html', file_ids=[file.filename for file in files],
                               user=current_user.id)

    except Exception as e:
        app.logger.error(f'Error uploading document: {str(e)}')
        return redirect(url_for('uploader'))


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
    """ downloads the document from S3"""
    args = request.args
    file_id = args.get('fileId')
    try:
        if not file_id or file_id not in get_user_file_ids():
            flash('File not found')
            return 'File not found', 404

        file = get_file_by_file_id(file_id)
        return file, 200

    except ValueError:
        # Invalid token
        print_string("couldn't verify user")
        return 'Unauthorized', 401





