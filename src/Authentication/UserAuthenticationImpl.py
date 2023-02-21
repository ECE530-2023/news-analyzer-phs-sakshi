

def login_user(username, password):
    d={'u':'p','admin':'admin'}
    return username in d and d[username] == password

def reset_username(u):
    d={'u':'p','admin':'admin'}
    return True

def reset_password(username,newpass):
    d={'u':'p','admin':'admin'}
    if username in d:
        d[username]=newpass
        return True
    return False
