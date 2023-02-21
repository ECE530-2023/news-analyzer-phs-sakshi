from flask import Flask, flash, request, redirect, url_for

app = Flask(__name__)


# @Input parameters - document to upload
# Response -
# 200 - Successful
# 400 - Bad Request
# 415 - Unsupported Media type
# 500 - Internal Server Error
@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files or file.filename == '':
        flash('No file part')
        return 'No file',400
    file = request.files['file']

    if file and is_allowed_file_extension(file.filename):
        ingest_file(file)
        analyze_file(file)
        return '', 200
    return '', 500


def is_allowed_file_extension(ext):
    return '.' in ext and \
           ext.rsplit('.', 1)[1].lower() in ['pdf', 'png', 'jpg', 'jpeg', 'csv', 'doc']



