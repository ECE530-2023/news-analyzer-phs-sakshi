""" Implement main logic for file uploader APIs"""

from src.database.Document import fetch_all_user_file_ids
from src.database.Document import get_file

ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'csv', 'doc', 'txt']


def get_user_file_ids():
    """
    :param user_id: user id to
    :return: all file ids for the user
    """
    file_ids = fetch_all_user_file_ids()
    return file_ids if file_ids else []


def get_file_by_file_id(file_id):
    """
    :param file_id: file id to search database
    :return: file with id = file_id
    """
    return get_file(file_id)


def is_allowed_file_extension(ext):
    """
    :param ext: allowed extension for all files
    :return: boolean returns True if extension is allowed
    """
    return '.' in ext and \
           ext.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size(file):
    """
    :param file: file whose size to calculate
    :return: size of the file
    """
    return len(file.read())


def get_file_extension(filename):
    """
    :param filename: file whose extension to extract
    :return: extension of the file
    """
    ext = '.' in filename and filename.rsplit('.', 1)[1].lower()
    return ext if ext and ext in ALLOWED_EXTENSIONS else False
