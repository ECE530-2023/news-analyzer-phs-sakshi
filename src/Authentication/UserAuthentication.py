from flask import Flask, jsonify, request

app = Flask(__name__)


#Input - @username - username
# @password - password
# Response - 200 - Login Successfull
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/login')
def login():
    return True

#Input - @email - email
# Response - 200 - Successfull
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/forget_username', methods=['POST'])
def forget_username():
    return True

#Input - @username - username
# Response - 200 - Successfull
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/forget_password', methods=['POST'])
def forget_password():
    return True

#Input - @username - username
# Response - 200 - Successfull
# 401 - Unauthorized
# 500 - Bad Request
@app.route('/update_username', methods=['POST'])
def update_username():
    return True

#Input - @username - username
# Response - 200 - Successfull
# 401 - Unauthorized
# 500 - Bad Request
def update_password():
    return True
