from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.invoices import InvoiceCreate, InvoiceItemCreate, InvoiceUpdate
from app.schemas.recipes import RecipeCreate, RecipeIngredientCreate, RecipeUpdate
from app.services.implementations.invoices import InvoiceService
from app.services.implementations.recipes import RecipeService


@pytest.mark.asyncio
async def test_recipe_create_and_update_persists_full_composition(
    db_session: AsyncSession,
) -> None:
    group_id = (
        await db_session.execute(
            text(
                "INSERT INTO product_groups (code, name) "
                "VALUES ('NESTED-GROUP', 'Nested group') RETURNING id"
            )
        )
    ).scalar_one()
    product_id = (
        await db_session.execute(
            text(
                "INSERT INTO products (name, group_id) "
                "VALUES ('Nested product', :group_id) RETURNING id"
            ),
            {"group_id": group_id},
        )
    ).scalar_one()
    author_id = (
        await db_session.execute(
            text(
                "INSERT INTO authors (code, surname, name, country, year) "
                "VALUES ('NESTED-AUTHOR', 'Tester', 'Recipe', 'BY', 2000) "
                "RETURNING id"
            )
        )
    ).scalar_one()
    ingredient_id = (
        await db_session.execute(
            text(
                "INSERT INTO ingredients (name, calories_per_gram) "
                "VALUES ('Nested ingredient', 2.5) RETURNING id"
            )
        )
    ).scalar_one()
    method_id = (
        await db_session.execute(
            text(
                "INSERT INTO preparation_methods (code, name) "
                "VALUES ('NESTED-METHOD', 'Mix') RETURNING id"
            )
        )
    ).scalar_one()
    await db_session.commit()

    service = RecipeService(db_session)
    created = await service.create(
        RecipeCreate(
            number="NESTED-RECIPE",
            name="Nested recipe",
            description="Initial description",
            product_id=product_id,
            author_id=author_id,
            ingredients=[
                RecipeIngredientCreate(
                    ingredient_id=ingredient_id,
                    preparation_method_id=method_id,
                    grams_per_kg=Decimal("250.000"),
                )
            ],
        )
    )

    assert len(created.ingredients) == 1
    assert created.ingredients[0].ingredient.name == "Nested ingredient"
    assert created.ingredients[0].preparation_method.name == "Mix"

    updated = await service.update(
        created.id,
        RecipeUpdate(
            description=None,
            ingredients=[
                RecipeIngredientCreate(
                    ingredient_id=ingredient_id,
                    preparation_method_id=method_id,
                    grams_per_kg=Decimal("500.000"),
                )
            ],
        ),
    )

    assert updated is not None
    assert updated.description is None
    assert updated.ingredients[0].grams_per_kg == Decimal("500.000")
    # SQLite in the unit-test fixture does not enable FK cascades, so remove
    # the child row explicitly before deleting the recipe test data.
    await db_session.execute(
        text("DELETE FROM recipe_ingredients WHERE recipe_id = :recipe_id"),
        {"recipe_id": created.id},
    )
    assert await service.delete(created.id) is True


@pytest.mark.asyncio
async def test_invoice_create_and_update_persists_items(
    db_session: AsyncSession,
) -> None:
    supplier_id = (
        await db_session.execute(
            text(
                "INSERT INTO suppliers (code, name) "
                "VALUES ('NESTED-SUPPLIER', 'Nested supplier') RETURNING id"
            )
        )
    ).scalar_one()
    ingredient_id = (
        await db_session.execute(
            text(
                "INSERT INTO ingredients (name, calories_per_gram) "
                "VALUES ('Invoice nested ingredient', 1.25) RETURNING id"
            )
        )
    ).scalar_one()
    await db_session.commit()

    service = InvoiceService(db_session)
    created = await service.create(
        InvoiceCreate(
            supplier_id=supplier_id,
            number="NESTED-INVOICE",
            invoice_date=date(2026, 10, 7),
            items=[
                InvoiceItemCreate(
                    ingredient_id=ingredient_id,
                    quantity=Decimal("10.000"),
                    unit_price=Decimal("3.5000"),
                )
            ],
        )
    )

    assert len(created.items) == 1
    assert created.items[0].ingredient.name == "Invoice nested ingredient"

    updated = await service.update(
        created.id,
        InvoiceUpdate(
            number=None,
            items=[
                InvoiceItemCreate(
                    ingredient_id=ingredient_id,
                    quantity=Decimal("20.000"),
                    unit_price=Decimal("4.2500"),
                )
            ],
        ),
    )

    assert updated is not None
    assert updated.number is None
    assert updated.items[0].quantity == Decimal("20.000")
    assert updated.items[0].unit_price == Decimal("4.2500")
