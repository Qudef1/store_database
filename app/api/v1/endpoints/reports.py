from datetime import date

from fastapi import APIRouter, Depends

from app.db.repositories import (
    get_min_calorie_products_service,
    get_product_recipes_service,
    get_supplier_price_list_service,
)
from app.schemas.reports import (
    DishWithRecipes,
    MinCalorieDishesResponse,
    PriceListResponse,
)

router = APIRouter()


@router.get("/supplier-price-list", response_model=PriceListResponse)
async def get_supplier_price_list(
    supplier_id: int,
    price_date: date,
    service = Depends(get_supplier_price_list_service),
) -> PriceListResponse:
    return await service.get_price_list(supplier_id, price_date)


@router.get("/min-calorie-products", response_model=MinCalorieDishesResponse)
async def get_min_calorie_products(
    service = Depends(get_min_calorie_products_service),
) -> MinCalorieDishesResponse:
    return await service.get_min_calorie_dishes()


@router.get("/products-with-recipes", response_model=list[DishWithRecipes])
async def get_products_with_recipes(
    service = Depends(get_product_recipes_service),
) -> list[DishWithRecipes]:
    return await service.get_products_with_recipes()