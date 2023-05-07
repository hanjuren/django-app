FROM python:3.10.5

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install \
    libpq-dev

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY . .

#EXPOSE 8000
#
#CMD ["python", "manage.py", "runserver"]