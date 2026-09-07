from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.repositories.interfaces.products import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class ProductRepository(BaseRepository[Product], IRepository[Product]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Product)