FROM python:3-slim-stretch

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y git libopus-dev && \
 pip install --trusted-host pypi.python.org -r requirements.txt
