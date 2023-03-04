We have used SQLite for our database implementation along with cloud.
The database for news feed analyzer has two parts - 
1. SQLite
2. Cloud storage (such as AWS S3)

We will be using SQLite to store our analysis of the documents. However the original documents itself and the text extraction of the documents will be stored on cloud.
We chose a SQL + cloud structure because of the following reasons -
1. We wanted quick and easy access to our analysis of the documents, therefore storing the same in SQLite
2. Since we may have thousands of files, and each file can be very large, we chose to store those files in cloud.
3. The format of our data is very structured, so we felt SQLite would serve us better.
4. Relational Data - SQL is ideal for handling relational data, where data is stored in tables and has a predefined schema.

Advantages of SQLite:
- Lightweight - SQLite is a lightweight database engine, which means it uses very few system resources.
- High Performance: SQLite is fast and efficient. It uses a transactional model and can handle large amounts of data. It also has a small memory footprint, which makes it suitable for high-performance applications.

Advantages of Cloud:
- Scalability - We can scale the database based on the size of the file/number of files
- Reliability - Cloud services are designed to be highly reliable and provide high levels of uptime. We can be sure that we don't lose the files of client and they can download the files everytime.
- Security - Cloud providers invest heavily in security measures to protect their infrastructure and customer data.
- Disaster Recovery: Cloud services offer built-in disaster recovery capabilities, which can help businesses to quickly recover from a catastrophic event such as a natural disaster or cyber attack.

Also, we plan to implement the authentication by Google(handle credentials using Firebase). 
For SQLite we plan to have the following structure - 

Tables:

1. Users Table<br />
   User_id <br />
   permission_set <br />
   email
2. Document Table<br />
 doc_id <br />
   date_uploaded <br />
   date_deleteion <br />
user_id  <br />
doc_link <br />
doc_text_link <br />
sentiment <br />
file size <br />
doc_name <br />
3. Paragraphs Table <br />
para_id <br />
doc_id <br />
sentiment 
4. Keywords Table
   keyword_id <br />
doc_id <br />
para_id <br />
definition <br />
keyword_name

The figure below shows how the tables are connected.
![Database Design](database%20design.png)<br />

This design helps with my APIs since my APIs which are compute heavy, like text analysis API use SQLite to access contents which is faster and utilises cloud for when we need our API to store large amounts of data.
