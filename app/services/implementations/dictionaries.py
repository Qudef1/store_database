from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PreparationMethod, ProductGroup
from app.repositories.sqlalchemy.dictionaries import (
    PreparationMethodRepository,
    ProductGroupRepository,
)
from app.schemas.dictionaries import (
    PreparationMethodCreate,
    PreparationMethodRead,
    PreparationMethodUpdate,
    ProductGroupCreate,
    ProductGroupRead,
    ProductGroupUpdate,
)


class ProductGroupService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ProductGroupRepository(session)

    async def get(self, id: int) -> ProductGroupRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return ProductGroupRead.model_validate(obj)

    async def list(
        self, *, offset: int = 0, limit: int = 100
    ) -> list[ProductGroupRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [ProductGroupRead.model_validate(o) for o in objs]

    async def create(self, schema: ProductGroupCreate) -> ProductGroupRead:
        obj = ProductGroup(
            code=schema.code,
            name=schema.name,
        )
        obj = await self._repo.create(obj)
        return ProductGroupRead.model_validate(obj)

    async def update(
        self, id: int, schema: ProductGroupUpdate
    ) -> ProductGroupRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.code is not None:
            existing.code = schema.code
        if schema.name is not None:
            existing.name = schema.name
        existing = await self._repo.update(id, existing)
        assert existing is not None
        return ProductGroupRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)


class PreparationMethodService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = PreparationMethodRepository(session)

    async def get(self, id: int) -> PreparationMethodRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return PreparationMethodRead.model_validate(obj)

    async def list(
        self, *, offset: int = 0, limit: int = 100
    ) -> list[PreparationMethodRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [PreparationMethodRead.model_validate(o) for o in objs]

    async def create(self, schema: PreparationMethodCreate) -> PreparationMethodRead:
        obj = PreparationMethod(
            code=schema.code,
            name=schema.name,
        )
        obj = await self._repo.create(obj)
        return PreparationMethodRead.model_validate(obj)

    async def update(
        self, id: int, schema: PreparationMethodUpdate
    ) -> PreparationMethodRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.code is not None:
            existing.code = schema.code
        if schema.name is not None:
            existing.name = schema.name
        existing = await self._repo.update(id, existing)
        assert existing is not None
        return PreparationMethodRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)
