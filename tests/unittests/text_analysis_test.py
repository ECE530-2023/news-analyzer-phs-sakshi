"""tests text analysis module"""
import src.TextAnalysis.text_analyzer_impl as text_analyzer


def test_analyze_file():
    """tests file analysis"""
    testcases = [
        ['file 1', True],
        [None, False]
    ]
    for test in testcases:
        text_analyzer.analyze_file(test[0] == test[1])


def test_find_keywords():
    """ tests finding keywords in a file"""
    testcases = [
        ['file 1', ['file', '1']],
        ['file', ['file']],
        [None, []]
    ]
    for test in testcases:
        text_analyzer.find_keywords_file(test[0] == test[1])


def test_analyze_text():
    """ tests analyzing text"""
    testcases = [
        ['file 1', True],
        [None, False]
    ]
    for test in testcases:
        text_analyzer.analyze_file_sentiment(test[0] == test[1])


def test_convert_file_to_text():
    """tests extracting text from different types of file"""
    testcases = [
        ['file 1', True],
        [None, False]
    ]
    for test in testcases:
        text_analyzer.convert_file_to_text(test[0] == test[1])


def test_tag_document_by_keyword():
    """ tests tagging each paragraph in a document with a keyword"""
    testcases = [
        ['file 1', True],
        [None, False]
    ]
    for test in testcases:
        text_analyzer.tag_document_by_keyword(test[0] == test[1])


def test_get_definition():
    """ tests getting definition for a keyword"""
    testcases = [
        ['sun', 'sun def'],
        ['no word', None]
    ]
    for test in testcases:
        text_analyzer.get_definition(test[0] == test[1])

def test_get_document_summary():
    """ tests getting a summary for the file"""
    testcases = [
        [1, 'doc 1'],
        [10, None]
    ]
    for test in testcases:
        text_analyzer.get_document_summary(test[0] == test[1])


def test_get_paragraphs_by_sentiment():
    """ tests fetching all paragraphs that belong to a sentiment"""
    testcases = [
        ['positive', ['para 1 file 1', 'para 6 file 2']],
        ['no sentiment', None]
    ]
    for test in testcases:
        text_analyzer.get_paragraphs_by_sentiment(test[0] == test[1])

def test_get_paragraphs_by_keywords():
    """ tests fetching all paragraphs by a keyword"""
    testcases = [
        ['key2', ['para 1 file 2', 'para 3 file 3']],
        ['no key', None]
    ]
    for test in testcases:
        text_analyzer.get_paragraphs_by_keywords(test[0] == test[1])


test_analyze_file()
test_find_keywords()
test_analyze_text()
test_convert_file_to_text()
test_tag_document_by_keyword()
test_get_paragraphs_by_keywords()
test_get_paragraphs_by_sentiment()
test_get_document_summary()
test_get_definition()
