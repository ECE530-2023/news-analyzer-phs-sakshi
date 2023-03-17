"""Feed Ingester Module"""
import json
from botocore.exceptions import ClientError
from flask import Flask, request, send_file
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as rq

from src.FileUploader.file_uploader_impl import get_file_size
from src.InputOutput.output import print_string
import boto3

from src.database.Document import insert_doc_link

app = Flask(__name__)


access_key = 'AKIAUPEMIMSKUTBFY366'
access_secret = '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'
bucket_name = 'bucket1-sep'

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=access_secret)

@app.route('/ingestFile', methods=['POST'])
def ingest_file(file):
    """
    :param file: ingest file
    :return: boolean if file was ingested successfully
    """
    if not file:
        return False
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request())
        user_id = idinfo['sub']
    except ValueError:
        # Invalid token
        print_string("couldn't verify user")
    try:
        file_json = json.loads(file)
        file_link = s3.upload_fileobj(file_json["filename"], bucket_name, file_json["filename"])
        file_size = get_file_size(file)
        file_id = insert_doc_link(file_json["filename"], user_id, file_link, file_size)
        print_string('File uploaded successfully!')
        return file_id
    except ClientError as e:
        print_string("Invalid credentials" + e)
        return False
    except Exception as e:
        print_string("Error encountered " + e)
def download_file(url):
    response = rq.get(url)
    file_name = url.split('/')[-1]
    headers = {'Content-Disposition': f'attachment; filename={file_name}'}
    return send_file(response.content, as_attachment=True, attachment_filename=file_name, mimetype='application/octet-stream', headers=headers)
