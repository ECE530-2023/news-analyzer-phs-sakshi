Overview -
The application is built using Python and can analyze documents in various formats, including PDF, Microsoft Word,
and plain text files. The application can identify entities, relationships, keywords and sentiments in the text,
and it can generate reports summarizing the information in the document.

Setup -
(I had the values for 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'AWS_S3_ACCESS_KEY', 'AWS_S3_ACCESS_SECRET','AWS_S3_BUCKET_NAME' set in my local,
but due to security reasons I have replaced them with an empty string. If you want to run the application, ping me, I can provide you the credentials)

1. if running locally (after cloning the repository) -
- install Python 3
- set PYTHONPATH as "${PYTHONPATH}:/path/to/your/project"
- set environment variables for 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'AWS_S3_ACCESS_KEY', 'AWS_S3_ACCESS_SECRET','AWS_S3_BUCKET_NAME'
- install all packages using requirements.txt
- run the application using terminal (mac)
    - cd path/to/project
    - python src/main.py
2. if running using docker -
    - set values variables for 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'AWS_S3_ACCESS_KEY', 'AWS_S3_ACCESS_SECRET','AWS_S3_BUCKET_NAME' in the Dockerfile
    - open the terminal
    - cd path/to/project
    - start docker
    - enter command - docker build -t news-analyzer-phs-sakshi .
    - enter command - docker run -d -p 8000:5000 news-analyzer-phs-sakshi
    - open port 127.0.0.1:8000 to see the application



Usage
To use the Smart Document Analyzer, you will need to provide it with a document to analyze.
The application supports the following file formats:
    - PDF (.pdf)
    - Microsoft Word (.docx)
    - Plain text (.txt)
    - Image (.png/.jpg/.jpeg)

To analyze a document, run the src/main.py script and upload the file.
The application will analyze the document and generate a report summarizing the information in the document.

Customers -
1. Application developers
2. Analysts

The homepage leads to a page displaying some basic text indicating that the application is successfully running.

User stories -
Authentication module -
- User should be able to login using a google account

File Upload module -
- User should be able to upload documents in different formats(jpg,pdf,csv,doc,png)
- User should be able to download his past documents

Text Analysis module -
- User should be able to see document summary
- User should be able to find all paragraphs related to a sentiment(positive/negative/neutral)
- User should be able to find the definition for a given keyword
- see all the keywords associated with a file
- Used NLTK library for tokenization and getting the keywords, summary and sentiment

File Ingester module -
- User should be able to ingest files to AWS S3

I would prefer an entity based module for this project.


Features

1. Swagger URL as our main API documentation - go to http://127.0.0.1/swagger for checking out the API documentation.
It contains information about what each API does, their error codes, input parameters, output parameters.

2. Google Authentication - Users should be authorized by google to upload/download/analyze files.

3. We used flake8 for linting

4. AWS S3 for storing files, since files can be large.

5. Project is containerized using docker.

6. Security - all the SQL queries are formed dynamically to prevent SQL query injection.

7. Unit tests - we have sunny and non-sunny unit tests for each module

8. We used async/ await (we implemented this for the FeedIngester and the TextAnalysis module) to have multiprocessing in the project

Future work - 
- Add support for more file formats, such as HTML, XML, and JSON.
- Enhance the security of the application by implementing additional authentication mechanisms, such as two-factor authentication or OAuth.
- Implement permission set for users, such as upload only, download only, etc.
- Integrate the application with third-party data sources such as news feeds, social media, and web pages, to provide additional context and insights into the analyzed documents.