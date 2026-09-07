from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base
from app.repositories.interfaces.base import IRepository

T = TypeVar("T", bound=Base)


class BaseRepository(IRepository[T], Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self._session = session
        self._model = model

    async def get(self, id: int) -> T | None:
        return await self._session.get(self._model, id)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[T]:
        stmt = select(self._model).offset(offset).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj: T) -> T:
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update(self, id: int, obj: T) -> T | None:
        existing = await self.get(id)
        if existing is None:
            return None
        for key, value in vars(obj).items():
            if key != "_sa_instance_state":
                setattr(existing, key, value)
        await self._session.flush()
        await self._session.refresh(existing)
        return existing

    async def delete(self, id: int) -> bool:
        existing = await self.get(id)
        if existing is None:
            return False
        await self._session.delete(existing)
        await self._session.flush()
        return True