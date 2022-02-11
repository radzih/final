FROM python:3.10

WORKDIR /src
COPY requirements.txt /src
RUN pip3 install -r requirements.txt
COPY . /src
