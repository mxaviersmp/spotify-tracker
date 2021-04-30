# spotify-stats

A Spotify API to collect statistics from users played musics

- Add environment variables: `$ set -a; . ./.env; set +a`

- Init airflow db: `airflow db init`
- copy the `etl/dags` folder to `~/airflow/dags/`
- List dags: `$ airflow dags list`
- Run dag: `$ airflow dags test spotify_etl 2015-06-01`

- Serve api: `$ uvicorn app.api.main:app`

- `$ npm install -g serverless`
- `$ npm install`
- Configure aws credentials for serverless
- `$ sls deploy --region "us-east-1" --stage "dev"`
- `$ sls invoke -f app --path notebooks/data.json --log`
- `$ sls remove --region "us-east-1" --stage "dev"`

- `$ alembic revision --autogenerate`
- `$ bash migrate.sh`

- `$ mkdir ./logs ./plugins`
- `$ echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" >> .env`
- `$ docker-compose up airflow-init`
- `$ docker-compose up -d

![db erd diagram](./spotify-stats-erd.png)
![etl diagram](./spotify-stats-etl.png)
