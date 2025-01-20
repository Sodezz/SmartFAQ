FROM python:latest
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./client.py /code/client.py
RUN pip install --no-cache-dir --upgrade -r requirements.txt
LABEL authors="Sodez"

