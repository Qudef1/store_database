from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ingredient, Invoice, InvoiceItem, Supplier
from app.schemas.reports import (
    DishWithRecipes,
    MinCalorieDishesResponse,
    PriceListResponse,
    PriceListItem,
)
from app.schemas.recipes import RecipeRead, RecipeTitle
from app.schemas.suppliers import SupplierRead


class SupplierPriceListService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_price_list(self, supplier_id: int, price_date: date) -> PriceListResponse:
        stmt = (
            select(InvoiceItem, Ingredient, Invoice, Supplier)
            .join(Invoice, InvoiceItem.invoice_id == Invoice.id)
            .join(Ingredient, InvoiceItem.ingredient_id == Ingredient.id)
            .join(Supplier, Invoice.supplier_id == Supplier.id)
            .where(Invoice.supplier_id == supplier_id)
            .where(Invoice.invoice_date == price_date)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        supplier = None
        items = []
        for item, ingredient, invoice, sup in rows:
            if supplier is None:
                supplier = SupplierRead.model_validate(sup)
            items.append(
                PriceListItem(
                    ingredient_id=ingredient.id,
                    ingredient_name=ingredient.name,
                    unit_price=item.unit_price,
                    invoice_number=invoice.number,
                )
            )
        return PriceListResponse(price_date=price_date, supplier=supplier, items=items)


class MinCalorieProductsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_min_calorie_dishes(self) -> MinCalorieDishesResponse:
        stmt = (
            select(Recipe, Ingredient, RecipeIngredient)
            .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
            .join(Ingredient, RecipeIngredient.ingredient_id == Ingredient.id)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        from collections import defaultdict

        recipe_calories: dict[int, Decimal] = defaultdict(Decimal)
        recipe_ingredients: dict[int, list[tuple[str, Decimal]]] = defaultdict(list)
        recipe_names: dict[int, str] = {}

        for recipe, ingredient, recipe_ingredient in rows:
            calories = ingredient.calories_per_gram * recipe_ingredient.grams_per_kg
            recipe_calories[recipe.id] += calories
            recipe_ingredients[recipe.id].append((ingredient.name, calories))
            recipe_names[recipe.id] = recipe.name

        if not recipe_calories:
            return MinCalorieDishesResponse(min_calories_per_100g=Decimal("0"), items=[])

        min_cal = min(recipe_calories.values())
        items = []
        for recipe_id, cal in recipe_calories.items():
            if cal == min_cal:
                items.append(
                    MinCalorieDishesResponse(
                        min_calories_per_100g=min_cal / 10,
                        items=[
                            {
                                "recipe_id": recipe_id,
                                "recipe_name": recipe_names[recipe_id],
                                "calories_per_100g": cal / 10,
                            }
                        ],
                    )
                )
        return MinCalorieDishesResponse(min_calories_per_100g=min_cal / 10, items=items)


class ProductRecipesService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_products_with_recipes(self) -> list[DishWithRecipes]:
        from app.models import Recipe, RecipeIngredient
        from app.schemas.recipes import RecipeTitle

        stmt = select(Recipe).order_by(Recipe.product_id)
        result = await self._session.execute(stmt)
        recipes = result.scalars().all()

        products_map: dict[int, DishWithRecipes] = {}
        for recipe in recipes:
            if recipe.product_id not in products_map:
                products_map[recipe.product_id] = DishWithRecipes(
                    product_id=recipe.product_id,
                    product_name="",
                    group_name=None,
                    recipes=[],
                )
            products_map[recipe.product_id].recipes.append(
                RecipeTitle(id=recipe.id, number=recipe.number, name=recipe.name)
            )
        return list(products_map.values())