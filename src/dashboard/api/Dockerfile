FROM python:3.11-slim-buster

 

WORKDIR /app

 

RUN apt-get update && apt-get install -y postgresql-client
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

 

COPY . .
RUN chmod 0777 /app/entrypoint.sh
# removing Line Endings > Unix
RUN sed -i -e 's/\r$//' /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]