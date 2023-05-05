import unittest
from unittest.mock import patch

from src.FileUploader.upload_file import app
from io import BytesIO
import io


class TestFileUpload(unittest.TestCase):


    @patch('src.FileUploader.upload_file.upload_file_to_s3', return_value='file_id')
    @patch('src.FileUploader.upload_file.analyze_file', return_value=True)
    def test_upload_valid_files(self, mock_upload, mock_analyze):
        # Create a mock file to upload
        file = b'This is a test file'
        file = BytesIO(file)
        data = {"files[]": (file, 'test.txt')}
        with app.test_client() as client:
            response = client.post('/upload', data=data, content_type='multipart/form-data')


        # Check that the file was uploaded and analyzed
        self.assertEqual(mock_upload.call_count, 1)
        self.assertEqual(mock_upload.call_args[0][1], 'test.txt')
        self.assertEqual(mock_analyze.call_count, 1)

    def test_upload_document_no_file(self):
        # Mock a POST request without a file object
        with app.test_client() as client:
            response = client.post('/upload')

        # Check that the response status code is 404
        self.assertEqual(response.status_code, 500)

    def test_upload_document_invalid_file(self):

        file = b'test file contents'
        file = BytesIO(file)
        data = {"file": (file, "test.exe")}
        # Mock a POST request with the invalid file object
        with app.test_client() as client:
            response = client.post('/upload', data=data)

        # Check that the response status code is 415
        self.assertEqual(response.status_code, 500)

    @patch('src.FileUploader.upload_file.get_user_file_ids',
           return_value=['file_id'])
    @patch('src.FileUploader.upload_file.get_file_by_file_id',
           return_value=b'file_content')
    def test_download_document_success(self, mock_get_file_by_file_id,
                                       mock_get_user_file_ids):
        # Mock a GET request with a valid fileId and token in the headers
        with app.test_client() as client:
            response = client.get('/download?fileId=file_id', headers={'Authorization': 'Bearer token'})

        # Check that the response status code is 200 and the file content is returned
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'file_content')

        # Check that the get_user_file_ids and get_file_by_file_id
        # functions were called with the correct arguments
        mock_get_user_file_ids.assert_called_once()
        mock_get_file_by_file_id.assert_called_once()

    def test_download_document_invalid_token(self):
        # Mock a GET request with an invalid token in the headers
        with app.test_client() as client:
            response = client.get('/download?fileId=file_id', headers={'Authorization': 'Bearer invalid_token'})

        # Check that the response status code is 404
        self.assertEqual(response.status_code, 404)

    def test_download_document_file_not_found(self):
        # Mock a GET request with a non-existent fileId and a valid token in the headers
        with app.test_client() as client:
            response = client.get('/download?fileId=invalid_file_id',
                                  headers={'Authorization': 'Bearer token'})

        # Check that the response status code is 404
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
