from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Invoice, InvoiceItem
from app.repositories.interfaces.invoices import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice], IRepository[Invoice]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Invoice)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[Invoice]:
        stmt = (
            select(self._model)
            .options(
                selectinload(Invoice.supplier),
                selectinload(Invoice.items).selectinload(InvoiceItem.ingredient),
            )
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())


class InvoiceItemRepository(BaseRepository[InvoiceItem], IRepository[InvoiceItem]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, InvoiceItem)