## Установка всех пакетов

``
pip install -r requirements.txt
``

## Разработка

### Создание среды
python3.11 -m venv venv

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

### Запуск сервера:

``
uvicorn main:app --reload
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
