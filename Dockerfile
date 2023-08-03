FROM python:3.9-slim

WORKDIR /app

ADD dist /app

RUN python3 -m pip install /app/*.whl
