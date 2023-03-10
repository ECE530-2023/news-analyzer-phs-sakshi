"""Feed Ingester Module"""
from flask import Flask
from src.InputOutput.output import print_string
app = Flask(__name__)


@app.route('/ingestFile', methods=['POST'])
def ingest_file(file):
    """
    :param file: ingest file
    :return: boolean if file was ingested successfully
    """
    if not file:
        return False
    print_string("file saved")
    return True
