FROM python:3.9-alpine3.13 
LABEL maintainer = "Anubhav Saxena"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app 
WORKDIR /app 
EXPOSE 8000

ARG DEV=false
RUN  pip install --upgrade pip && \
     pip install -r /tmp/requirements.txt && \
     apk add --update --no-cache postgresql-client libpq && \
     apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir psycopg2 \
    && apk del --no-cache .build-deps &&\
    if [ $DEV = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
        
ENV PATH="py/bin:$PATH"

USER django-user
