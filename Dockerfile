FROM python:3.7-alpine AS builder
WORKDIR /app
COPY . /app
RUN apk update
RUN apk add sdl2-dev gcc musl-dev freetype-dev sdl2_image-dev sdl2_mixer-dev sdl2_ttf-dev jpeg-dev libpng-dev portmidi-dev
RUN pip install pipenv
RUN pipenv install --dev
