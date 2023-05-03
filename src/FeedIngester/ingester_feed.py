""" Module for uploading and saving file to Amazon S3 bucket"""

import logging
import boto3
import os
from src.InputOutput.output import print_string


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get('AWS_S3_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_S3_ACCESS_SECRET')
)


async def upload_file_to_s3(file_data, file):
    """

    :param file_data: data of the file to uplaod
    :param file: name of the file to uplaod
    :return: name of the uploaded file
    """
    # filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file_data,
            os.environ.get('AWS_S3_BUCKET_NAME'),
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print_string("Something Happened: " + str(e))
        logging.info("file not uploaded to S3 "+file.filename)
        return e

    # after upload file to s3 bucket, return filename of the uploaded file
    print_string("file uploaded to S3")
    return file.filename


def get_file_url(filename):
    """ gets the url where the file while be stored in S3"""
    if filename:
        return '%s/%s/%s' % (s3.meta.endpoint_url,
                             os.environ.get('AWS_S3_BUCKET_NAME'), filename)
    raise ValueError('Invalid file name')
