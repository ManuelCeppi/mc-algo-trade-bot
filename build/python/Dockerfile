# syntax=docker/dockerfile:1

FROM python:3.7-alpine
RUN apk update
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED 1
CMD tail -f /dev/null
