"""Tests user authentication module"""
import logging
import src.Authentication.user_authentication_impl as auth_impl


def test_user_authentication_login_user():
    """tests user authentication for logging user"""
    testcases = [
        ['admin', 'admin', True],
        ['u', 'user', False]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert auth_impl.login_user(test[0], test[1]) == test[2]


def test_user_authentication_reset_username():
    """tests user authentication to reset username"""
    testcases = [
        ['u', True],
        ['user', False]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert auth_impl.reset_username(test[0]) == test[1]


def test_user_authentication_reset_password():
    """tests user authentication to reset password"""
    testcases = [
        ['u', 'user', True],
        ['op', 'not found user', False]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert auth_impl.reset_password(test[0], test[1]) == test[2]


test_user_authentication_login_user()
test_user_authentication_reset_username()
test_user_authentication_reset_password()
