""" Implement main logic for file uploader APIs"""


def get_user_file_ids(file_id):
    """
    :param file_id: file id to search
    :return: boolean returns True if file is present in the database
    """
    ids = [1, 2, 3, 4]
    return file_id in ids


def get_file_by_file_id(file_id):
    """
    :param file_id: file id to search database
    :return: file with id = file_id
    """
    files = {1: 'file 1', 2: 'file 2', 3: 'file 3', 4: 'file 4'}
    return files[file_id] if file_id in files else None


def is_allowed_file_extension(ext):
    """
    :param ext: allowed extension for all files
    :return: boolean returns True if extension is allowed
    """
    return '.' in ext and \
           ext.rsplit('.', 1)[1].lower() in ['pdf', 'png', 'jpg', 'jpeg', 'csv', 'doc']
