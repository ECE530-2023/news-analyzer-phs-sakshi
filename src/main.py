from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import google
from flask_login import logout_user

from app import app
from src.FileUploader.upload_file import upload_document,download_document
from src.database.create_database import start_database

app.secret_key = "supersecretkey"

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    return upload_document()

@app.route('/uploader')
def uploader():
    return render_template('upload.html')
@app.route('/download', methods=['GET'])
def download():
    return download_document()
@app.route("/")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    # resp = google.get("/oauth2/v2/userinfo")
    # assert resp.ok, resp.text
    # email = resp.json()["email"]
    # check if email is authorized to access the application

    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    email= resp.json()["emails"][0]["value"]
    print("You are {email} on Google".format(email=email))
    return email

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))



if __name__ == '__main__':
    start_database()
    app.run()
