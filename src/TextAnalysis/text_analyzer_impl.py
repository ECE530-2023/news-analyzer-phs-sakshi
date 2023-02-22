"""tests text analyzer module"""


def analyze_file(file):
    """
    :param file: file to analyze
    :return: boolean - True if file was analyzed successfully
    """
    file = convert_file_to_text(file)
    find_keywords(file)
    tag_document_by_keyword(file)
    analyze_text(file)
    return True


def find_keywords(file):
    """ finds keywords of the file"""
    return file.split(' ')[:3]


def analyze_text(file):
    """ analyzes the text present in a file"""
    return True if file else False


def convert_file_to_text(file):
    """converts a given file say an image to text"""
    return True if file else False


def tag_document_by_keyword(file):
    """tags each paragraph in the file with a keyword"""
    return True if file else False


def get_definition(keyword):
    """ returns the definition of a keyword"""
    words = {'sun': 'sun def', 'moon': 'moon def'}
    return words[keyword] if keyword in words else None


def get_document_summary(file_id):
    """ returns the summary of a file"""
    summary = {1: 'doc 1', 2: 'doc 2'}
    return summary[file_id] if file_id in summary else None


def get_paragraphs_by_sentiment(sentiment):
    """returns all paragraphs associated with a sentiment"""
    paragraphs = {'positive': ['para 1 file 1', 'para 6 file 2'],
                  'negative': ['para 1 file 2', 'para 3 file 3'],
                  'neutral': ['para n file 4', 'para 4 file 9']}
    return paragraphs[sentiment] if sentiment in paragraphs else None


def get_paragraphs_by_keywords(keyword):
    """returns all paragraphs associated with a keyword"""
    paragraphs = {'key1': ['para 1 file 1', 'para 6 file 2'],
                  'key2': ['para 1 file 2', 'para 3 file 3'],
                  'key3': ['para n file 4', 'para 4 file 9']}
    return paragraphs[keyword] if keyword in paragraphs else None
