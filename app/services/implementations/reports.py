from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import Date, bindparam, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.reports import (
    DishCalorieRead,
    DishWithRecipes,
    MinCalorieDishesResponse,
    PriceListItem,
    PriceListResponse,
)
from app.schemas.suppliers import SupplierRead


class SupplierPriceListService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_price_list(
        self, supplier_id: int, price_date: date
    ) -> PriceListResponse:
        supplier_sql = text(
            """
            SELECT id, code, name, address, phone
            FROM suppliers
            WHERE id = :supplier_id
            """
        )
        supplier_row = (
            (await self._session.execute(supplier_sql, {"supplier_id": supplier_id}))
            .mappings()
            .one_or_none()
        )
        if supplier_row is None:
            raise HTTPException(status_code=404, detail="Supplier not found")

        items_sql = text(
            """
            SELECT
                ing.id AS ingredient_id,
                ing.name AS ingredient_name,
                ii.unit_price,
                inv.number AS invoice_number
            FROM invoices AS inv
            JOIN invoice_items AS ii ON ii.invoice_id = inv.id
            JOIN ingredients AS ing ON ing.id = ii.ingredient_id
            WHERE inv.supplier_id = :supplier_id
              AND inv.invoice_date = :price_date
            ORDER BY ing.id, inv.id
            """
        ).bindparams(bindparam("price_date", type_=Date()))
        rows = (
            await self._session.execute(
                items_sql,
                {"supplier_id": supplier_id, "price_date": price_date},
            )
        ).mappings()

        items = [PriceListItem.model_validate(row) for row in rows]
        return PriceListResponse(
            price_date=price_date,
            supplier=SupplierRead.model_validate(supplier_row),
            items=items,
        )


class MinCalorieProductsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_min_calorie_dishes(self) -> MinCalorieDishesResponse:
        sql = text(
            """
            WITH recipe_calories AS (
                SELECT
                    p.id AS product_id,
                    p.name AS product_name,
                    pg.name AS group_name,
                    r.id AS recipe_id,
                    r.name AS recipe_name,
                    SUM(ing.calories_per_gram * ri.grams_per_kg) AS calories_per_1kg
                FROM recipes AS r
                JOIN products AS p ON p.id = r.product_id
                JOIN product_groups AS pg ON pg.id = p.group_id
                JOIN recipe_ingredients AS ri ON ri.recipe_id = r.id
                JOIN ingredients AS ing ON ing.id = ri.ingredient_id
                GROUP BY p.id, p.name, pg.name, r.id, r.name
            )
            SELECT
                product_id,
                product_name,
                group_name,
                recipe_id,
                recipe_name,
                calories_per_1kg
            FROM recipe_calories
            WHERE calories_per_1kg = (SELECT MIN(calories_per_1kg) FROM recipe_calories)
            ORDER BY recipe_id
            """
        )
        rows = (await self._session.execute(sql)).mappings().all()
        if not rows:
            return MinCalorieDishesResponse(min_calories_per_100g=Decimal(0), items=[])

        items = []
        for row in rows:
            calories_per_1kg = Decimal(str(row["calories_per_1kg"]))
            items.append(
                DishCalorieRead(
                    **{key: row[key] for key in row if key != "calories_per_1kg"},
                    calories_per_100g=calories_per_1kg / 10,
                    calories_per_1kg=calories_per_1kg,
                )
            )
        return MinCalorieDishesResponse(
            min_calories_per_100g=items[0].calories_per_100g,
            items=items,
        )


class ProductRecipesService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_products_with_recipes(self) -> list[DishWithRecipes]:
        from app.schemas.reports import DishRecipeRead

        sql = text(
            """
            SELECT
                p.id AS product_id,
                p.name AS product_name,
                pg.name AS group_name,
                r.id AS recipe_id,
                r.number AS recipe_number,
                r.name AS recipe_name
            FROM recipes AS r
            JOIN products AS p ON p.id = r.product_id
            JOIN product_groups AS pg ON pg.id = p.group_id
            ORDER BY p.id, r.id
            """
        )
        rows = (await self._session.execute(sql)).mappings()

        products_map: dict[int, DishWithRecipes] = {}
        for row in rows:
            product_id = row["product_id"]
            if product_id not in products_map:
                products_map[product_id] = DishWithRecipes(
                    product_id=product_id,
                    product_name=row["product_name"],
                    group_name=row["group_name"],
                    recipes=[],
                )
            products_map[product_id].recipes.append(
                DishRecipeRead(
                    recipe_id=row["recipe_id"],
                    recipe_number=row["recipe_number"],
                    recipe_name=row["recipe_name"],
                )
            )
        return list(products_map.values())
