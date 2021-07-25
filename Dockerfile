ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/