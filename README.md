### Описание:
Апи для проекта Yatube. Позволяет создавать посты, комментарии к постам, группы и пользователей.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/inferiown/api_final_yatube.git
```

```
cd api_final_yatube.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры:

Примеры доступны по ссылке 127.0.0.1:8000/redoc/ после запуска проекта.
