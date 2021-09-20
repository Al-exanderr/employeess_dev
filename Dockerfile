# pull official base image
FROM python:3.6.9-alpine

# set work directory into container
WORKDIR /usr/src/app

# set environment variables for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies for Postgre
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy current folder content (project) to container
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]'


