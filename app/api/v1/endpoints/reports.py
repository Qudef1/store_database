from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.reports import (
    DishWithRecipes,
    MinCalorieDishesResponse,
    PriceListResponse,
)
from app.services.implementations.reports import (
    MinCalorieProductsService,
    ProductRecipesService,
    SupplierPriceListService,
)

router = APIRouter()


@router.get("/supplier-price-list", response_model=PriceListResponse)
async def get_supplier_price_list(
    supplier_id: int,
    price_date: date,
    session: AsyncSession = Depends(get_session),
) -> PriceListResponse:
    service = SupplierPriceListService(session)
    return await service.get_price_list(supplier_id, price_date)


@router.get("/min-calorie-products", response_model=MinCalorieDishesResponse)
async def get_min_calorie_products(
    session: AsyncSession = Depends(get_session),
) -> MinCalorieDishesResponse:
    service = MinCalorieProductsService(session)
    return await service.get_min_calorie_dishes()


@router.get("/products-with-recipes", response_model=list[DishWithRecipes])
async def get_products_with_recipes(
    session: AsyncSession = Depends(get_session),
) -> list[DishWithRecipes]:
    service = ProductRecipesService(session)
    return await service.get_products_with_recipes()