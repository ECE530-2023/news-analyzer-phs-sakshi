"""tests text analyzer module"""

import logging
import csv
import string
from heapq import nlargest

import pypdf
import pytesseract
import nltk
import textract
import docx
import requests


from PIL import Image
from bs4 import BeautifulSoup
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize

from src.FileUploader.file_uploader_impl import get_file_extension
from src.database.Document import update_doc_sentiment, \
    insert_doc, get_file_by_id
from src.database.Keywords import insert_keywords, insert_keywords_by_para
from src.database.Paragraphs import insert_paragraph, update_para_sentiment, get_para_by_keyword
from src.database.Paragraphs import get_para_by_sentiment
from src.FeedIngester.ingester_feed import get_file_url

nltk.download('stopwords')
nltk.download('punkt')


async def analyze_file(file, file_id):
    """
    :param file: file to analyze
    file_id : file name of the current file to analyze
    :return: boolean - True if file was analyzed successfully
    """
    file_extension = get_file_extension(file_id)
    if file_extension:
        file_data = convert_file_to_text(file, file_extension)
        if file_data:
            find_keywords_file(file_data, file_id)
            logging.info("found keywords ")
            tag_document_by_keyword(file_data, file_id)
            logging.info("tagged document ")
            sentiment = analyze_file_sentiment(file_data, file_id)
            logging.info("sentiment analysis complete ")
            file_size = len(file_data)
            summary = get_document_summary(file_data)
            insert_doc(file_id, get_file_url(file_id), file_data, sentiment, file_size, summary)
            logging.info("file saved successfully ")
            return file_extension
    else:
        return False


def find_keywords_file(file, file_id):
    """ finds keywords of the file"""
    keywords = find_keywords(file)
    for keyword, ct in keywords:
        insert_keywords(keyword, file_id, get_definition(keyword))
    return keywords


def find_keywords(file):
    """
    :param file: file to extract keywords from
    :return: keywords of the file
    """
    tokens = word_tokenize(file)
    stop_words = set(stopwords.words('english'))
    stop_words.update(list(string.punctuation))
    keywords = [word.lower() for word in tokens if word.lower() not in stop_words]
    print(keywords)
    fdist = FreqDist(keywords)
    #
    # # Print the 10 most common words (i.e. the keywords)
    print(fdist.most_common(10))
    return fdist.most_common(10)


def analyze_file_sentiment(file, file_id):
    """ analyzes the text present in a file"""
    blob = TextBlob(file)
    sentiment = blob.sentiment.polarity
    if sentiment < 0.0:
        sentiment = 'NEGATIVE'
    elif sentiment > 0.5:
        sentiment = 'POSITIVE'
    else:
        sentiment = 'NEUTRAL'
    update_doc_sentiment(file_id, sentiment)
    return sentiment


def analyze_paragraph_sentiment(para_id, para, file_id):
    """ get the sentiment associated with a paragraph """
    blob = TextBlob(para)
    sentiment = blob.sentiment.polarity
    if sentiment < -1.0:
        sentiment = 'NEGATIVE'
    elif sentiment > 1.0:
        sentiment = 'POSITIVE'
    else:
        sentiment = 'NEUTRAL'
    update_para_sentiment(file_id, sentiment, para_id)
    return sentiment


def convert_file_to_text(file, file_extension):
    """ Extract text from the file based on its extension """

    if file_extension == 'pdf':
        text = convert_pdf_to_text(file)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        text = convert_image_to_text(file)
    elif file_extension == 'csv':
        text = convert_csv_to_text(file)
    elif file_extension == 'docx':
        text = convert_doc_to_text(file)
    else:
        text = file.read().decode('utf-8')
    # extract text from other file types using Textract library
    return text if text else ''


def convert_pdf_to_text(file):
    """ extract the text from a pdf file """
    pdf_reader = pypdf.PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


def convert_image_to_text(file):
    """ extract text from image """
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text


def convert_csv_to_text(file):
    """ extract text from csv file """
    csv_reader = csv.reader(file)

    # Read each row of the CSV file
    text = ''
    for row in csv_reader:
        text += ','.join(row) + '\n'
    return text


def convert_doc_to_text(file):
    """ extract text from .docx file """
    text = ''
    doc = docx.Document(file)
    for para in doc.paragraphs:
        text += para.text
    return text


def tag_document_by_keyword(file, file_id):
    """tags each paragraph in the file with a keyword"""
    paragraphs = file.split('\n\n')
    for para in paragraphs:
        para_id = insert_paragraph(file_id, para)
        keywords = find_keywords(para)
        for keyword, ct in keywords:
            insert_keywords_by_para(keyword, para_id, file_id, get_definition(keyword))
        analyze_paragraph_sentiment(para_id, para, file_id)
    return True


def get_definition(keyword):
    """ returns the definition of a keyword"""
    # Construct the URL for the Merriam-Webster dictionary
    url = f"https://www.merriam-webster.com/dictionary/{keyword}"

    # Send a GET request to the URL and get the response
    response = requests.get(url)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div element that contains the definition
    definition_div = soup.find('div', class_='sense')

    # Extract the text of the definition from the div element
    if definition_div:
        definition = definition_div.text.strip()
        return definition
    return ' '


def get_document_summary(text):
    """ returns the summary of a file"""
    try:
        sentences = sent_tokenize(text)
        word_frequencies = {}
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence):
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        maximum_frequency = max(word_frequencies.values())
        for word in word_frequencies:
            word_frequencies[word] = word_frequencies[word]/maximum_frequency

        # Calculate the score of each sentence based on the sum of the scores of its words
        sentence_scores = {}
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_frequencies.keys():
                    if len(sentence.split(' ')) < 30:
                        if sentence not in sentence_scores.keys():
                            sentence_scores[sentence] = word_frequencies[word]
                        else:
                            sentence_scores[sentence] += word_frequencies[word]

        # Print the summary, which consists of the three highest-scoring sentences
        summary_sentences = nlargest(3, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        return summary
    except Exception:
        return ''


def get_paragraphs_by_sentiment(sentiment):
    """returns all paragraphs associated with a sentiment"""
    return get_para_by_sentiment(sentiment)


def get_paragraphs_by_keywords(keyword):
    """returns all paragraphs associated with a keyword"""
    return get_para_by_keyword(keyword)


def get_file_info(file_id):
    """ get the information of the file using file name """
    return get_file_by_id(file_id)