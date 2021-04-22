# Base image
FROM python:3.9.4-slim

# Maintainer Info
LABEL maintainer="Rahul Brahmal <rahul@imbue.dev>"
LABEL maintainer="Ronak Bansal <ronak@imbue.dev>"

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# install dependencies 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]