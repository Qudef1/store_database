-- ============================================================================
-- Банк данных технологий создания различных продуктов
-- DDL PostgreSQL
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Справочники
-- ----------------------------------------------------------------------------

CREATE TABLE product_groups (
    id   SERIAL PRIMARY KEY,
    code VARCHAR(32)  NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE preparation_methods (
    id   SERIAL PRIMARY KEY,
    code VARCHAR(32)  NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE ingredients (
    id                 SERIAL PRIMARY KEY,
    name               VARCHAR(255) NOT NULL UNIQUE,
    calories_per_gram  NUMERIC(12, 4) NOT NULL,
    CONSTRAINT ck_ingredients_calories_per_gram_positive CHECK (calories_per_gram > 0)
);

CREATE TABLE suppliers (
    id      SERIAL PRIMARY KEY,
    code    VARCHAR(32)  NOT NULL UNIQUE,
    name    VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone   VARCHAR(32)
);

CREATE TABLE authors (
    id      SERIAL PRIMARY KEY,
    code    VARCHAR(32)  NOT NULL UNIQUE,
    surname VARCHAR(255) NOT NULL,
    name    VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    year    INTEGER NOT NULL
);

-- ----------------------------------------------------------------------------
-- Основные сущности
-- ----------------------------------------------------------------------------

CREATE TABLE products (
    id        SERIAL PRIMARY KEY,
    name      VARCHAR(255) NOT NULL,
    group_id  INTEGER NOT NULL REFERENCES product_groups(id) ON DELETE RESTRICT
);

CREATE INDEX ix_products_group_id ON products(group_id);

CREATE TABLE recipes (
    id          SERIAL PRIMARY KEY,
    number      VARCHAR(64)  NOT NULL UNIQUE,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    author_id   INTEGER NOT NULL REFERENCES authors(id) ON DELETE RESTRICT
);

CREATE INDEX ix_recipes_product_id ON recipes(product_id);
CREATE INDEX ix_recipes_author_id  ON recipes(author_id);

-- ----------------------------------------------------------------------------
-- Рецепт → ингредиенты (M:N)
-- ----------------------------------------------------------------------------

CREATE TABLE recipe_ingredients (
    id                    SERIAL PRIMARY KEY,
    recipe_id             INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id         INTEGER NOT NULL REFERENCES ingredients(id) ON DELETE RESTRICT,
    preparation_method_id INTEGER NOT NULL REFERENCES preparation_methods(id) ON DELETE RESTRICT,
    grams_per_kg          NUMERIC(12, 3) NOT NULL,
    CONSTRAINT uq_recipe_ingredients UNIQUE (recipe_id, ingredient_id, preparation_method_id)
);

CREATE INDEX ix_recipe_ingredients_recipe_id      ON recipe_ingredients(recipe_id);
CREATE INDEX ix_recipe_ingredients_ingredient_id  ON recipe_ingredients(ingredient_id);
CREATE INDEX ix_recipe_ingredients_preparation_id ON recipe_ingredients(preparation_method_id);

-- ----------------------------------------------------------------------------
-- Накладные и позиции
-- ----------------------------------------------------------------------------

CREATE TABLE invoices (
    id           SERIAL PRIMARY KEY,
    supplier_id  INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE RESTRICT,
    number       VARCHAR(64),
    invoice_date DATE NOT NULL,
    CONSTRAINT uq_invoices_supplier_id_number UNIQUE (supplier_id, number)
);

CREATE INDEX ix_invoices_supplier_id  ON invoices(supplier_id);
CREATE INDEX ix_invoices_invoice_date ON invoices(invoice_date);

CREATE TABLE invoice_items (
    id           SERIAL PRIMARY KEY,
    invoice_id   INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(id) ON DELETE RESTRICT,
    quantity     NUMERIC(14, 3) NOT NULL,
    unit_price   NUMERIC(14, 4) NOT NULL,
    CONSTRAINT uq_invoice_items_invoice_id_ingredient_id UNIQUE (invoice_id, ingredient_id),
    CONSTRAINT ck_invoice_items_quantity_positive   CHECK (quantity > 0),
    CONSTRAINT ck_invoice_items_unit_price_positive CHECK (unit_price > 0)
);

CREATE INDEX ix_invoice_items_invoice_id    ON invoice_items(invoice_id);
CREATE INDEX ix_invoice_items_ingredient_id ON invoice_items(ingredient_id);