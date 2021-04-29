FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app
COPY requirements.txt /app
COPY setup.py /app

RUN python -m pip --disable-pip-version-check --no-cache-dir install /app/

WORKDIR /app

ENV APP_MODULE=app.api.main:app
