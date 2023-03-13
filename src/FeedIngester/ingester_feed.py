"""Feed Ingester Module"""
from flask import Flask
from src.InputOutput.output import print_string
import boto3
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
    s3.upload_fileobj(file.filename, 'bucket-1', file.filename)
    print_string('File uploaded successfully!')
    return True

ingest_file()