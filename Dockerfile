FROM python:3.7-alpine AS builder
WORKDIR /app
COPY . /app
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev make libffi-dev openssl-dev git cargo g++
RUN pip install -I pipenv==2018.11.26

FROM builder AS development
RUN pipenv install --dev
