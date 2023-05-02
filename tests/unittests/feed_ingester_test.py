import io
import os
import unittest
import unittest.mock as mock
from unittest.mock import patch
import pytest

from src.FeedIngester.ingester_feed import upload_file_to_s3, get_file_url
from botocore.exceptions import ClientError

class TestIngesterFeed(unittest.TestCase):

    @mock.patch('src.FeedIngester.ingester_feed.s3.upload_fileobj')
    def test_upload_file_to_s3(self, mock_upload_fileobj):
        # Set up test data
        file_data = io.BytesIO(b'test data')
        file = mock.MagicMock()
        file.filename = 'test.txt'
        file.content_type = 'text/plain'

        # Call the function
        result = upload_file_to_s3(file_data, file)

        # Assert that the S3 client was called correctly
        mock_upload_fileobj.assert_called_with(
            file_data,
            os.environ.get('AWS_S3_BUCKET_NAME'),
            'test.txt',
            ExtraArgs={'ContentType': 'text/plain'}
        )

        # Assert that the function returns the correct result
        self.assertEqual(result, 'test.txt')

    def test_get_file_url(self):
        # Set up test data
        filename = 'test.txt'

        # Call the function
        result = get_file_url(filename)

        # Assert that the function returns the correct URL
        self.assertEqual(result, 'https://s3.amazonaws.com/' + os.environ.get('AWS_S3_BUCKET_NAME') + '/test.txt')

    def test_get_file_url_with_empty_filename(self):
        filename = ''
        with pytest.raises(ValueError):
            get_file_url(filename)

    @patch('src.FeedIngester.ingester_feed.s3.upload_fileobj')
    def test_upload_error(self, mock_upload_fileobj):
        file_data = io.BytesIO(b'Test data')
        file_data.content_type = 'image/png'
        file = mock_upload_fileobj.return_value

        error_message = 'An error occurred while uploading the file'
        mock_upload_fileobj.side_effect = ClientError({'Error': {'Message': error_message}}, 'operation_name')

        result = upload_file_to_s3(file_data, file)

        assert result == mock_upload_fileobj.side_effect

