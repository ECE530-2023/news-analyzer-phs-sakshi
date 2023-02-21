from flask import Flask

app = Flask(__name__)

app.run(host='localhost', port=5000)
@app.route("/")
def document_analyzer_home():
    return "Welcome to document analyzer"
