import io
import unittest
from unittest.mock import patch, MagicMock

from src.FileUploader.file_uploader_impl import get_user_file_ids, get_file_by_file_id, is_allowed_file_extension, get_file_size, get_file_extension


class TestFileUploaderImpl(unittest.TestCase):
    @patch('src.FileUploader.file_uploader_impl.fetch_all_user_file_ids', return_value=['file_id_1', 'file_id_2'])
    def test_get_user_file_ids(self, mock_fetch_all_user_file_ids):
        result = get_user_file_ids()
        self.assertEqual(result, ['file_id_1', 'file_id_2'])

    @patch('src.FileUploader.file_uploader_impl.get_file', return_value={'id': 'file_id_1', 'name': 'test.pdf'})
    def test_get_file_by_file_id(self, mock_get_file):
        result = get_file_by_file_id('file_id_1')
        self.assertEqual(result, {'id': 'file_id_1', 'name': 'test.pdf'})

    def test_is_allowed_file_extension(self):
        self.assertTrue(is_allowed_file_extension('test.pdf'))
        self.assertTrue(is_allowed_file_extension('test.PNG'))
        self.assertFalse(is_allowed_file_extension('test.py'))

    def test_get_file_size(self):
        mock_file = MagicMock()
        mock_file.read.return_value = b'This is a test file'
        self.assertEqual(get_file_size(mock_file), 19)

    def test_get_file_extension(self):
        self.assertEqual(get_file_extension('test.pdf'), 'pdf')
        self.assertEqual(get_file_extension('test.txt'), 'txt')
        self.assertEqual(get_file_extension('test.Png'), 'png')
        self.assertEqual(get_file_extension('test'), False)

    @patch('src.FileUploader.file_uploader_impl.fetch_all_user_file_ids', return_value=[])
    def test_get_user_file_ids_empty_db(self, mock_user_file_ids):
        expected_file_ids = []
        actual_file_ids = get_user_file_ids()
        assert actual_file_ids == expected_file_ids

    @patch('src.FileUploader.file_uploader_impl.get_file', return_value=None)
    def test_get_file_by_file_id_non_existing_file(self, mock_file):
        file_id = 'non_existing_file_id'
        actual_file = get_file_by_file_id(file_id)
        assert actual_file == None

    def test_get_file_size_empty_file(self):
        file = io.BytesIO(b'')
        actual_size = get_file_size(file)
        assert actual_size == 0


if __name__ == '__main__':
    unittest.main()
