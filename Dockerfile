FROM python:3.11 AS builder
WORKDIR /app
COPY . /app
RUN pip install poetry

FROM builder AS development
RUN poetry install
