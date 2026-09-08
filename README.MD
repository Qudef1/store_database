# Банк данных технологий создания продуктов

Приложение для учета продуктов питания, рецептов, ингредиентов, поставщиков и накладных.  
Построено на **FastAPI + SQLAlchemy 2.0 (async) + Pydantic 2 + PostgreSQL**.

---

## Технологии

- **Python** 3.11+
- **PostgreSQL** 15+
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** 2.0 (async) — ORM
- **Pydantic** 2 — валидация схем
- **Alembic** — миграции БД
- **pytest** + **pytest-asyncio** — тестирование

---

## Структура проекта

```
lab2/
├── app/
│   ├── config.py                 # pydantic-settings: конфигурация
│   ├── main.py                   # Точка входа FastAPI
│   │
│   ├── models/                   # ORM-модели SQLAlchemy
│   │   ├── base.py
│   │   ├── authors.py
│   │   ├── dictionaries.py       # product_groups, preparation_methods
│   │   ├── ingredients.py
│   │   ├── invoices.py           # invoices + invoice_items
│   │   ├── products.py
│   │   ├── recipes.py            # recipes + recipe_ingredients
│   │   └── suppliers.py
│   │
│   ├── schemas/                  # Pydantic-схемы
│   │   ├── base.py
│   │   ├── authors.py
│   │   ├── dictionaries.py
│   │   ├── ingredients.py
│   │   ├── invoices.py
│   │   ├── products.py
│   │   ├── recipes.py
│   │   ├── reports.py            # Схемы отчётов
│   │   └── queries.py            # Параметры пагинации/фильтров
│   │
│   ├── repositories/             # Infrastructure: доступ к данным
│   │   ├── interfaces/           # Абстракции (IRepository)
│   │   └── sqlalchemy/           # Реализации на SQLAlchemy
│   │
│   ├── services/                 # Application: бизнес-логика
│   │   ├── interfaces/           # Сервисные контракты
│   │   └── implementations/      # Реализации CRUD + отчёты
│   │
│   ├── db/                       # Сессия БД и DI
│   │   ├── session.py
│   │   └── repositories.py
│   │
│   └── api/
│       └── v1/
│           ├── router.py         # Версионирование API
│           └── endpoints/        # Контроллеры FastAPI
│               ├── products.py
│               ├── recipes.py
│               ├── suppliers.py
│               ├── reports.py
│               └── ...
│
├── sql/
│   ├── 01_schema.sql             # DDL PostgreSQL
│   └── 02_seed.sql               # Тестовые данные
│
├── tests/
│   ├── conftest.py               # Фикстуры pytest
│   ├── unit/                     # Unit-тесты сервисов
│   └── integration/              # Интеграционные тесты API
│
├── docker-compose.yml            # PostgreSQL в Docker
├── .env                          # Локальные переменные окружения
├── .env.example
├── requirements.txt
├── Plan.md
└── README.md
```

---

## Быстрый старт (рекомендуется)

### 1. Запустите PostgreSQL в Docker

```bash
docker compose up -d
```

Проверьте статус:

```bash
docker compose ps
```

Контейнер `lab2-postgres` автоматически:
- создаст БД `food_products`
- применит `sql/01_schema.sql` и `sql/02_seed.sql`

### 2. Установите зависимости

```bash
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Настройте переменные окружения

Файл `.env` в корне проекта:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_products
DB_USER=postgres
DB_PASSWORD=postgres
DEBUG=true
```

### 4. Запустите приложение

```bash
uvicorn app.main:app --reload
```

После запуска:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **API**: http://127.0.0.1:8000/api/v1

---

## Альтернатива: локальный PostgreSQL без Docker

Если вы не используете Docker, выполните:

### 1. Установите PostgreSQL 15+

### 2. Создайте базу данных

```bash
psql -U postgres -c "CREATE DATABASE food_products;"
```

### 3. Примените схему БД

```bash
psql -U postgres -d food_products -f sql/01_schema.sql
psql -U postgres -d food_products -f sql/02_seed.sql
```

Или через Alembic:

```bash
alembic -c alembic.ini upgrade head
```

### 4. Установите зависимости и запустите

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\Activate.ps1  # Windows PowerShell

pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **API**: http://127.0.0.1:8000/api/v1

---

## Основные endpoints

### Продукты
| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/products/` | Создать продукт |
| `GET` | `/api/v1/products/` | Список продуктов |
| `GET` | `/api/v1/products/{id}` | Продукт по ID |
| `PUT` | `/api/v1/products/{id}` | Обновить продукт |
| `DELETE` | `/api/v1/products/{id}` | Удалить продукт |

### Рецепты
| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/recipes/` | Создать рецепт |
| `GET` | `/api/v1/recipes/` | Список рецептов |
| `GET` | `/api/v1/recipes/{id}` | Рецепт по ID |
| `PUT` | `/api/v1/recipes/{id}` | Обновить рецепт |
| `DELETE` | `/api/v1/recipes/{id}` | Удалить рецепт |

### Поставщики
| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/suppliers/` | Создать поставщика |
| `GET` | `/api/v1/suppliers/` | Список поставщиков |
| `GET` | `/api/v1/suppliers/{id}` | Поставщик по ID |
| `PUT` | `/api/v1/suppliers/{id}` | Обновить поставщика |
| `DELETE` | `/api/v1/suppliers/{id}` | Удалить поставщика |

### Отчеты
| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/api/v1/reports/supplier-price-list` | Прайс-лист поставщика на дату |
| `GET` | `/api/v1/reports/min-calorie-products` | Блюда с минимальной калорийностью |
| `GET` | `/api/v1/reports/products-with-recipes` | Блюда и названия рецептов |

---

## Управление PostgreSQL (Docker)

```bash
# Запуск
docker compose up -d

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down

# Полное удаление контейнера и volumes (данные будут потеряны)
docker compose down -v
```

---

## Запуск тестов

### Unit-тесты

```bash
pytest tests/unit -v
```

### Интеграционные тесты

```bash
pytest tests/integration -v
```

### Все тесты

```bash
pytest -v
```

### С покрытием

```bash
pytest --cov=app --cov=tests -v
```

---

## Переменные окружения

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `DB_HOST` | `localhost` | Хост PostgreSQL |
| `DB_PORT` | `5432` | Порт PostgreSQL |
| `DB_NAME` | `food_products` | Имя базы данных |
| `DB_USER` | `postgres` | Пользователь БД |
| `DB_PASSWORD` | `postgres` | Пароль БД |
| `DEBUG` | `false` | Режим отладки |

---

## Миграции Alembic

```bash
# Создать миграцию
alembic -c alembic.ini revision --autogenerate -m "message"

# Применить миграции
alembic -c alembic.ini upgrade head

# Откатить последнюю миграцию
alembic -c alembic.ini downgrade -1
```

---

## Лицензия

Учебный проект.