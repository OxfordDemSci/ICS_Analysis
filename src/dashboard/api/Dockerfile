FROM python:3.11-slim

 

WORKDIR /app

 

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    libexpat1-dev \
    libproj-dev \
    libgeos-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variable
ENV GDAL_VERSION=3.2.2
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

 

COPY . .
RUN chmod 0777 /app/entrypoint.sh
# removing Line Endings > Unix
RUN sed -i -e 's/\r$//' /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]