FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/twitter

ADD Pipfile .
ADD Pipfile.lock .

RUN pip install --no-cache-dir pipenv; pipenv install --system --deploy