FROM python:3.10.5

ENV PYTHONUNBUFFERED 1
ENV DOCKERIZE_VERSION v0.7.0

RUN apt-get update \
    && apt-get install -y wget \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apt-get autoremove -yqq --purge wget && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get -y install \
    libpq-dev

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY . .

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]