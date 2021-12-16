FROM python:3.8

COPY ["album.py", "app.py", "requirements.txt", "./"]

RUN pip3 install -r requirements.txt && mkdir results