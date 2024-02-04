# Moda CTF Web Application
## WEB | X

Описание:
Уязвимость в авторизации.

> FLAG: `X`

## Сборка и запуск:

``
$ docker-compose up -d --build
``

Протестировать http://localhost:8080 (frontend) и http://localhost:3000 (backend)

### !!! Важно !!!

В переменную окружения DB_HOST должно прописываться название контейнера бд, в нашем случае - db
