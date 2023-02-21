from flask import Flask, jsonify, request

from src.Authentication.UserAuthenticationImpl import login_user

app = Flask(__name__)


#Input - @username - username
# @password - password
# Response - 200 - Login Successful
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('Logged in successfully.')
        return 'Success', 200
    else:
        return '', 401

#Input - @email - email
# Response - 200 - Successful
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/forget_username', methods=['POST'])
def forget_username():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        return 'Success', 200
    else:
        return '', 401

#Input - @username - username
# Response - 200 - Successful
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/forget_password', methods=['POST'])
def forget_password():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        return 'Success', 200
    else:
        return '', 401

#Input - @username - username
# Response - 200 - Successful
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/update_username', methods=['POST'])
def update_username():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        return 'Success', 200
    else:
        return '', 401

#Input - @username - username
# Response - 200 - Successful
# 401 - Unauthorized
# 500 - Bad Request
def update_password():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        return 'Success', 200
    else:
        return '', 401
