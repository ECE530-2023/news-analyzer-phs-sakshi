import os
import unittest
from io import BytesIO
from unittest import mock, TestCase
from src.FeedIngester.ingester_feed import upload_file_to_s3, get_file_url


class FeedIngesterTest(TestCase):


    @mock.patch('src.FeedIngester.ingester_feed.boto3.client')
    async def test_upload_file_to_s3(self, mock_s3_client):
        # Arrange
        mock_s3 = mock.Mock()
        mock_s3_client.return_value = mock_s3

        file_data = BytesIO(b'test data')
        file_name = 'test_file.txt'

        expected_content_type = 'text/plain'
        expected_bucket_name = 'my-bucket'

        os.environ['AWS_S3_ACCESS_KEY'] = 'my_access_key'
        os.environ['AWS_S3_ACCESS_SECRET'] = 'my_access_secret'
        os.environ['AWS_S3_BUCKET_NAME'] = expected_bucket_name

        # Act
        result = await upload_file_to_s3(file_data, file_name)

        # Assert
        mock_s3.upload_fileobj.assert_called_once_with(
            file_data,
            expected_bucket_name,
            file_name,
            ExtraArgs={
                "ContentType": expected_content_type
            }
        )

        self.assertEqual(result, file_name)

    @mock.patch.dict(os.environ, {
        'AWS_S3_ACCESS_KEY': 'ACCESS_KEY',
        'AWS_S3_ACCESS_SECRET': 'ACCESS_SECRET',
        'AWS_S3_BUCKET_NAME': 'my-bucket'
    })
    def test_get_file_url(self):
        # Test with a valid filename
        url = get_file_url('my-file.txt')
        self.assertEqual(url, 'https://s3.amazonaws.com/my-bucket/my-file.txt')

        # Test with an invalid filename
        with self.assertRaises(ValueError):
            get_file_url(None)

if __name__ == '__main__':
    unittest.main()