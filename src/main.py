import json

from flask import render_template, redirect, url_for, jsonify
from flask_dance.contrib.google import google
from flask_login import logout_user, login_user, login_required, current_user
import requests
import os
from app import app, login_manager
from src.Authentication.User import User
from src.FileUploader.upload_file import upload_document, download_document
from src.database.Users import addUser
from src.database.create_database import start_database
from src.TextAnalysis.file_analysis import get_keyword_definition, analyze_complete_file, document_summary

app.secret_key = "supersecretkey"

@app.route('/swagger.json')
def swagger():
    with open('./static/swagger.json', 'r') as f:
        return jsonify(json.load(f))
@app.route('/')
@app.route('/home')
def home():
    if google.authorized:
        try:
            resp = google.get("/oauth2/v2/userinfo")
            assert resp.ok, resp.text
            email = resp.json()["email"]
            addUser(email)
            login_user(User(email))
            return render_template('home.html', user=email)
        except Exception:
            return render_template('home.html')


@app.route('/about')
def about():
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
        return render_template('about.html',user=user_id)
    return render_template('about.html')
@login_required
@app.route('/file_analysis', methods=['POST'])
def file_analysis():
    user_id = None
    if current_user.is_authenticated:
        return analyze_complete_file()
    return render_template('unauthorized_access.html')

@login_required
@app.route('/upload', methods=['POST'])
async def upload():
    user_id = None
    if current_user.is_authenticated:
        return await upload_document()
    return render_template('unauthorized_access.html')

@login_required
@app.route('/uploader')
def uploader():
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
        return render_template('upload.html', user=user_id)
    return render_template('unauthorized_access.html')
@login_required
@app.route('/download', methods=['GET'])
def download():
    if current_user.is_authenticated:
        return download_document()
    return render_template('unauthorized_access.html')

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('unauthorized_access.html')
@login_required
@app.route('/search', methods=['GET'])
def search():
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
        return render_template('search.html', user=user_id)
    return render_template('unauthorized_access.html')

@login_required
@app.route('/keywordDefinition', methods=['POST'])
def search_keyword_def():
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
        return get_keyword_definition()
    return render_template('unauthorized_access.html')
@app.route("/login/google")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))

@app.route("/logout", methods=['POST'])
def logout():
    if google.authorized:
        # Revoke the user's access token
        access_token = google.token['access_token']
        revoke_url = f'https://accounts.google.com/o/oauth2/revoke?token={access_token}'
        requests.get(revoke_url)

        # Log the user out of the application
        logout_user()

    return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
@login_required
@app.route("/index")
def dashboard():
    if google.authorized:
        try:
            resp = google.get("/oauth2/v2/userinfo")
            assert resp.ok, resp.text
            email = resp.json()["email"]
            addUser(email)
            login_user(User(email))
            return render_template('index.html', user=email)
        except Exception:
            return render_template('unauthorized_access.html')
@login_required
@app.route("/analyze")
def analyze():
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
        return render_template('analyze.html', user=user_id)
    return render_template('unauthorized_access.html')

@app.route('/documentSummary',methods=['POST'])
def document_summary_api():
    """get the summary of the document"""
    if current_user.is_authenticated:
        user_id = current_user.id
        return document_summary()
    return render_template('unauthorized_access.html')

@app.route('/route', methods=['GET'])
def get_about():
    return render_template('about.html')


if __name__ == '__main__':
    start_database()
    app.run(host='0.0.0.0', port=5000)
