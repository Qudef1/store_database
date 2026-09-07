from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Invoice, InvoiceItem
from app.repositories.interfaces.invoices import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice], IRepository[Invoice]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Invoice)


class InvoiceItemRepository(BaseRepository[InvoiceItem], IRepository[InvoiceItem]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, InvoiceItem)