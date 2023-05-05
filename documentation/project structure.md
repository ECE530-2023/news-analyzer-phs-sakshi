Python Flask was used to design this application

The project is divided into 4 main modules -
Each module contains a main file and an implementation file. for example for TextAnalysis module - we have a main file - file_analysis.py
where all the apis live and a text_analyzer_impl.py file which contains all the logic for analysis the file, updating the database,etc.
This is consistent for all teh modules.

1. Authentication - The project uses Google authentication for authorizing the user
The Authentication module contains information about User storage

2. FeedIngester module - The module is responsible for uploading and downloading files to the Cloud.
The project utilizes AWS S3 for storing files to the cloud.

3. FileUploader module - The module is responsible for uploading, downloading files to S3 and analyzing the file.
This module acts as a center point for the FeedIngester module and the TextAnalysis module. It internally calls both the modules
and updates the information in the database.

4. TextAnalysis module - The module is responsible for analysing the uploaded files. It extracts the text from files (like jpg, csv, pdf, etc)
and performs in depth analysis to extract the keywords, sentiment, summary of the document.

5. database module - This module is where all the database lives. For more information about the database checkout the database documentation.

6. templates - all the html pages live inside this folder. This is because flask by default searches for all the UI in this folder.
We have a base.html - which acts as a base file for all other pages. We have different pages - home.html - basic home page; analyze.html
- page to analyze files; etc.

the __init__.py file is used for packaging purposes
we have created a python package for this. the jar for the same can be seen under dist folder -> news-analyzer-phs-sakshi-0.0.1.tar.gz

we also have a docker container for the same. (the Dockerfile is used to create the docker image)
