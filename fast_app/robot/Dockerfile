FROM python:3.10

RUN mkdir /robot

WORKDIR /robot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .