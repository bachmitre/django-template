FROM python:3

RUN apt-get update && apt-get -y --no-install-recommends install

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
