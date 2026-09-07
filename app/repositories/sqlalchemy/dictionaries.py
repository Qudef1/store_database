from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProductGroup, PreparationMethod
from app.repositories.interfaces.dictionaries import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class ProductGroupRepository(BaseRepository[ProductGroup], IRepository[ProductGroup]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProductGroup)


class PreparationMethodRepository(BaseRepository[PreparationMethod], IRepository[PreparationMethod]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PreparationMethod)