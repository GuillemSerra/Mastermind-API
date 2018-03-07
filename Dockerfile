FROM python:3.6-slim

RUN apt-get update && apt-get install -y python3-dev gcc git

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libssl-dev \
  libxml2-dev libxslt1-dev python3-dev python3-openssl libz-dev

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

COPY ./src /app


#ENTRYPOINT ["gunicorn", "-b 0.0.0.0:8080", "--config=/app/gunicorn_conf.py", "-w 2", "--worker-class", "quart.worker.GunicornUVLoopWorker", "app:app"]
ENTRYPOINT ["python", "-u", "app.py"]
