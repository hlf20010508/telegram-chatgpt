FROM python:3.8.16-slim-bullseye
WORKDIR /telegram-chatgpt
COPY ./ ./

RUN apt-get update &&\
    apt-get install -y libsndfile-dev &&\
    pip install openai python-telegram-bot soundfile numpy &&\
    apt-get clean &&\
    apt-get auto-remove -y
