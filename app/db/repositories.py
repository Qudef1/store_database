from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.sqlalchemy.authors import AuthorRepository
from app.repositories.sqlalchemy.dictionaries import ProductGroupRepository, PreparationMethodRepository
from app.repositories.sqlalchemy.ingredients import IngredientRepository
from app.repositories.sqlalchemy.invoices import InvoiceItemRepository, InvoiceRepository
from app.repositories.sqlalchemy.products import ProductRepository
from app.repositories.sqlalchemy.recipes import RecipeRepository
from app.repositories.sqlalchemy.suppliers import SupplierRepository
from app.services.implementations.authors import AuthorService
from app.services.implementations.dictionaries import PreparationMethodService, ProductGroupService
from app.services.implementations.ingredients import IngredientService
from app.services.implementations.invoices import InvoiceService
from app.services.implementations.products import ProductService
from app.services.implementations.recipes import RecipeService
from app.services.implementations.reports import (
    MinCalorieProductsService,
    ProductRecipesService,
    SupplierPriceListService,
)
from app.services.implementations.suppliers import SupplierService


def get_product_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductRepository:
    return ProductRepository(session)


def get_recipe_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RecipeRepository:
    return RecipeRepository(session)


def get_supplier_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SupplierRepository:
    return SupplierRepository(session)


def get_ingredient_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IngredientRepository:
    return IngredientRepository(session)


def get_author_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthorRepository:
    return AuthorRepository(session)


def get_product_group_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductGroupRepository:
    return ProductGroupRepository(session)


def get_preparation_method_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PreparationMethodRepository:
    return PreparationMethodRepository(session)


def get_invoice_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> InvoiceRepository:
    return InvoiceRepository(session)


def get_invoice_item_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> InvoiceItemRepository:
    return InvoiceItemRepository(session)


# Service factories
def get_product_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductService:
    return ProductService(session)


def get_recipe_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RecipeService:
    return RecipeService(session)


def get_supplier_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SupplierService:
    return SupplierService(session)


def get_ingredient_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> IngredientService:
    return IngredientService(session)


def get_author_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthorService:
    return AuthorService(session)


def get_product_group_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductGroupService:
    return ProductGroupService(session)


def get_preparation_method_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PreparationMethodService:
    return PreparationMethodService(session)


def get_invoice_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> InvoiceService:
    return InvoiceService(session)


def get_supplier_price_list_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SupplierPriceListService:
    return SupplierPriceListService(session)


def get_min_calorie_products_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> MinCalorieProductsService:
    return MinCalorieProductsService(session)


def get_product_recipes_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductRecipesService:
    return ProductRecipesService(session)