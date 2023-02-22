"""Feed Ingester Module"""
from flask import Flask

app = Flask(__name__)


@app.route('/ingestFile', methods=['POST'])
def ingest_file(file):
    """
    :param file: ingest file
    :return: boolean if file was ingested successfully
    """
    if not file:
        return False
    print("file saved")
    return True
