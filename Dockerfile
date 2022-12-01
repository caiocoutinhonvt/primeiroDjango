FROM python:3.7.4

WORKDIR /usr/src/app
COPY ./  /usr/src/app
COPY requirements.txt ./

RUN apt-get clean && apt-get update
RUN apt-get install -y gcc python3-dev python-dev build-essential default-libmysqlclient-dev musl-dev python-mysqldb
RUN pip install --upgrade pip --user

RUN pip3 install -r requirements.txt

