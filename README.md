# Афиша интересных мест Москвы

Django-приложение, которое отображает карту с достопримечательностями.
В админке можно редактировать места и фотографии.

## Запуск

Установите зависимости:

- `pip install -r requirements.txt`

Переменные окружения:

- DEBUG=True
- SECRET_KEY=your-secret-key
- ALLOWED_HOSTS=127.0.0.1,localhost
- DB_ENGINE=django.db.backends.sqlite3
- DB_NAME=db.sqlite3

Примените миграции и создайте суперпользователя:

- `python manage.py migrate`
- `python manage.py createsuperuser`

Запуск сервера:

- `python manage.py runserver`

Сайт будет доступен на http://127.0.0.1:8000/

Админка: http://127.0.0.1:8000/admin/

## Загрузка данных

Можно загрузить место из JSON по URL:

- `python manage.py load_place "https://example.com/place.json"`

JSON должен содержать следующую структуру:
```
{
  "title": "Название места",
  "imgs": [
    "https://example.com/media/photo1.jpg",
    "https://example.com/media/photo2.jpg"
  ],
  "description_short": "Краткое описание.",
  "description_long": "Полное описание",
  "coordinates": {
    "lng": "37.50169",
    "lat": "55.816591"
  }
}
```
