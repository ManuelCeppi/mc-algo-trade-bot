# syntax=docker/dockerfile:1

FROM python:alpine3.19
RUN apk update
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED 1
CMD tail -f /dev/null
