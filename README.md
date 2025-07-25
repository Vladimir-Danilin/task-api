## Task API
Простой REST API сервис для управления списком задач.

Функционал
- Создание задачи
- Просмотр списка задач с фильтрацией по статусу
- Обновление задачи (title, description, status)
- Удаление задачи
- токен-авторизация
- Тесты
- Миграции

Запуск
1. Клонировать репозиторий ```git clone https://github.com/Vladimir-Danilin/task-api.git```
2. Настроить .env если необходимо ```src/.env```
3. Запустить базу данных и сервис ```docker-compose up --build```

API будет доступен по адресу: http://localhost:8000

Документация Swagger: http://localhost:8000/docs
