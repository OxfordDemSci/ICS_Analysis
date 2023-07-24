FROM python:3.11-slim-buster

WORKDIR /app

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "--config", "gunicorn.config.py", "wsgi:app"]