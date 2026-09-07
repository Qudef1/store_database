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