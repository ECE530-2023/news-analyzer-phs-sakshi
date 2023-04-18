""" Implement main logic for file uploader APIs"""
import os

from src.database.Document import fetch_all_user_file_ids
from src.database.Document import get_file


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
           ext.rsplit('.', 1)[1].lower() in ['pdf', 'png', 'jpg', 'jpeg', 'csv', 'doc', 'txt']

def get_file_size(file):
    return len(file.read())

def get_file_extension(ext):
    return '.' in ext and ext.rsplit('.', 1)[1].lower()

