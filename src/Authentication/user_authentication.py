""" User Authentication Module """
from src.app import app

import os
from flask import Flask, render_template, session, redirect, request, url_for
from google.auth.transport import requests

app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['GOOGLE_CLIENT_ID'] = '427430065548-1ldttecl3sapmnb14ho8vieh41dsi7jf.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'
app.config['GOOGLE_DISCOVERY_URL'] = 'https://accounts.google.com/.well-known/openid-configuration'

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    state = os.urandom(24)
    session['state'] = state
    google_client_id = app.config['GOOGLE_CLIENT_ID']
    redirect_uri = url_for('oauth2callback', _external=True)
    authorize_url = f'{app.config["GOOGLE_DISCOVERY_URL"]}/auth?response_type=code&client_id={google_client_id}&redirect_uri={redirect_uri}&state={state}&scope=openid%20email%20profile'
    return redirect(authorize_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    if state != request.args.get('state'):
        return 'Invalid state parameter', 400
    code = request.args.get('code')
    google_client_id = app.config['GOOGLE_CLIENT_ID']
    google_client_secret = app.config['GOOGLE_CLIENT_SECRET']
    redirect_uri = url_for('oauth2callback', _external=True)
    token_url, headers, body = requests.authenticated_http(
        requests.Request(),
        google_client_id,
        google_client_secret,
        code,
        redirect_uri)
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google_client_id, google_client_secret)
    )
    id_token = token_response.json()['id_token']
    try:
        userinfo = id_token.verify_oauth2_token(
            id_token, requests.Request(), google_client_id)
        session['user'] = userinfo['email']
        return redirect(url_for('index'))
    except ValueError:
        return 'Invalid token', 400



# @app.route('/login', methods=['POST'])
# def login():
#     """
# Input - @username - username
# @password - password
# Response - 200 - Login Successful
# 401 - Unauthorized
# 500 - Bad Request
# """
#     token = request.headers.get('Authorization').split(' ')[1]
#     try:
#         id_token.verify_oauth2_token(token, requests.Request())
#         print_string("verified user")
#         return 'Success', 200
#     except ValueError:
#         # Invalid token
#         print_string("couldn't verify user")
#         return 'Server Error', 500
#
#
# @app.route('/forget_username', methods=['POST'])
# def forget_username():
#     """
# Input - @email - email
# Response - 200 - Successful
# 401 - Unauthorized
# 500 - Bad Request
# """
#     form = LoginForm()
#     args = request.args
#     email = args.get('email')
#     if form.validate_on_submit():
#         if reset_username(email):
#             flash('Logged in successfully.')
#             return 'Success', 200
#         return '', 401
#     return 'Server Error', 500
#
#
# @app.route('/forget_password', methods=['POST'])
# def forget_password():
#     """
# Input - @username - username
# Response - 200 - Successful
# 401 - Unauthorized
# 500 - Bad Request
# """
#     form = LoginForm()
#     args = request.args
#     username = args.get('username')
#     new_password = args.get('new_password')
#     if form.validate_on_submit():
#         if reset_password(username,new_password):
#             flash('Logged in successfully.')
#             return 'Success', 200
#         return '', 401
#     return 'Server Error', 500
#
#
# @app.route('/update_password', methods=['POST'])
# def update_password():
#     """
# Input - @username - username
# Response - 200 - Successful
# 401 - Unauthorized
# 500 - Bad Request
# """
#     form = LoginForm()
#     args = request.args
#     username = args.get('username')
#     new_password = args.get('new_password')
#     if form.validate_on_submit():
#         if reset_password(username,new_password):
#             flash('Logged in successfully.')
#             return 'Success', 200
#         return '', 401
#     return 'Server Error', 500
