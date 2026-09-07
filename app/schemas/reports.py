from datetime import date
from decimal import Decimal

from pydantic import Field

from app.schemas.base import BaseSchema
from app.schemas.suppliers import SupplierRead


class PriceListItem(BaseSchema):
    ingredient_id: int
    ingredient_name: str
    unit_price: Decimal = Field(
        gt=0,
        max_digits=14,
        decimal_places=4,
    )
    invoice_number: str | None = None


class PriceListResponse(BaseSchema):
    price_date: date
    supplier: SupplierRead
    items: list[PriceListItem] = Field(default_factory=list)


class DishCalorieRead(BaseSchema):
    product_id: int
    product_name: str
    group_name: str | None = None
    recipe_id: int | None = None
    recipe_name: str | None = None
    calories_per_100g: Decimal = Field(
        ge=0,
        max_digits=16,
        decimal_places=3,
    )
    calories_per_1kg: Decimal = Field(
        ge=0,
        max_digits=18,
        decimal_places=3,
    )


class MinCalorieDishesResponse(BaseSchema):
    min_calories_per_100g: Decimal = Field(
        ge=0,
        max_digits=16,
        decimal_places=3,
    )
    items: list[DishCalorieRead] = Field(default_factory=list)


class DishRecipeRead(BaseSchema):
    recipe_id: int
    recipe_number: str
    recipe_name: str


class DishWithRecipes(BaseSchema):
    product_id: int
    product_name: str
    group_name: str | None = None
    recipes: list[DishRecipeRead] = Field(default_factory=list)
    