

def get_user_file_ids(file_id):
    ids = [1, 2, 3, 4]
    return file_id in ids

def get_file_by_fileId(file_id):
    files = {1: 'file 1', 2: 'file 2', 3: 'file 3', 4: 'file 4'}
    return files[file_id]

def is_allowed_file_extension(ext):
    return '.' in ext and \
           ext.rsplit('.', 1)[1].lower() in ['pdf', 'png', 'jpg', 'jpeg', 'csv', 'doc']