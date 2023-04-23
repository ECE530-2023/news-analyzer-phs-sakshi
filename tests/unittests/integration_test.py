import unittest
from unittest.mock import patch
from src.app import app

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_analyze_complete_file(self):
        with patch('src.TextAnalysis.file_analysis.get_text_of_file', return_value='sample text'):
            response = self.client.post('/file_analysis')
            self.assertEqual(response.status_code, 200)

    def test_get_keyword_definition(self):
        with patch('src.TextAnalysis.file_analysis.get_keyword_definition', return_value='test definition'):
            response = self.client.post('/keywordDefinition')
            self.assertEqual(response.status_code, 200)

    def test_upload_and_download_document(self):
        data = {'file': (open('test_file.txt', 'rb'), 'test_file.txt')}
        response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        uploaded_file_id = response.json['file_id']

        response = self.client.get('/download', query_string={'file_id': uploaded_file_id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_file', response.headers['Content-Disposition'])
        self.assertEqual(response.data.decode('utf-8'), 'Test file content.\n')

if __name__ == '__main__':
    unittest.main()
