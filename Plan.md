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
| `app/repositiries/` | ⚠️ Опечатка в названии (`repositiries`), файлы пустые |
| `app/services/` | ⚠️ Только заглушки |
| SQL DDL + seed | ❌ Отсутствуют |
| ORM-модели (`app/models/*.py`) | ❌ Пустые |
| Pydantic-схемы (`app/schemas/*.py`) | ❌ Пустые |
| Alembic | ⚠️ `env.py` есть, но конфиг/миграции не настроены |
| Тесты | ❌ Отсутствуют |

---

## Этап 1. Фундамент (БД + ORM)

- [ ] **Переименовать** `app/repositiries` → `app/repositories` (исправить опечатку).
- [ ] **Создать** `sql/01_schema.sql` — DDL PostgreSQL (9 таблиц, FK, CHECK, индексы).
- [ ] **Создать** `sql/02_seed.sql` — тестовые данные.
- [ ] **Реализовать** ORM-модели в `app/models/*.py`:
  - `authors.py`
  - `dictionaries.py` (product_group, preparation_method)
  - `ingredients.py`
  - `invoices.py` (supplier + ingredient_price)
  - `products.py`
  - `recipes.py`
  - `suppliers.py`
- [ ] **Настроить** Alembic: `alembic.ini`, обновить `env.py`, создать первую миграцию.

---

## Этап 2. Pydantic-схемы (контракты API)

- [ ] **Заполнить** `app/schemas/dictionaries.py` — `ProductGroup`, `PreparationMethod` (Base/Create/Update/Read).
- [ ] **Заполнить** `app/schemas/ingredients.py` — `Ingredient` + `IngredientPrice`.
- [ ] **Заполнить** `app/schemas/suppliers.py` — `Supplier`.
- [ ] **Заполнить** `app/schemas/authors.py` — `Author`.
- [ ] **Заполнить** `app/schemas/products.py` — `Product`.
- [ ] **Заполнить** `app/schemas/recipes.py` — `Recipe`, `RecipeIngredient`.
- [ ] **Заполнить** `app/schemas/reports.py` — 3 отчёта (прайс-лист, мин. калорийность, блюда+рецепты).
- [ ] **Заполнить** `app/schemas/queries.py` — фильтры/пагинация.

---

## Этап 3. Репозитории (Infrastructure)

- [ ] **Создать** интерфейсы в `app/repositories/interfaces/`:
  - `base.py` — `IRepository[T]` (CRUD)
  - `products.py`, `recipes.py`, `suppliers.py` и т.д.
- [ ] **Реализовать** репозитории в `app/repositories/implementations/`:
  - По одному на сущность, используя `AsyncSession`.
- [ ] **Зарегистрировать** репозитории в `app/db/` (Dependency Injection через `Depends`).

---

## Этап 4. Сервисы / Use-cases (Application)

- [ ] **Создать** интерфейсы в `app/services/interfaces/`:
  - `ISupplierPriceListService`
  - `IMinCalorieProductsService`
  - `IProductRecipesService`
- [ ] **Реализовать** сервисы в `app/services/implementations/`:
  - CRUD-сервисы для продуктов, рецептов, поставщиков
  - Отчетные сервисы (3 функции из задания)

---

## Этап 5. API (Presentation)

- [ ] **Реализовать** endpoints в `app/api/v1/endpoints/`:
  - `products.py`, `recipes.py`, `suppliers.py` — CRUD
  - `reports.py` — 3 отчётных эндпоинта
- [ ] **Подключить** роутеры в `app/api/v1/router.py`.
- [ ] **Собрать** приложение в `app/main.py` (создать `FastAPI`, подключить роутеры).

---

## Этап 6. Конфигурация и запуск

- [ ] **Создать** `app/config.py` (pydantic-settings: `DATABASE_URL`, режим отладки).
- [ ] **Обновить** `requirements.txt`.
- [ ] **Создать** `.env` и `.env.example`.
- [ ] **Проверить** запуск: `uvicorn app.main:app --reload`.

---

## Этап 7. Тестирование

- [ ] **Написать** unit-тесты для сервисов (моки репозиториев).
- [ ] **Написать** интеграционные тесты API (`TestClient` + `pytest-asyncio`).

---

## Критические зависимости

```
Этап 1 (ORM) → Этап 2 (Схемы) → Этап 3 (Репозитории) → Этап 4 (Сервисы) → Этап 5 (API)
```

Следующий шаг: начать с **Этапа 1** (SQL DDL + ORM-модели).
