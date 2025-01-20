FROM python:latest
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./server.py /code/server.py
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["fastapi", "run", "/code/server.py", "--port", "8000"]
LABEL authors="Sodez"

