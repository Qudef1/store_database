from __future__ import annotations

from typing import Generic, TypeVar

from app.models import Base
from app.repositories.interfaces.base import IRepository
from app.schemas.base import BaseSchema

T = TypeVar("T", bound=Base)
C = TypeVar("C", bound=BaseSchema)
U = TypeVar("U", bound=BaseSchema)
R = TypeVar("R", bound=BaseSchema)


class BaseCrudService(Generic[T, C, U, R]):
    def __init__(self, repository: IRepository[T], create_schema: type[C], update_schema: type[U], read_schema: type[R]) -> None:
        self._repo = repository
        self._create_schema = create_schema
        self._update_schema = update_schema
        self._read_schema = read_schema

    async def get(self, id: int) -> R | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return self._read_schema.model_validate(obj)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[R]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [self._read_schema.model_validate(o) for o in objs]

    async def create(self, schema: C) -> R:
        obj = await self._repo.create(self._create_schema_to_model(schema))
        return self._read_schema.model_validate(obj)

    async def update(self, id: int, schema: U) -> R | None:
        obj = await self._repo.update(id, self._update_schema_to_model(schema))
        if obj is None:
            return None
        return self._read_schema.model_validate(obj)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)

    def _create_schema_to_model(self, schema: C) -> T:
        raise NotImplementedError

    def _update_schema_to_model(self, schema: U) -> T:
        raise NotImplementedError