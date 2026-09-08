from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ingredient, Invoice, InvoiceItem, Recipe, RecipeIngredient, Supplier  # noqa: F401
from app.schemas.reports import (
    DishCalorieRead,
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
        from app.models import Product, ProductGroup

        stmt = (
            select(Recipe, Product, ProductGroup, Ingredient, RecipeIngredient)
            .join(Product, Recipe.product_id == Product.id)
            .join(ProductGroup, Product.group_id == ProductGroup.id)
            .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
            .join(Ingredient, RecipeIngredient.ingredient_id == Ingredient.id)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        from collections import defaultdict

        recipe_calories: dict[int, Decimal] = defaultdict(Decimal)
        recipe_product_map: dict[int, tuple[int, str, str, int, str]] = {}

        for recipe, product, group, ingredient, recipe_ingredient in rows:
            calories = ingredient.calories_per_gram * recipe_ingredient.grams_per_kg
            recipe_calories[recipe.id] += calories
            recipe_product_map[recipe.id] = (product.id, product.name, group.name, recipe.id, recipe.name)

        if not recipe_calories:
            return MinCalorieDishesResponse(min_calories_per_100g=Decimal("0"), items=[])

        min_cal = min(recipe_calories.values())
        items = []
        for recipe_id, cal in recipe_calories.items():
            if cal == min_cal:
                product_id, product_name, group_name, rec_id, rec_name = recipe_product_map[recipe_id]
                items.append(
                    DishCalorieRead(
                        product_id=product_id,
                        product_name=product_name,
                        group_name=group_name,
                        recipe_id=rec_id,
                        recipe_name=rec_name,
                        calories_per_100g=cal / 10,
                        calories_per_1kg=cal,
                    )
                )
        return MinCalorieDishesResponse(min_calories_per_100g=min_cal / 10, items=items)


class ProductRecipesService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_products_with_recipes(self) -> list[DishWithRecipes]:
        from app.models import Product, ProductGroup, Recipe
        from app.schemas.reports import DishRecipeRead

        stmt = (
            select(Recipe, Product, ProductGroup)
            .join(Product, Recipe.product_id == Product.id)
            .join(ProductGroup, Product.group_id == ProductGroup.id)
            .order_by(Recipe.product_id)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        products_map: dict[int, DishWithRecipes] = {}
        for recipe, product, group in rows:
            if recipe.product_id not in products_map:
                products_map[recipe.product_id] = DishWithRecipes(
                    product_id=product.id,
                    product_name=product.name,
                    group_name=group.name,
                    recipes=[],
                )
            products_map[recipe.product_id].recipes.append(
                DishRecipeRead(
                    recipe_id=recipe.id,
                    recipe_number=recipe.number,
                    recipe_name=recipe.name,
                )
            )
        return list(products_map.values())
