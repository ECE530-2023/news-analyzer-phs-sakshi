""" tests the text_analyzer and text_analyzer_impl file functions"""
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask

from src.TextAnalysis.text_analyzer_impl import analyze_file, \
    find_keywords_file, \
    find_keywords, analyze_file_sentiment, \
    convert_file_to_text, tag_document_by_keyword

app = Flask(__name__)


class TestAnalyzeFileImpl(unittest.TestCase):

    @patch("src.TextAnalysis.text_analyzer_impl.convert_file_to_text")
    @patch("src.TextAnalysis.text_analyzer_impl.find_keywords_file")
    @patch("src.TextAnalysis.text_analyzer_impl.tag_document_by_keyword")
    @patch("src.TextAnalysis.text_analyzer_impl.analyze_file_sentiment")
    @patch('src.TextAnalysis.text_analyzer_impl.get_document_summary')
    @patch('src.TextAnalysis.text_analyzer_impl.insert_doc', return_value=True)
    def test_analyze_file_success(self, mock_analyze_file_sentiment,
                                  mock_tag_document_by_keyword, mock_find_keywords_file,
                                  mock_convert_file_to_text, mock_summary, mock_insert):
        """ function to test success file analysis"""
        mock_analyze_file_sentiment.return_value = 0.5
        mock_tag_document_by_keyword.return_value = True
        mock_find_keywords_file.return_value = ["keyword1", "keyword2"]
        mock_convert_file_to_text.return_value = "This is some sample text."
        mock_summary.return_value = 'short summary'
        file = MagicMock()
        file_id = "12345.txt"

        analyze_file(file, file_id)
        mock_convert_file_to_text.assert_called_once()
        mock_find_keywords_file.assert_called_once()
        mock_tag_document_by_keyword.assert_called_once()
        mock_analyze_file_sentiment.assert_called_once()

    @patch('src.TextAnalysis.text_analyzer_impl.find_keywords')
    @patch('src.TextAnalysis.text_analyzer_impl.insert_keywords')
    @patch('src.TextAnalysis.text_analyzer_impl.get_definition')
    def test_find_keywords_file(self, mock_get_definition,
                                mock_insert_keywords, mock_find_keywords):
        """ test to find keywords in a file"""
        file = "This is a test file."
        file_id = 1
        keywords = [("test", 1), ("file", 2)]
        mock_find_keywords.return_value = keywords
        mock_get_definition.return_value = "A definition"

        result = find_keywords_file(file, file_id)

        self.assertEqual(result, keywords)
        mock_find_keywords.assert_called_once_with(file)
        expected_calls = [unittest.mock.call(k, file_id, mock_get_definition(k)) for k, t in keywords]
        mock_insert_keywords.assert_has_calls(expected_calls)
        mock_get_definition.assert_any_call("test")
        mock_get_definition.assert_any_call("file")

    def test_find_keywords(self):

        with app.app_context():
            # Call the function with a test file
            file_contents = 'file contents'
            keywords = find_keywords(file_contents)

            # Check that the function returns a list
            self.assertIsInstance(keywords, list)

            # Check that the list has length 2
            self.assertEqual(len(keywords), 2)

            # Check that each item in the list is a tuple
            # with two elements (word, frequency)
            for item in keywords:
                self.assertIsInstance(item, tuple)
                self.assertEqual(len(item), 2)
                self.assertIsInstance(item[0], str)
                self.assertIsInstance(item[1], int)

    def test_convert_file_to_text(self):
        # Test converting a PDF file to text
        # create a temporary PDF file
        with open('temp.pdf', 'w') as f:
            f.write('This is a test PDF file.')
        yield {'filename': 'temp.pdf'}
        # delete the temporary file
        text = convert_file_to_text('temp.pdf')
        assert text == 'This is a test PDF file.'

    @patch('src.TextAnalysis.text_analyzer_impl.insert_paragraph',
           return_value=1)
    @patch('src.TextAnalysis.text_analyzer_impl.find_keywords',
           return_value=[('first', 1), ('second', 1)])
    @patch('src.TextAnalysis.text_analyzer_impl.insert_keywords')
    @patch('src.TextAnalysis.text_analyzer_impl.analyze_paragraph_sentiment')
    @patch('src.TextAnalysis.text_analyzer_impl.insert_keywords_by_para')
    def test_tag_document_by_keyword(self, mock_insert_para,
                                     mock_find_keyword, mock_insert_keys,
                                     mock_analyze_para_senti, mock_insert):
        # Test tagging a document by keyword
        # create a test file with paragraphs
        text = 'This is the first paragraph.\n\n' \
               'This is the second paragraph.' \
               '\n\nThis is the third paragraph.'
        file_id = 1
        result = tag_document_by_keyword(text, file_id)
        self.assertTrue(result)

    @patch("src.TextAnalysis.text_analyzer_impl.convert_file_to_text")
    @patch("src.TextAnalysis.text_analyzer_impl.find_keywords_file")
    @patch("src.TextAnalysis.text_analyzer_impl.tag_document_by_keyword")
    @patch("src.TextAnalysis.text_analyzer_impl.analyze_file_sentiment")
    @patch('src.TextAnalysis.text_analyzer_impl.insert_doc', return_value=True)
    def test_analyze_file_invalid_input_file(self, mock_insert,
                                             mock_analyze_file_sentiment,
                                             mock_tag_document_by_keyword,
                                             mock_find_keywords_file,
                                             mock_convert_file_to_text):
        mock_analyze_file_sentiment.return_value = 0.5
        mock_tag_document_by_keyword.return_value = True
        mock_find_keywords_file.return_value = ["keyword1", "keyword2"]
        mock_convert_file_to_text.return_value = "This is some sample text."

        file = MagicMock()
        file_id = "12345"
        file.read.return_value = b''

        result = analyze_file(file, file_id)

        self.assertFalse(result)
        mock_convert_file_to_text.assert_not_called()
        mock_find_keywords_file.assert_not_called()
        mock_tag_document_by_keyword.assert_not_called()
        mock_analyze_file_sentiment.assert_not_called()
        mock_insert.assert_not_called()

    @patch('src.TextAnalysis.text_analyzer_impl.update_doc_sentiment')
    def test_analyze_file_sentiment_neutral(self, mock_update):
        file = 'This is some sample text with neutral sentiment.'
        file_id = 'test_file_id'
        result = analyze_file_sentiment(file, file_id)

        self.assertEqual(result, 'NEUTRAL')

    @patch('src.TextAnalysis.text_analyzer_impl.update_doc_sentiment')
    def test_analyze_file_sentiment_negative(self, mock_update):
        file = 'This is the worse.I hate it'
        file_id = 'test_file_id'
        result = analyze_file_sentiment(file, file_id)

        self.assertEqual(result, 'NEGATIVE')

    @patch('src.TextAnalysis.text_analyzer_impl.update_doc_sentiment')
    def test_analyze_file_sentiment_positive(self, mock_update):
        file = 'This is some sample text with positive sentiment.' \
               'This is the best.'
        file_id = 'test_file_id'
        result = analyze_file_sentiment(file, file_id)

        self.assertEqual(result, 'POSITIVE')

    def test_analyze_file_no_content(self):
        file = 'non_existing_file'
        file_id = '123'
        self.assertFalse(analyze_file(file, file_id))

    def test_analyze_file_with_unsupported_extension(self):
        file = 'unsupported_file'
        file_id = '123.xyz'
        self.assertFalse(analyze_file(file, file_id))

    def test_analyze_empty_file(self):
        file = 'empty_file.pdf'
        file_id = '123'
        with open(file, 'w') as f:
            f.write('')
        self.assertFalse(analyze_file(file, file_id))

    @patch('src.TextAnalysis.text_analyzer_impl.update_doc_sentiment')
    def test_find_keywords_file_empty_file(self, mock_update):
        file_id = 1234
        file = ''
        res = find_keywords_file(file, file_id)
        self.assertEqual(res, [])
        res = analyze_file_sentiment(file, file_id)
        self.assertEqual(res, 'NEUTRAL')


if __name__ == '__main__':
    unittest.main()
