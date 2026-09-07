from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.repositories.interfaces.products import IRepository as IProductRepository
from app.repositories.sqlalchemy.products import ProductRepository
from app.schemas.products import ProductCreate, ProductRead, ProductUpdate


class ProductService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ProductRepository(session)

    async def get(self, id: int) -> ProductRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return ProductRead.model_validate(obj)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[ProductRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [ProductRead.model_validate(o) for o in objs]

    async def create(self, schema: ProductCreate) -> ProductRead:
        obj = Product(
            name=schema.name,
            group_id=schema.group_id,
        )
        await self._repo.create(obj)
        return ProductRead.model_validate(obj)

    async def update(self, id: int, schema: ProductUpdate) -> ProductRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.name is not None:
            existing.name = schema.name
        if schema.group_id is not None:
            existing.group_id = schema.group_id
        await self._repo.update(id, existing)
        return ProductRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)