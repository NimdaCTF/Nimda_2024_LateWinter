FROM python:3.10

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip3.10 install -r requirements.txt

COPY . .

RUN chmod a+x src/docker/*.sh