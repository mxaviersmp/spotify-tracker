FROM apache/airflow:2.0.2-python3.8

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential libpq-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

COPY ./app /opt/app
COPY ./requirements.txt /opt/
COPY ./setup.py /opt/

RUN pip install --disable-pip-version-check --user --no-cache-dir install /opt/
