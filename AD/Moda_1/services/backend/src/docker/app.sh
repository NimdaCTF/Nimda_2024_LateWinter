#!/bin/bash

alembic revision --autogenerate -m "Database init creation"
alembic upgrade head

cd src

mv /usr/local/lib/python3.10/site-packages/fastapi_users/authentication/strategy/jwt_.py /usr/local/lib/python3.10/site-packages/fastapi_users/authentication/strategy/jwt.py

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:3000