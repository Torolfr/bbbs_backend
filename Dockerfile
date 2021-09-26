FROM python:3.9
WORKDIR /code
ENV ./.env .
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./project .