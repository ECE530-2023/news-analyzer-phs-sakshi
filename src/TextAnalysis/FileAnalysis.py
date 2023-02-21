from flask import Flask, flash, request, redirect, url_for

app = Flask(__name__)


# @Input parameters - keywords to match the paragraphs
# Response -
# 200 - Successful - list of paragraphs
# 400 - Bad Request
# 500 - Internal Server Error
@app.route('/paragraphsByKeyword', methods=['POST'])
def get_paragraphs_by_keywords():
    return '', 200

@app.route('/paragraphsBySentiment', methods=['POST'])
def get_paragraphs_by_sentiment():
    return [], 200

def get_