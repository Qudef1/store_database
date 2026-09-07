from datetime import date
from decimal import Decimal

from app.schemas.reports import (
    DishWithRecipes,
    MinCalorieDishesResponse,
    PriceListResponse,
)


class ISupplierPriceListService:
    async def get_price_list(
        self, supplier_id: int, price_date: date
    ) -> PriceListResponse:
        raise NotImplementedError


class IMinCalorieProductsService:
    async def get_min_calorie_dishes(self) -> MinCalorieDishesResponse:
        raise NotImplementedError


class IProductRecipesService:
    async def get_products_with_recipes(self) -> list[DishWithRecipes]:
        raise NotImplementedError