FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN apt-get -y install libpq-dev python3-dev

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/