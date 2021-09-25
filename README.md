# BBBS

### Описание
Сайт предназначен для помощи наставникам в работе с детьми.

### Технологии
- Python 3.9
- Django 3.2.3
- Django Rest Framework 3.12.4
- gunicorn 20.0.4
- Docker
- docker-compose
- Nginx
- Postgres

### Начало работы

1. Склонируйте проект:


```git clone https://github.com/hlystovea/BBBS.git```  


2. Создайте файл .env по примеру env.example.


3. Запустите контейнеры:

```docker-compose up -d```

Frontend подтянется из docker-hub. 

4. Запустите миграции:

```docker-compose exec backend python manage.py migrate --noinput```

5. Соберите статику:

```docker-compose exec backend python manage.py collectstatic --no-input```

6. Создайте своего суперпользователя:

```docker-compose exec backend python manage.py createsuperuser```

7. Сайт будет доступен по адресу:
 
```http://127.0.0.1```


