# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /yaari
COPY . /yaari/
RUN cd src && pip install -r requirements.txt
