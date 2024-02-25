FROM python:3.10

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip3.10 install -r requirements.txt --no-dependencies

# FIXES
# RUN sed -i 's/from collections import Mapping/from collections.abc import Mapping/' /usr/local/lib/python3.10/site-packages/jwt/api_jwt.py
# RUN sed -i 's/from collections import Mapping/from collections.abc import Mapping/' /usr/local/lib/python3.10/site-packages/jwt/api_jws.py

RUN apt update && apt install openssl -y


COPY api_jws.py /usr/local/lib/python3.10/site-packages/jwt/api_jws.py
COPY api_jwt.py /usr/local/lib/python3.10/site-packages/jwt/api_jwt.py
COPY algorithms.py /usr/local/lib/python3.10/site-packages/jwt/algorithms.py

COPY . .

RUN mkdir ./src/keys &&  \
    openssl genrsa -out ./src/keys/private.pem 2048 && \
    openssl rsa -in ./src/keys/private.pem -out ./src/keys/public.pem -RSAPublicKey_out


# /app/src/docker/app.sh
RUN chmod a+x src/docker/*.sh