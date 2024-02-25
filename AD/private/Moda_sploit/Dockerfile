FROM ubuntu:20.04

RUN apt update
RUN apt install -y python3.8 python3-pip python3-gmpy2

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY ./code /code
WORKDIR /code
ENTRYPOINT python3 sploit3.py