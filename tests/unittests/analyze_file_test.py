import unittest
from unittest.mock import patch, MagicMock
import os
from flask import Flask
import pytest

from src.TextAnalysis.text_analyzer_impl import analyze_file, find_keywords_file, find_keywords, analyze_file_sentiment, \
    convert_file_to_text, tag_document_by_keyword

app = Flask(__name__)

class TestAnalyzeFile(unittest.TestCase):

    @patch("src.TextAnalysis.text_analyzer_impl.convert_file_to_text")
    @patch("src.TextAnalysis.text_analyzer_impl.find_keywords_file")
    @patch("src.TextAnalysis.text_analyzer_impl.tag_document_by_keyword")
    @patch("src.TextAnalysis.text_analyzer_impl.analyze_file_sentiment")
    def test_analyze_file_success(self, mock_analyze_file_sentiment, mock_tag_document_by_keyword, mock_find_keywords_file, mock_convert_file_to_text):
        mock_analyze_file_sentiment.return_value = 0.5
        mock_tag_document_by_keyword.return_value = True
        mock_find_keywords_file.return_value = ["keyword1", "keyword2"]
        mock_convert_file_to_text.return_value = "This is some sample text."

        file = MagicMock()
        file_id = "12345"

        result = analyze_file(file, file_id)

        self.assertTrue(result)
        mock_convert_file_to_text.assert_called_once_with(file)
        mock_find_keywords_file.assert_called_once_with("This is some sample text.", file_id)
        mock_tag_document_by_keyword.assert_called_once_with("This is some sample text.", file_id)
        mock_analyze_file_sentiment.assert_called_once_with("This is some sample text.", file_id)

    @patch("src.TextAnalysis.text_analyzer_impl.convert_file_to_text")
    @patch("src.TextAnalysis.text_analyzer_impl.find_keywords_file")
    @patch("src.TextAnalysis.text_analyzer_impl.tag_document_by_keyword")
    @patch("src.TextAnalysis.text_analyzer_impl.analyze_file_sentiment")
    def test_analyze_file_failure(self, mock_analyze_file_sentiment, mock_tag_document_by_keyword, mock_find_keywords_file, mock_convert_file_to_text):
        mock_analyze_file_sentiment.side_effect = Exception("Sentiment analysis failed")
        mock_tag_document_by_keyword.return_value = True
        mock_find_keywords_file.return_value = ["keyword1", "keyword2"]
        mock_convert_file_to_text.return_value = "This is some sample text."

        file = MagicMock()
        file_id = "12345"

        with self.assertRaises(Exception):
            analyze_file(file, file_id)

        mock_convert_file_to_text.assert_called_once_with(file)
        mock_find_keywords_file.assert_called_once_with("This is some sample text.", file_id)
        mock_tag_document_by_keyword.assert_called_once_with("This is some sample text.", file_id)
        mock_analyze_file_sentiment.assert_called_once_with("This is some sample text.", file_id)

    @patch('src.TextAnalysis.text_analyzer_impl.find_keywords')
    @patch('src.TextAnalysis.text_analyzer_impl.insert_keywords')
    @patch('src.TextAnalysis.text_analyzer_impl.get_definition')
    def test_find_keywords_file(self, mock_get_definition, mock_insert_keywords, mock_find_keywords):
        file = "This is a test file."
        file_id = 1
        keywords = ["test", "file"]
        mock_find_keywords.return_value = keywords
        mock_get_definition.return_value = "A definition"

        result = find_keywords_file(file, file_id)

        self.assertEqual(result, keywords)
        mock_find_keywords.assert_called_once_with(file)
        expected_calls = [unittest.mock.call(k, file_id, mock_get_definition(k)) for k in keywords]
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

            # Check that each item in the list is a tuple with two elements (word, frequency)
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

    @patch('src.TextAnalysis.text_analyzer_impl.insert_paragraph', return_value=1)
    @patch('src.TextAnalysis.text_analyzer_impl.find_keywords', return_value=['first', 'second'])
    @patch('src.TextAnalysis.text_analyzer_impl.insert_keywords')
    @patch('src.TextAnalysis.text_analyzer_impl.analyze_paragraph_sentiment')
    def test_tag_document_by_keyword(self, mock_insert_para, mock_find_keyword, mock_insert_keys, mock_analyze_para_senti):
        # Test tagging a document by keyword
        # create a test file with paragraphs
        text = 'This is the first paragraph.\n\nThis is the second paragraph.\n\nThis is the third paragraph.'
        file_id = 1
        result = tag_document_by_keyword(text, file_id)
        assert result == True


if __name__ == '__main__':
    unittest.main()
