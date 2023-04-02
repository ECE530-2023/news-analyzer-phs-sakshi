import os
from werkzeug.utils import secure_filename
import boto3

access_key = 'AKIAUPEMIMSKUTBFY366'
access_secret = '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'
bucket_name = 'bucket1-sep'

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret
)
def upload_file_to_s3(file):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e


    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename