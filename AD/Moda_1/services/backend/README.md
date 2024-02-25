## Разработка

### Создание среды (в папке backend)
python3.10 -m venv venv

### Запуск

Для Windows:

**In cmd.exe:**

``
venv\Scripts\activate.bat
``

**In PowerShell**

``
venv\Scripts\Activate.ps1
``

Для Linux & MacOS:

``
source venv/bin/activate
``

### Формирование зависимостей

```
pip3.10 freeze > ../requirements.txt
```

### Установка всех пакетов

``
pip3.10 install -r requirements.txt
``

### Проверка пути

Для Windows:

**In cmd.exe:**

``
echo %PATH%
``

**In PowerShell:**

``
$Env:Path
``

Для Linux & MacOS:

``
echo $PATH
``

### Деактивация

Для всех ОС:

``
deactivate
``

### Удаление

Для Linux & MacOS & Windows PowerShell:

``
deactivate
rm -r venv
``

### Установка библиотек

``
python3.11 -m pip install fastapi[all]
``

### Запуск сервера (в src):

``
uvicorn main:app --reload --port 3000
``

### Остановка сервера:

``
exit()
``

### Установка пакетов для БД

Для Linux & MacOS & Windows:

``
pip install sqlalchemy alembic
``

### Миграция

Инициализация для Linux & MacOS & Windows PowerShell:

``
alembic init migrations:
``

Создание ревизии (подготовка будущей миграции):

``
alembic revision --autogenerate -m "Database init creation"
``

Миграция:

``
alembic upgrade <номер ревизии>
``

Переключение на последнюю версию:

``
alembic upgrade head
``
