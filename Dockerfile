FROM python:latest
WORKDIR /app
COPY .. .
RUN pip install --no-cache-dir -r requirements.txt
COPY /start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

