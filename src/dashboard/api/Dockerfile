FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# CMD [ "gunicorn", "--config", "gunicorn.config.py", "wsgi:app"]