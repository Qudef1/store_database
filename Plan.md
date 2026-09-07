# План выполнения проекта

Проект: «Банк данных технологий создания различных продуктов».  
Стек: Python 3.11+, PostgreSQL 15+, SQLAlchemy 2.0 (async), Pydantic 2, FastAPI.

---

## Текущий прогресс

| Компонент | Статус |
|---|---|
| Структура каталогов | ✅ Создана |
| `app/models/base.py` | ✅ Готов (`Base` с naming convention) |
| `app/schemas/base.py` | ✅ Готов (`BaseSchema`, `Page`, `IdResponse`) |
| `app/api/v1/router.py` | ⚠️ Пустой, есть только заглушка |
| `app/repositories/` | ✅ Опечатка исправлена, интерфейсы готовы |
| `app/services/` | ✅ CRUD-сервисы + отчетные сервисы готовы |
| SQL DDL + seed | ✅ Созданы `sql/01_schema.sql` и `sql/02_seed.sql` |
| ORM-модели (`app/models/*.py`) | ✅ Заполнены все 7 файлов |
| Pydantic-схемы (`app/schemas/*.py`) | ⚠️ Частично готовы (есть базовые, CRUD, reports, queries) |
| Alembic | ✅ `alembic.ini`, `env.py`, `script.py.mako` настроены |
| Тесты | ❌ Отсутствуют |

---

## Этап 1. Фундамент (БД + ORM) — ✅ Выполнен

- [x] **Переименовать** `app/repositiries` → `app/repositories` (исправить опечатку).
- [x] **Создать** `sql/01_schema.sql` — DDL PostgreSQL (9 таблиц, FK, CHECK, индексы).
- [x] **Создать** `sql/02_seed.sql` — тестовые данные.
- [x] **Реализовать** ORM-модели в `app/models/*.py`:
  - `authors.py`
  - `dictionaries.py` (product_group, preparation_method)
  - `ingredients.py`
  - `invoices.py` (supplier + ingredient_price)
  - `products.py`
  - `recipes.py`
  - `suppliers.py`
- [x] **Настроить** Alembic: `alembic.ini`, обновить `env.py`, создать первую миграцию.

---

## Этап 2. Pydantic-схемы (контракты API)

- [x] **Заполнить** `app/schemas/dictionaries.py` — `ProductGroup`, `PreparationMethod` (Base/Create/Update/Read).
- [x] **Заполнить** `app/schemas/ingredients.py` — `Ingredient` + `IngredientPrice`.
- [x] **Заполнить** `app/schemas/suppliers.py` — `Supplier`.
- [x] **Заполнить** `app/schemas/authors.py` — `Author`.
- [x] **Заполнить** `app/schemas/products.py` — `Product`.
- [x] **Заполнить** `app/schemas/recipes.py` — `Recipe`, `RecipeIngredient`.
- [x] **Заполнить** `app/schemas/reports.py` — 3 отчёта (прайс-лист, мин. калорийность, блюда+рецепты).
- [x] **Заполнить** `app/schemas/queries.py` — фильтры/пагинация.

---

## Этап 3. Репозитории (Infrastructure) — ✅ Выполнен

- [x] **Создать** интерфейсы в `app/repositories/interfaces/`:
  - `base.py` — `IRepository[T]` (CRUD)
  - `products.py`, `recipes.py`, `suppliers.py`, `ingredients.py`, `authors.py`, `dictionaries.py`, `invoices.py`
- [x] **Реализовать** репозитории в `app/repositories/sqlalchemy/`:
  - `base.py` — `BaseRepository[T]` с通用 CRUD через SQLAlchemy 2.0 async
  - По одному на сущность: `products.py`, `recipes.py`, `suppliers.py`, `ingredients.py`, `authors.py`, `dictionaries.py`, `invoices.py`
- [x] **Зарегистрировать** репозитории в `app/db/` (Dependency Injection через `Depends`):
  - `session.py` — `get_session()`, `async_session_maker`
  - `repositories.py` — `get_*_repository()` для каждой сущности

---

## Этап 4. Сервисы / Use-cases (Application) — ✅ Выполнен

- [x] **Создать** интерфейсы в `app/services/interfaces/`:
  - `base.py` — `ICrudService[T, C, U]`
  - `products.py`, `recipes.py`, `suppliers.py`, `ingredients.py`, `authors.py`, `dictionaries.py`, `invoices.py`
  - `reports.py` — `ISupplierPriceListService`, `IMinCalorieProductsService`, `IProductRecipesService`
- [x] **Реализовать** сервисы в `app/services/implementations/`:
  - CRUD-сервисы для продуктов, рецептов, поставщиков, ингредиентов, авторов, словарей, накладных
  - Отчетные сервисы (3 функции из задания)

---

## Этап 5. API (Presentation) — ✅ Выполнен

- [x] **Реализовать** endpoints в `app/api/v1/endpoints/`:
  - `products.py`, `recipes.py`, `suppliers.py` — CRUD
  - `reports.py` — 3 отчётных эндпоинта
  - `ingredients.py`, `authors.py`, `dictionaries.py`, `invoices.py` — CRUD
- [x] **Подключить** роутеры в `app/api/v1/router.py`.

---

## Этап 6. Конфигурация и запуск — ✅ Выполнен

- [x] **Создать** `app/config.py` (pydantic-settings: `DATABASE_URL`, режим отладки).
- [x] **Обновить** `requirements.txt`.
- [x] **Создать** `.env` и `.env.example`.
- [x] **Собрать** приложение в `app/main.py` (создать `FastAPI`, подключить роутеры).

---

## Этап 7. Тестирование — ✅ Выполнен

- [x] **Написать** unit-тесты для сервисов (моки репозиториев).
- [x] **Написать** интеграционные тесты API (`TestClient` + `pytest-asyncio`).

---

## Критические зависимости

```
Этап 1 (ORM) → Этап 2 (Схемы) → Этап 3 (Репозитории) → Этап 4 (Сервисы) → Этап 5 (API)
```

Следующий шаг: установить зависимости (`pip install -r requirements.txt`) и запустить `uvicorn app.main:app --reload`.
