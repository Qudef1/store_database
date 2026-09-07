from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Supplier
from app.repositories.interfaces.suppliers import IRepository as ISupplierRepository
from app.repositories.sqlalchemy.suppliers import SupplierRepository
from app.schemas.suppliers import SupplierCreate, SupplierRead, SupplierUpdate


class SupplierService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = SupplierRepository(session)

    async def get(self, id: int) -> SupplierRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return SupplierRead.model_validate(obj)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[SupplierRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [SupplierRead.model_validate(o) for o in objs]

    async def create(self, schema: SupplierCreate) -> SupplierRead:
        obj = Supplier(
            code=schema.code,
            name=schema.name,
            address=schema.address,
            phone=schema.phone,
        )
        await self._repo.create(obj)
        return SupplierRead.model_validate(obj)

    async def update(self, id: int, schema: SupplierUpdate) -> SupplierRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.code is not None:
            existing.code = schema.code
        if schema.name is not None:
            existing.name = schema.name
        if schema.address is not None:
            existing.address = schema.address
        if schema.phone is not None:
            existing.phone = schema.phone
        await self._repo.update(id, existing)
        return SupplierRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)