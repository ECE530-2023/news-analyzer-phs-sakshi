Collaborator - Anwesha Saha

Storage Decision Structure:
-------------------------------
We decided to use two forms of storage. This is because we estimate that some data for example entire documents will require expansive and undeterminable amounts of space whereas links and other structured data can be stored in a relational data format for quick access.
1. SQLite
2. Cloud storage (such as AWS S3)

SQLite will be used to store the components and links of the documents and the links will give access to the location where the actual file is stored in cloud.The entire original document and extracted text along with summary will be stored on cloud.

Reason for Storage Structure:
-------------------------------
This structure is chosen because:

1. It gives us faster access to data we immediately require - through SQLite
2. Cloud storage allows us to consider large file sizes and different formats without having to worry about these considerations on local system (dynamic allocation of resources)
3. Without the actual document analysis and the original document, the data is quite structured which is a good fit for a relational database and allows the use of schemas and a table structure

Advantages of Choosing Selected Methods: 
-----------------------------------------
SQLite
- Lightweight
- High Performance - uses a transactional model,small memory footprint(suitable for high-performance applications)

Cloud:
- Scalability - scale database based on size of the file/number of files
- Reliability - intrinsic reliability
- Security - intrinsic security
- Disaster Recovery - built-in disaster recovery

Implement the authentication by Google(handle credentials using Firebase).

Structure of SQLite:
---------------------

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

This design helps with our APIs since these APIs are compute heavy - for example text analysis API uses SQLite to access contents which is faster and utilises cloud for when we need our API to store large amounts of data.
