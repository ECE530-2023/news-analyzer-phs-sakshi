FROM python:3.10.3

ENV PYTHONPATH="${PYTHONPATH}:documentAnalyzer/"
ENV GOOGLE_CLIENT_ID=""
ENV GOOGLE_CLIENT_SECRET=""

ENV AWS_S3_ACCESS_KEY=''
ENV AWS_S3_ACCESS_SECRET=''
ENV AWS_S3_BUCKET_NAME=''
# copy the requirements file into the image
COPY requirements.txt /documentAnalyzer/requirements.txt

# switch working directory
WORKDIR /documentAnalyzer

ENV PYHTONUNBUFFERED=1
RUN apt-get update \
  && apt-get -y install tesseract-ocr
# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /documentAnalyzer



# expose port 5000 to the outside world
EXPOSE 8000

# configure the container to run the flask app on port 5000
ENTRYPOINT [ "python" ]
CMD ["src/main.py"]

# to run the container on port 8000, use the following command:
# docker run -p 8000:5000 <image_name>