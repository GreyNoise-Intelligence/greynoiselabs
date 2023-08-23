FROM python:3.7.2-slim

WORKDIR /app

ADD dist /app

RUN python3 -m pip install /app/*.whl
