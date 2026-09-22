from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ingredient, Product
from app.repositories.sqlalchemy.ingredients import IngredientRepository
from app.repositories.sqlalchemy.invoices import InvoiceRepository
from app.repositories.sqlalchemy.products import ProductRepository
from app.repositories.sqlalchemy.recipes import RecipeRepository
from app.services.implementations.reports import (
    MinCalorieProductsService,
    ProductRecipesService,
    SupplierPriceListService,
)


@pytest.mark.asyncio
async def test_parameterized_crud_handles_frontend_values(db_session: AsyncSession):
    await db_session.execute(
        text("INSERT INTO product_groups (code, name) VALUES (:code, :name)"),
        {"code": "RAW-SQL-GROUP", "name": "Raw SQL group"},
    )
    group_id = (
        await db_session.execute(
            text("SELECT id FROM product_groups WHERE code = :code"),
            {"code": "RAW-SQL-GROUP"},
        )
    ).scalar_one()

    repository = ProductRepository(db_session)
    frontend_value = "Cake'); DROP TABLE products; --"
    created = await repository.create(Product(name=frontend_value, group_id=group_id))

    assert created.id is not None
    assert (await repository.get(created.id)).name == frontend_value

    created.name = "Updated safely"
    updated = await repository.update(created.id, created)
    assert updated is not None
    assert updated.name == "Updated safely"
    assert any(item.id == created.id for item in await repository.list())

    assert await repository.delete(created.id) is True
    assert await repository.delete(created.id) is False


@pytest.mark.asyncio
async def test_decimal_crud_and_all_report_queries(db_session: AsyncSession):
    ingredient_repository = IngredientRepository(db_session)
    ingredient = await ingredient_repository.create(
        Ingredient(name="Raw SQL ingredient", calories_per_gram=Decimal("2.5000"))
    )
    assert Decimal(str(ingredient.calories_per_gram)) == Decimal("2.5000")

    seed_statements = [
        (
            "INSERT INTO product_groups (code, name) VALUES (:code, :name)",
            {"code": "REPORT-GROUP", "name": "Report group"},
        ),
        (
            (
                "INSERT INTO authors (code, surname, name, country, year) "
                "VALUES (:code, :surname, :name, :country, :year)"
            ),
            {
                "code": "REPORT-AUTHOR",
                "surname": "Tester",
                "name": "Raw",
                "country": "BY",
                "year": 2000,
            },
        ),
        (
            (
                "INSERT INTO suppliers (code, name, address, phone) "
                "VALUES (:code, :name, :address, :phone)"
            ),
            {
                "code": "REPORT-SUPPLIER",
                "name": "Report supplier",
                "address": "Test address",
                "phone": "+375000000000",
            },
        ),
        (
            "INSERT INTO preparation_methods (code, name) VALUES (:code, :name)",
            {"code": "REPORT-METHOD", "name": "Mix"},
        ),
    ]
    for sql, params in seed_statements:
        await db_session.execute(text(sql), params)

    async def id_for(table: str, code: str) -> int:
        return (
            await db_session.execute(
                text(f"SELECT id FROM {table} WHERE code = :code"),
                {"code": code},
            )
        ).scalar_one()

    group_id = await id_for("product_groups", "REPORT-GROUP")
    author_id = await id_for("authors", "REPORT-AUTHOR")
    supplier_id = await id_for("suppliers", "REPORT-SUPPLIER")
    method_id = await id_for("preparation_methods", "REPORT-METHOD")

    product_id = (
        await db_session.execute(
            text(
                "INSERT INTO products (name, group_id) VALUES (:name, :group_id) "
                "RETURNING id"
            ),
            {"name": "Report product", "group_id": group_id},
        )
    ).scalar_one()
    recipe_id = (
        await db_session.execute(
            text(
                "INSERT INTO recipes (number, name, product_id, author_id) "
                "VALUES (:number, :name, :product_id, :author_id) RETURNING id"
            ),
            {
                "number": "REPORT-RECIPE",
                "name": "Report recipe",
                "product_id": product_id,
                "author_id": author_id,
            },
        )
    ).scalar_one()
    invoice_id = (
        await db_session.execute(
            text(
                "INSERT INTO invoices (supplier_id, number, invoice_date) "
                "VALUES (:supplier_id, :number, :invoice_date) RETURNING id"
            ),
            {
                "supplier_id": supplier_id,
                "number": "REPORT-INVOICE",
                "invoice_date": "2026-09-22",
            },
        )
    ).scalar_one()
    await db_session.execute(
        text(
            "INSERT INTO recipe_ingredients "
            "(recipe_id, ingredient_id, preparation_method_id, grams_per_kg) "
            "VALUES (:recipe_id, :ingredient_id, :method_id, :grams)"
        ),
        {
            "recipe_id": recipe_id,
            "ingredient_id": ingredient.id,
            "method_id": method_id,
            "grams": 1000,
        },
    )
    await db_session.execute(
        text(
            "INSERT INTO invoice_items "
            "(invoice_id, ingredient_id, quantity, unit_price) "
            "VALUES (:invoice_id, :ingredient_id, :quantity, :unit_price)"
        ),
        {
            "invoice_id": invoice_id,
            "ingredient_id": ingredient.id,
            "quantity": 10,
            "unit_price": 12.5,
        },
    )
    await db_session.commit()

    price_list = await SupplierPriceListService(db_session).get_price_list(
        supplier_id, date(2026, 9, 22)
    )
    assert price_list.supplier.id == supplier_id
    assert price_list.items[0].ingredient_id == ingredient.id

    calories = await MinCalorieProductsService(db_session).get_min_calorie_dishes()
    assert calories.min_calories_per_100g == Decimal(250)
    assert calories.items[0].calories_per_1kg == Decimal(2500)

    products = await ProductRecipesService(db_session).get_products_with_recipes()
    report_product = next(item for item in products if item.product_id == product_id)
    assert report_product.recipes[0].recipe_id == recipe_id

    recipe = await RecipeRepository(db_session).get(recipe_id)
    assert recipe is not None
    assert recipe.author.id == author_id
    assert recipe.ingredients[0].ingredient.id == ingredient.id
    assert recipe.ingredients[0].preparation_method.id == method_id

    invoice = await InvoiceRepository(db_session).get(invoice_id)
    assert invoice is not None
    assert invoice.supplier.id == supplier_id
    assert invoice.items[0].ingredient.id == ingredient.id
