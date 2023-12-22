FROM python:3.11.5

RUN apt-get update && apt-get install -y python3-pip && apt-get clean

WORKDIR /djangoproject/
add . /djangoproject/
RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir torch

RUN pip3 install -r requirements.txt
RUN python manage.py makemigrations