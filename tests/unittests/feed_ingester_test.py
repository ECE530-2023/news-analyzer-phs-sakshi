import unittest
from unittest.mock import Mock, patch
from src.FeedIngester.ingester_feed import upload_file_to_s3

class TestUploadFileToS3(unittest.TestCase):

    @patch('src.FeedIngester.ingester_feed.s3.upload_fileobj')
    def test_upload_file_success(self, mock_upload_fileobj):
        # Mock file object
        file = Mock()
        file.filename = 'test.txt'
        file.content_type = 'text/plain'

        # Call function
        result = upload_file_to_s3(file)

        # Check that the upload_fileobj function was called with the correct arguments
        mock_upload_fileobj.assert_called_once_with(
            file,
            'bucket1-sep',
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        # Check that the function returns the filename of the uploaded file
        self.assertEqual(result, file.filename)

    @patch('src.FeedIngester.ingester_feed.s3.upload_fileobj')
    def test_upload_file_failure(self, mock_upload_fileobj):
        # Mock file object
        file = Mock()
        file.filename = 'test.txt'
        file.content_type = 'text/plain'

        # Mock an exception being raised by the upload_fileobj function
        mock_upload_fileobj.side_effect = Exception('Error uploading file')

        # Call function
        result = upload_file_to_s3(file)

        # Check that the function returns the caught exception
        self.assertIsInstance(result, Exception)

if __name__ == '__main__':
    unittest.main()