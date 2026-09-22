-- ============================================================================
-- Демонстрационные данные. Скрипт можно запускать повторно: дубликаты не
-- создаются, а все связи определяются по стабильным кодам и номерам.
-- ============================================================================

INSERT INTO product_groups (code, name) VALUES
    ('GR-BAKERY',  'Хлебобулочные изделия'),
    ('GR-CONFECT', 'Кондитерские изделия'),
    ('GR-DAIRY',   'Молочные изделия'),
    ('GR-DRINKS',  'Напитки'),
    ('GR-SAUCES',  'Соусы')
ON CONFLICT (code) DO NOTHING;

INSERT INTO ingredients (name, calories_per_gram) VALUES
    ('Мука пшеничная',   3.2700),
    ('Сахар',            3.8700),
    ('Масло сливочное',  7.1700),
    ('Яйцо куриное',     1.5700),
    ('Молоко',           0.4200),
    ('Какао-порошок',    3.6400),
    ('Соль',             0.0000),
    ('Дрожжи',           0.8500),
    ('Мука ржаная',      3.0500),
    ('Вода',             0.0000),
    ('Масло растительное', 8.9900),
    ('Овсяные хлопья',   3.6600),
    ('Мёд',              3.0400),
    ('Творог',           1.2100),
    ('Сливки',           3.4000),
    ('Ванильный сахар',  3.9400),
    ('Лимон',            0.2900),
    ('Ягоды',            0.5000),
    ('Томаты',           0.1800),
    ('Крахмал',          3.1300),
    ('Разрыхлитель',     0.5300),
    ('Уксус',            0.1800),
    ('Горчица',          1.6200)
ON CONFLICT (name) DO NOTHING;

INSERT INTO preparation_methods (code, name) VALUES
    ('PM-SIFT',  'Просеивание'),
    ('PM-SOFT',  'Размягчение'),
    ('PM-HEAT',  'Нагревание'),
    ('PM-MIX',   'Смешивание'),
    ('PM-MELT',  'Растапливание'),
    ('PM-WHIP',  'Взбивание'),
    ('PM-KNEAD', 'Замешивание'),
    ('PM-BAKE',  'Выпекание'),
    ('PM-COOL',  'Охлаждение'),
    ('PM-BOIL',  'Варка')
ON CONFLICT (code) DO NOTHING;

INSERT INTO suppliers (code, name, address, phone) VALUES
    ('SUP-001', 'ООО "Мельник"', 'г. Москва, ул. Зерновая, 12', '+7-495-111-22-33'),
    ('SUP-002', 'АО "Молочный дом"', 'г. Тула, ул. Молочная, 5', '+7-487-222-33-44'),
    ('SUP-003', 'ИП Иванов', 'г. Калуга, ул. Садовая, 7', '+7-484-333-44-55'),
    ('SUP-004', 'ООО "Фруктовый край"', 'г. Минск, ул. Полевая, 18', '+375-17-244-55-66'),
    ('SUP-005', 'ООО "АгроТомат"', 'г. Брест, ул. Урожайная, 4', '+375-162-33-44-55'),
    ('SUP-006', 'АО "Золотое зерно"', 'г. Витебск, пр-т Строителей, 21', '+375-212-55-66-77')
ON CONFLICT (code) DO NOTHING;

INSERT INTO authors (code, surname, name, country, year) VALUES
    ('AU-001', 'Покровский', 'Алексей', 'Россия', 1975),
    ('AU-002', 'Smith', 'John', 'Великобритания', 1968),
    ('AU-003', 'Дюпон', 'Пьер', 'Франция', 1980),
    ('AU-004', 'Ковалёва', 'Марина', 'Беларусь', 1987),
    ('AU-005', 'Росси', 'Лука', 'Италия', 1979),
    ('AU-006', 'Мюллер', 'Анна', 'Германия', 1990),
    ('AU-007', 'Сато', 'Харуки', 'Япония', 1984)
ON CONFLICT (code) DO NOTHING;

WITH product_data(name, group_code) AS (
    VALUES
        ('Белый хлеб', 'GR-BAKERY'),
        ('Шоколадный кекс', 'GR-CONFECT'),
        ('Творожное печенье', 'GR-DAIRY'),
        ('Ржаной хлеб', 'GR-BAKERY'),
        ('Французский багет', 'GR-BAKERY'),
        ('Овсяное печенье', 'GR-CONFECT'),
        ('Медовый торт', 'GR-CONFECT'),
        ('Натуральный йогурт', 'GR-DAIRY'),
        ('Ванильное мороженое', 'GR-DAIRY'),
        ('Домашний лимонад', 'GR-DRINKS'),
        ('Ягодный морс', 'GR-DRINKS'),
        ('Томатный соус', 'GR-SAUCES'),
        ('Домашний майонез', 'GR-SAUCES')
)
INSERT INTO products (name, group_id)
SELECT data.name, groups.id
FROM product_data AS data
JOIN product_groups AS groups ON groups.code = data.group_code
WHERE NOT EXISTS (
    SELECT 1
    FROM products AS existing
    WHERE existing.name = data.name AND existing.group_id = groups.id
);

WITH recipe_data(number, name, description, product_name, group_code, author_code) AS (
    VALUES
        ('R-001', 'Классический белый хлеб', 'Домашний рецепт пшеничного хлеба', 'Белый хлеб', 'GR-BAKERY', 'AU-001'),
        ('R-002', 'Шоколадный кекс на молоке', 'Нежный шоколадный кекс с какао', 'Шоколадный кекс', 'GR-CONFECT', 'AU-002'),
        ('R-003', 'Творожное печенье', 'Мягкое печенье с творогом', 'Творожное печенье', 'GR-DAIRY', 'AU-003'),
        ('R-004', 'Ржаной хлеб на закваске', 'Плотный ароматный хлеб из ржаной муки', 'Ржаной хлеб', 'GR-BAKERY', 'AU-004'),
        ('R-005', 'Французский багет', 'Багет с хрустящей корочкой', 'Французский багет', 'GR-BAKERY', 'AU-003'),
        ('R-006', 'Овсяное печенье с мёдом', 'Печенье из овсяных хлопьев с натуральным мёдом', 'Овсяное печенье', 'GR-CONFECT', 'AU-006'),
        ('R-007', 'Медовый торт', 'Многослойный торт с медовыми коржами', 'Медовый торт', 'GR-CONFECT', 'AU-004'),
        ('R-008', 'Йогурт классический', 'Натуральный йогурт из молока и сливок', 'Натуральный йогурт', 'GR-DAIRY', 'AU-007'),
        ('R-009', 'Мороженое ванильное', 'Сливочное мороженое с ванилью', 'Ванильное мороженое', 'GR-DAIRY', 'AU-005'),
        ('R-010', 'Лимонад цитрусовый', 'Освежающий напиток из лимонов', 'Домашний лимонад', 'GR-DRINKS', 'AU-004'),
        ('R-011', 'Морс ягодный', 'Напиток из свежих ягод', 'Ягодный морс', 'GR-DRINKS', 'AU-004'),
        ('R-012', 'Соус томатный пряный', 'Густой соус из спелых томатов', 'Томатный соус', 'GR-SAUCES', 'AU-005'),
        ('R-013', 'Майонез домашний', 'Классический соус на растительном масле', 'Домашний майонез', 'GR-SAUCES', 'AU-006'),
        ('R-014', 'Белый хлеб быстрый', 'Ускоренный вариант белого хлеба', 'Белый хлеб', 'GR-BAKERY', 'AU-006')
)
INSERT INTO recipes (number, name, description, product_id, author_id)
SELECT data.number, data.name, data.description, products.id, authors.id
FROM recipe_data AS data
JOIN product_groups AS groups ON groups.code = data.group_code
JOIN products ON products.name = data.product_name AND products.group_id = groups.id
JOIN authors ON authors.code = data.author_code
ON CONFLICT (number) DO NOTHING;

WITH component_data(recipe_number, ingredient_name, method_code, grams_per_kg) AS (
    VALUES
        ('R-001', 'Мука пшеничная', 'PM-SIFT', 800.000),
        ('R-001', 'Дрожжи', 'PM-MIX', 15.000),
        ('R-001', 'Соль', 'PM-MIX', 10.000),
        ('R-002', 'Мука пшеничная', 'PM-SIFT', 350.000),
        ('R-002', 'Сахар', 'PM-MIX', 250.000),
        ('R-002', 'Масло сливочное', 'PM-MELT', 200.000),
        ('R-002', 'Какао-порошок', 'PM-SIFT', 50.000),
        ('R-002', 'Молоко', 'PM-HEAT', 100.000),
        ('R-003', 'Мука пшеничная', 'PM-SIFT', 400.000),
        ('R-003', 'Масло сливочное', 'PM-SOFT', 200.000),
        ('R-003', 'Сахар', 'PM-WHIP', 150.000),
        ('R-003', 'Яйцо куриное', 'PM-MIX', 50.000),
        ('R-003', 'Творог', 'PM-MIX', 200.000),
        ('R-004', 'Мука ржаная', 'PM-SIFT', 650.000),
        ('R-004', 'Вода', 'PM-HEAT', 330.000),
        ('R-004', 'Дрожжи', 'PM-KNEAD', 10.000),
        ('R-004', 'Соль', 'PM-KNEAD', 10.000),
        ('R-005', 'Мука пшеничная', 'PM-SIFT', 700.000),
        ('R-005', 'Вода', 'PM-KNEAD', 280.000),
        ('R-005', 'Дрожжи', 'PM-KNEAD', 10.000),
        ('R-005', 'Соль', 'PM-KNEAD', 10.000),
        ('R-006', 'Овсяные хлопья', 'PM-MIX', 450.000),
        ('R-006', 'Мука пшеничная', 'PM-SIFT', 250.000),
        ('R-006', 'Мёд', 'PM-HEAT', 150.000),
        ('R-006', 'Масло сливочное', 'PM-SOFT', 100.000),
        ('R-006', 'Яйцо куриное', 'PM-WHIP', 50.000),
        ('R-007', 'Мука пшеничная', 'PM-SIFT', 400.000),
        ('R-007', 'Мёд', 'PM-HEAT', 200.000),
        ('R-007', 'Сахар', 'PM-MIX', 150.000),
        ('R-007', 'Масло сливочное', 'PM-MELT', 150.000),
        ('R-007', 'Яйцо куриное', 'PM-WHIP', 100.000),
        ('R-008', 'Молоко', 'PM-HEAT', 850.000),
        ('R-008', 'Сливки', 'PM-MIX', 150.000),
        ('R-009', 'Сливки', 'PM-WHIP', 600.000),
        ('R-009', 'Молоко', 'PM-HEAT', 250.000),
        ('R-009', 'Сахар', 'PM-MIX', 100.000),
        ('R-009', 'Ванильный сахар', 'PM-MIX', 50.000),
        ('R-010', 'Вода', 'PM-MIX', 850.000),
        ('R-010', 'Лимон', 'PM-MIX', 100.000),
        ('R-010', 'Сахар', 'PM-MIX', 50.000),
        ('R-011', 'Вода', 'PM-BOIL', 700.000),
        ('R-011', 'Ягоды', 'PM-BOIL', 250.000),
        ('R-011', 'Сахар', 'PM-MIX', 50.000),
        ('R-012', 'Томаты', 'PM-BOIL', 850.000),
        ('R-012', 'Масло растительное', 'PM-MIX', 80.000),
        ('R-012', 'Сахар', 'PM-MIX', 40.000),
        ('R-012', 'Соль', 'PM-MIX', 20.000),
        ('R-012', 'Крахмал', 'PM-MIX', 10.000),
        ('R-013', 'Масло растительное', 'PM-WHIP', 600.000),
        ('R-013', 'Яйцо куриное', 'PM-WHIP', 200.000),
        ('R-013', 'Горчица', 'PM-MIX', 100.000),
        ('R-013', 'Уксус', 'PM-MIX', 70.000),
        ('R-013', 'Сахар', 'PM-MIX', 20.000),
        ('R-013', 'Соль', 'PM-MIX', 10.000),
        ('R-014', 'Мука пшеничная', 'PM-SIFT', 750.000),
        ('R-014', 'Вода', 'PM-KNEAD', 220.000),
        ('R-014', 'Дрожжи', 'PM-KNEAD', 15.000),
        ('R-014', 'Соль', 'PM-KNEAD', 15.000)
)
INSERT INTO recipe_ingredients (
    recipe_id,
    ingredient_id,
    preparation_method_id,
    grams_per_kg
)
SELECT recipes.id, ingredients.id, methods.id, data.grams_per_kg
FROM component_data AS data
JOIN recipes ON recipes.number = data.recipe_number
JOIN ingredients ON ingredients.name = data.ingredient_name
JOIN preparation_methods AS methods ON methods.code = data.method_code
ON CONFLICT (recipe_id, ingredient_id, preparation_method_id) DO NOTHING;

WITH invoice_data(supplier_code, number, invoice_date) AS (
    VALUES
        ('SUP-001', 'INV-001', DATE '2026-01-15'),
        ('SUP-001', 'INV-002', DATE '2026-03-01'),
        ('SUP-002', 'INV-003', DATE '2026-02-01'),
        ('SUP-003', 'INV-004', DATE '2026-02-10'),
        ('SUP-004', 'INV-005', DATE '2026-04-05'),
        ('SUP-005', 'INV-006', DATE '2026-04-12'),
        ('SUP-006', 'INV-007', DATE '2026-05-03'),
        ('SUP-002', 'INV-008', DATE '2026-05-18'),
        ('SUP-004', 'INV-009', DATE '2026-06-07')
)
INSERT INTO invoices (supplier_id, number, invoice_date)
SELECT suppliers.id, data.number, data.invoice_date
FROM invoice_data AS data
JOIN suppliers ON suppliers.code = data.supplier_code
ON CONFLICT (supplier_id, number) DO NOTHING;

WITH item_data(supplier_code, invoice_number, ingredient_name, quantity, unit_price) AS (
    VALUES
        ('SUP-001', 'INV-001', 'Мука пшеничная', 1000.000, 65.0000),
        ('SUP-001', 'INV-001', 'Сахар', 500.000, 78.5000),
        ('SUP-001', 'INV-002', 'Мука пшеничная', 1200.000, 70.0000),
        ('SUP-001', 'INV-002', 'Сахар', 600.000, 80.0000),
        ('SUP-002', 'INV-003', 'Молоко', 800.000, 55.0000),
        ('SUP-002', 'INV-003', 'Масло сливочное', 200.000, 540.0000),
        ('SUP-003', 'INV-004', 'Яйцо куриное', 300.000, 9.5000),
        ('SUP-003', 'INV-004', 'Масло растительное', 250.000, 145.0000),
        ('SUP-004', 'INV-005', 'Лимон', 180.000, 120.0000),
        ('SUP-004', 'INV-005', 'Ягоды', 350.000, 260.0000),
        ('SUP-004', 'INV-005', 'Мёд', 100.000, 390.0000),
        ('SUP-005', 'INV-006', 'Томаты', 900.000, 95.0000),
        ('SUP-005', 'INV-006', 'Горчица', 120.000, 210.0000),
        ('SUP-005', 'INV-006', 'Уксус', 150.000, 68.0000),
        ('SUP-006', 'INV-007', 'Мука ржаная', 700.000, 72.0000),
        ('SUP-006', 'INV-007', 'Овсяные хлопья', 450.000, 110.0000),
        ('SUP-006', 'INV-007', 'Дрожжи', 80.000, 430.0000),
        ('SUP-002', 'INV-008', 'Сливки', 300.000, 310.0000),
        ('SUP-002', 'INV-008', 'Творог', 400.000, 240.0000),
        ('SUP-002', 'INV-008', 'Молоко', 1000.000, 58.0000),
        ('SUP-004', 'INV-009', 'Ванильный сахар', 90.000, 175.0000),
        ('SUP-004', 'INV-009', 'Крахмал', 200.000, 92.0000),
        ('SUP-004', 'INV-009', 'Разрыхлитель', 75.000, 185.0000)
)
INSERT INTO invoice_items (invoice_id, ingredient_id, quantity, unit_price)
SELECT invoices.id, ingredients.id, data.quantity, data.unit_price
FROM item_data AS data
JOIN suppliers ON suppliers.code = data.supplier_code
JOIN invoices
    ON invoices.supplier_id = suppliers.id
    AND invoices.number = data.invoice_number
JOIN ingredients ON ingredients.name = data.ingredient_name
ON CONFLICT (invoice_id, ingredient_id) DO NOTHING;
