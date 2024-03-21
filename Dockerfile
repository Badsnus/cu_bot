FROM python:3.10-slim

# Установка cron и других необходимых утилит
RUN apt-get update \
    && apt-get -y install cron \
    && apt-get clean

# Копирование скрипта и cron файла в рабочую директорию
WORKDIR /app
COPY . .

# Установка зависимостей Python
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копирование файла cron и активация его
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob \
    && crontab /etc/cron.d/cronjob

# Запуск cron в фоновом режиме
CMD ["cron", "-f"]
CMD ["python", "./bot.py"]
