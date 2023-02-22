""" Module to test file uploader module"""
import logging
import src.FileUploader.file_uploader_impl as file_uploader


def test_get_user_file_ids():
    """ tests function to get file by id"""
    testcases = [
        [2, True],
        [10, False]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert file_uploader.get_user_file_ids(test[0]) == test[1]


def test_get_file_by_file_id():
    """ tests fetching a file using file id"""
    testcases = [
        [2, 'file 2'],
        [10, None]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert file_uploader.get_user_file_ids(test[0]) == test[1]


def test_is_allowed_file_extension():
    """ tests if extension is allowed or not"""
    testcases = [
        ['file_2.pdf', True],
        ['file_1.json', False]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert file_uploader.get_user_file_ids(test[0]) == test[1]
