""" User Authentication Module """
import LoginForm
from flask import Flask, request, flash, request

from src.InputOutput.output import print_string
from user_authentication_impl import login_user, reset_username, reset_password
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    """
Input - @username - username
@password - password
Response - 200 - Login Successful
401 - Unauthorized
500 - Bad Request
"""
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        id_token.verify_oauth2_token(token, requests.Request())
        print_string("verified user")
        return 'Success', 200
    except ValueError:
        # Invalid token
        print_string("couldn't verify user")
        return 'Server Error', 500


@app.route('/forget_username', methods=['POST'])
def forget_username():
    """
Input - @email - email
Response - 200 - Successful
401 - Unauthorized
500 - Bad Request
"""
    form = LoginForm()
    args = request.args
    email = args.get('email')
    if form.validate_on_submit():
        if reset_username(email):
            flash('Logged in successfully.')
            return 'Success', 200
        return '', 401
    return 'Server Error', 500


@app.route('/forget_password', methods=['POST'])
def forget_password():
    """
Input - @username - username
Response - 200 - Successful
401 - Unauthorized
500 - Bad Request
"""
    form = LoginForm()
    args = request.args
    username = args.get('username')
    new_password = args.get('new_password')
    if form.validate_on_submit():
        if reset_password(username,new_password):
            flash('Logged in successfully.')
            return 'Success', 200
        return '', 401
    return 'Server Error', 500


@app.route('/update_password', methods=['POST'])
def update_password():
    """
Input - @username - username
Response - 200 - Successful
401 - Unauthorized
500 - Bad Request
"""
    form = LoginForm()
    args = request.args
    username = args.get('username')
    new_password = args.get('new_password')
    if form.validate_on_submit():
        if reset_password(username,new_password):
            flash('Logged in successfully.')
            return 'Success', 200
        return '', 401
    return 'Server Error', 500
