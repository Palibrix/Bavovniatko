FROM python:3.12
LABEL authors="palibrix"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -ms /bin/bash palibrix

USER palibrix

WORKDIR /home/app
COPY . /home/app/

COPY ./requirements.txt /home/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /home/app/requirements.txt

