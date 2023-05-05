FROM python:3.10.3

ENV PYTHONPATH="${PYTHONPATH}:documentAnalyzer/"
ENV GOOGLE_CLIENT_ID="427430065548-1ldttecl3sapmnb14ho8vieh41dsi7jf.apps.googleusercontent.com"
ENV GOOGLE_CLIENT_SECRET="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"

ENV AWS_S3_ACCESS_KEY='AKIAUPEMIMSKUTBFY366'
ENV AWS_S3_ACCESS_SECRET='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'
ENV AWS_S3_BUCKET_NAME='bucket1-sep'
# copy the requirements file into the image
COPY requirements.txt /documentAnalyzer/requirements.txt

# switch working directory
WORKDIR /documentAnalyzer


# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /documentAnalyzer



# expose port 5000 to the outside world
EXPOSE 8000

# configure the container to run the flask app on port 5000
ENTRYPOINT [ "python" ]
CMD ["src/start_app.py"]

# to run the container on port 8000, use the following command:
# docker run -p 8000:5000 <image_name>