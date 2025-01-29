FROM python:latest

WORKDIR /app
COPY .. .

#FROM python:3.13-alpine as builder

RUN pip install --no-cache-dir -r requirements.txt

#FROM python:3.13-alpine

COPY /start /start

RUN sed -i 's/\r//' /start
RUN chmod +x /start

