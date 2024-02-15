## API для реализации денежных транзакций + Swagger


Инструкция

### Клонирование репозитория на локальный компьютер
### Cоздание и активация виртуального окружения
    - python -m venv venv
    - venv/Scripts/activate
    - pip install -r req.txt
### Создание и применение миграций
    - python manage.py makemigrations
    - python manage.py migrate
### Запуск локального сервера Django
    - python manage.py runserver
### Тестирование функционала
    - регистрация пользователяпо по username,password на ендпоинте /auth/register
    - получение access токена по учетным данным на ендпоинте /auth/token
    - ввод токена в Authorize в формате "Bearer {access_token}"
