import logging
import boto3
from src.InputOutput.output import print_string

access_key = 'AKIAUPEMIMSKUTBFY366'
access_secret = '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'
bucket_name = 'bucket1-sep'

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret
)
def upload_file_to_s3(file_data, file):
    # filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file_data,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print_string("Something Happened: "+ e)
        logging.info("file not uploaded to S3 "+file.filename)
        return e


    # after upload file to s3 bucket, return filename of the uploaded file
    print_string("file uploaded to S3")
    return file.filename

def get_file_url(filename):
    return '%s/%s/%s' % (s3.meta.endpoint_url, bucket_name, filename)