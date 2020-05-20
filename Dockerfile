FROM python:3.7
LABEL AUTHOR="Lucas Biason"
LABEL version="1.0"

ENV PYTHONUNBUFFEDRED 1

COPY ./requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get install -y \
       gcc libc-dev libpq-dev python-dev
RUN pip install -r requirements.txt
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app
