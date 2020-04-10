FROM python:3.7.6-buster as builder

WORKDIR /app

COPY setup.py requirements.txt /app/
RUN pip install -r requirements.txt && \
    pip install -e .

COPY . /app/

ENV PYTHONUNBUFFERRED=1
ENV SENTRY=1

ENTRYPOINT ["guillotina"]

