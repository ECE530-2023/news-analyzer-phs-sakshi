"""logic to implement user authentication APIs"""


def login_user(username, password):
    """
    :param username: username to login to
    :param password: password of the user
    :return: boolean: if username and password match
    """
    users = {'u': 'p', 'admin': 'admin'}
    return username in users and users[username] == password


def reset_username(email):
    """
    :param email: email to check if the user is present or not
    :return: boolean to check if the user is present in the database
    """
    emails = {'u': 'p', 'admin': 'admin'}
    return email in emails


def reset_password(username, new_password):
    """
    :param username: username to reset password for
    :param new_password: new password to set
    :return: boolean if we were able to set new password associated with the username
    """
    users = {'u': 'p', 'admin': 'admin'}
    if username in users:
        users[username] = new_password
        return True
    return False
