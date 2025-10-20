### Запуск приложения через Docker Compose

1. Перейти в корень проекта:
```cd test_task_restapi```

2. Создать файл .env в корне проекта и скопировать туда данные из .enx.example

3. Поднять контейнеры и собрать контейнеры:
```docker-compose up -d```

4. Проверить запуск контейнеров:
```docker ps```
Должны присутствовать:
test_db — база данных Postgres
test_api — FastAPI backend
test_frontend — React frontend

5. Применить миграцию
```docker exec -it test_api alembic upgrade head```
Доступ к приложению:
Backend (FastAPI): [http://localhost:8000](http://localhost:8000)
Frontend (React): [http://localhost:3000](http://localhost:3000)

6. Загрузить тестовые данные в бд
```docker exec -it test_api python /app/seed.py```

7. Остановка и удаление контейнеров
```docker-compose down -v```
