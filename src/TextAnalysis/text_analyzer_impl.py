"""tests text analyzer module"""
import pypdf
import pytesseract
from PIL import Image
import csv
import docx
import spacy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from spacy.lang.en.stop_words import STOP_WORDS

from src.FileUploader.file_uploader_impl import get_file_extension
from src.database.Document import update_doc_sentiment, get_text_of_file
from src.database.Keywords import insert_keywords
from src.database.Paragraphs import insert_paragraph, update_para_sentiment, get_para_by_keyword
from src.database.Paragraphs import get_para_by_sentiment


nlp = spacy.load('en_core_web_sm')
def analyze_file(file, file_id):
    """
    :param file: file to analyze
    :return: boolean - True if file was analyzed successfully
    """
    file = convert_file_to_text(file)
    find_keywords_file(file, file_id)
    tag_document_by_keyword(file, file_id)
    analyze_file_sentiment(file, file_id)
    return True


def find_keywords_file(file, file_id):
    """ finds keywords of the file"""
    keywords = find_keywords(file)
    for keyword in keywords:
        insert_keywords(keyword, file_id, get_definition(keyword))
    return keywords

def find_keywords(file):
    keywords = []
    if file:
        # Process the text with spaCy
        doc = nlp(file)

        # Extract the most relevant keywords
        keywords = []
        for token in doc:
            if token.is_stop or token.is_punct or token.is_space:
                continue
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ']:
                keywords.append(token.lemma_)
    return keywords

def analyze_file_sentiment(file, file_id):
    """ analyzes the text present in a file"""
    blob = TextBlob(file, file_id)
    polarity = blob.sentiment.polarity
    update_doc_sentiment(file_id, polarity)
    return polarity

def analyze_paragraph_sentiment(para_id, para, file_id):
    blob = TextBlob(para, file_id)
    polarity = blob.sentiment.polarity
    update_para_sentiment(file_id, polarity, para_id)
    return polarity

def convert_file_to_text(file):
    """converts a given file say an image to text"""
    ext = get_file_extension(file["filename"])
    text = ''
    if ext == 'pdf':
        text = convert_pdf_to_text(file)
    elif ext == 'png':
        text = convert_image_to_text(file)
    elif ext == 'jpg':
        text = convert_image_to_text(file)
    elif ext == 'csv':
        text = convert_csv_to_text(file)
    else:
        text = convert_doc_to_text(file)
    return text

def convert_pdf_to_text(file):
    pdf_reader = pypdf.PdfFileReader(file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

def convert_image_to_text(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

def convert_csv_to_text(file):
    csv_reader = csv.reader(file)

    # Read each row of the CSV file
    text = ''
    for row in csv_reader:
        text += ','.join(row) + '\n'
    return text

def convert_doc_to_text(file):
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
        for keyword in keywords:
            insert_keywords(keyword, para_id, file_id, get_definition(keyword))
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
    definition = definition_div.text.strip()
    return definition


def get_document_summary(file_id):
    """ returns the summary of a file"""
    text = get_text_of_file(file_id)
    doc = nlp(text)
    sentences = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentences:
        for word in sent:
            if word.text.lower() in STOP_WORDS:
                break
        else:
            sentence_scores[str(sent)] = sent.similarity(doc)

    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:3]
    summary = ' '.join(summary_sentences)
    return summary


def get_paragraphs_by_sentiment(sentiment):
    """returns all paragraphs associated with a sentiment"""
    return get_para_by_sentiment(sentiment)


def get_paragraphs_by_keywords(keyword):
    """returns all paragraphs associated with a keyword"""
    return get_para_by_keyword(keyword)
