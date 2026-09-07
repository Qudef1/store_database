from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Supplier
from app.repositories.interfaces.suppliers import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class SupplierRepository(BaseRepository[Supplier], IRepository[Supplier]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Supplier)