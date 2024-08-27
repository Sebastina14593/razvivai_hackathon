FROM python:3.11-slim

RUN mkdir code
WORKDIR code

ADD . /code/
ADD .env.docker /code/.env

ENV APP_NAME=DOCKER_DEMO

RUN pip install -r requirements.txt

CMD gunicorn hackathon.wsgi:application -b 0.0.0.0:8000