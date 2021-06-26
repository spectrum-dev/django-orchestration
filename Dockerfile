# Base image
FROM python:3.9.5-slim

# Maintainer Info
LABEL maintainer="Rahul Brahmal <rahul@imbue.dev>"

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# Install GCC
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get -y install tzdata && \
    apt-get -y install build-essential && \
    apt-get -y install wget && \
    apt-get clean
    
# install dependencies 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .