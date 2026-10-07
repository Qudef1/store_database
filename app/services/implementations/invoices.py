from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Invoice, InvoiceItem
from app.repositories.sqlalchemy.invoices import InvoiceRepository
from app.schemas.invoices import InvoiceCreate, InvoiceRead, InvoiceUpdate


class InvoiceService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = InvoiceRepository(session)

    async def get(self, id: int) -> InvoiceRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return InvoiceRead.model_validate(obj)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[InvoiceRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [InvoiceRead.model_validate(o) for o in objs]

    async def create(self, schema: InvoiceCreate) -> InvoiceRead:
        obj = Invoice(
            supplier_id=schema.supplier_id,
            number=schema.number,
            invoice_date=schema.invoice_date,
        )
        obj.items = [
            InvoiceItem(
                ingredient_id=item.ingredient_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in schema.items
        ]
        obj = await self._repo.create(obj)
        return InvoiceRead.model_validate(obj)

    async def update(self, id: int, schema: InvoiceUpdate) -> InvoiceRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.supplier_id is not None:
            existing.supplier_id = schema.supplier_id
        if "number" in schema.model_fields_set:
            existing.number = schema.number
        if schema.invoice_date is not None:
            existing.invoice_date = schema.invoice_date
        if schema.items is not None:
            existing.items = [
                InvoiceItem(
                    ingredient_id=item.ingredient_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in schema.items
            ]
        existing = await self._repo.update(id, existing)
        assert existing is not None
        return InvoiceRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)
