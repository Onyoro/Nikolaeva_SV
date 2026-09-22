# Notes API

REST API для управления заметками с категориями. Учебная практика по направлению 01.03.02 «Прикладная математика и информатика», группа ИИПМИ-24.

**Демо:** https://notes-api-nikolaeva.onrender.com

## Описание проекта

Проект представляет собой REST API-сервис для создания, чтения, обновления и удаления заметок. Заметки можно объединять в категории. Взаимодействие с API осуществляется по HTTP, данные передаются в формате JSON.

Дополнительно реализована интерактивная HTML-страница, через которую можно работать с заметками прямо в браузере.

## Технологии

- **Python 3.9+**
- **Flask** — веб-фреймворк
- **Flask-SQLAlchemy** — ORM для работы с базой данных
- **PostgreSQL** — база данных
- **Flask-CORS** — поддержка CORS для кросс-доменных запросов
- **Gunicorn** — WSGI-сервер для production
- **Docker / Docker Compose** — контейнеризация
- **pytest** — unit-тестирование
- **Render** — хостинг

## Структура проекта

```
Nikolaeva_SV/
    app/
        __init__.py         # Инициализация пакета
        main.py             # Основной файл приложения
        templates/
            index.html      # Интерактивная HTML-страница
    scripts/
        log_processor.py    # Скрипт-обработчик логов (мини-проект)
        sample.log          # Пример файла логов
    tests/
        test_notes.py       # Unit-тесты для API
    .env.example            # Пример переменных окружения
    .gitignore
    Dockerfile              # Инструкция для сборки образа
    docker-compose.yml      # Запуск приложения вместе с БД
    Procfile                # Команда запуска для Render
    requirements.txt        # Зависимости проекта
    README.md               # Этот файл
```

## API эндпоинты

### Заметки

| Метод | URL | Описание |
|---|---|---|
| `GET` | `/api/notes` | Получить все заметки |
| `GET` | `/api/notes?page=1&per_page=10` | Постраничный вывод |
| `GET` | `/api/notes?category=1` | Фильтр по категории |
| `GET` | `/api/notes/<id>` | Получить заметку по ID |
| `POST` | `/api/notes` | Создать заметку |
| `PUT` | `/api/notes/<id>` | Обновить заметку |
| `DELETE` | `/api/notes/<id>` | Удалить заметку |

### Категории

| Метод | URL | Описание |
|---|---|---|
| `GET` | `/api/categories` | Получить все категории |
| `POST` | `/api/categories` | Создать категорию |

### Формат ответа для заметок

```json
{
  "id": 1,
  "title": "Заголовок",
  "content": "Текст заметки",
  "created_at": "2025-09-23T10:15:23",
  "updated_at": "2025-09-23T10:15:23",
  "category": "Работа",
  "category_id": 2
}
```

## Примеры API-запросов

### Получить все заметки

```bash
curl https://notes-api-nikolaeva.onrender.com/api/notes
```

### Получить заметки с пагинацией

```bash
curl "https://notes-api-nikolaeva.onrender.com/api/notes?page=1&per_page=5"
```

### Получить заметки по категории

```bash
curl "https://notes-api-nikolaeva.onrender.com/api/notes?category=1"
```

### Создать заметку

```bash
curl -X POST https://notes-api-nikolaeva.onrender.com/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Моя заметка","content":"Текст заметки"}'
```

### Создать заметку с категорией

```bash
curl -X POST https://notes-api-nikolaeva.onrender.com/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Рабочая заметка","content":"Текст","category_id":1}'
```

### Обновить заметку

```bash
curl -X PUT https://notes-api-nikolaeva.onrender.com/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Новый заголовок"}'
```

### Удалить заметку

```bash
curl -X DELETE https://notes-api-nikolaeva.onrender.com/api/notes/1
```

### Создать категорию

```bash
curl -X POST https://notes-api-nikolaeva.onrender.com/api/categories \
  -H "Content-Type: application/json" \
  -d '{"name":"Работа","description":"Рабочие заметки"}'
```

## Локальный запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Onyoro/Nikolaeva_SV.git
cd Nikolaeva_SV
```

### 2. Создать и активировать виртуальное окружение

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить переменные окружения

Скопируйте `.env.example` в `.env` и заполните своими данными:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/notes_db
```

### 5. Запустить приложение

```bash
flask run
```

Откройте в браузере: http://127.0.0.1:5000

## Запуск через Docker

Убедитесь, что установлен Docker Desktop, и он запущен.

```bash
docker-compose up --build
```

Приложение будет доступно на http://127.0.0.1:5000

Остановить:

```bash
docker-compose down
```

## Запуск тестов

```bash
pytest -v
```

Все 12 тестов должны пройти успешно. Тесты используют отдельную базу данных SQLite в памяти.

## Скрипт-обработчик логов

Мини-проект из блока 1 практики. Демонстрирует оптимизацию вложенных циклов через словарь.

```bash
cd scripts
python log_processor.py
```

Скрипт:
1. Читает `sample.log`.
2. Парсит строки через регулярные выражения.
3. Считает статистику по уровням (INFO, ERROR, WARNING) двумя способами — медленным (вложенные циклы) и быстрым (один проход).
4. Сравнивает производительность и экспортирует результат в JSON.

## Деплой на Render

Проект развёрнут на хостинге Render.

**Параметры Web Service:**
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app.main:app`
- Environment Variable: `DATABASE_URL` — строка подключения к PostgreSQL

**Публичный URL:** https://notes-api-nikolaeva.onrender.com

## Использование

### Через браузер

Откройте https://notes-api-nikolaeva.onrender.com — интерактивная страница с формами создания заметок и категорий.

### Через Postman / curl

Используйте эндпоинты, описанные выше.

### Через Python

```python
import requests

response = requests.post(
    "https://notes-api-nikolaeva.onrender.com/api/notes",
    json={"title": "Заметка из Python", "content": "Текст"}
)
print(response.json())
```

## Автор

Николаева С.В., группа ИИПМИ-24, 2026