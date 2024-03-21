FROM python:3.10-slim

RUN apt-get update \
    && apt-get -y install cron \
    && apt-get clean

WORKDIR /app
COPY . .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob \
    && crontab /etc/cron.d/cronjob

CMD ["python", "./start_service.py"]
