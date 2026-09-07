from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Author
from app.repositories.interfaces.authors import IRepository as IAuthorRepository
from app.repositories.sqlalchemy.authors import AuthorRepository
from app.schemas.authors import AuthorCreate, AuthorRead, AuthorUpdate


class AuthorService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = AuthorRepository(session)

    async def get(self, id: int) -> AuthorRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return AuthorRead.model_validate(obj)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[AuthorRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [AuthorRead.model_validate(o) for o in objs]

    async def create(self, schema: AuthorCreate) -> AuthorRead:
        obj = Author(
            code=schema.code,
            surname=schema.surname,
            name=schema.name,
            country=schema.country,
            year=schema.year,
        )
        await self._repo.create(obj)
        return AuthorRead.model_validate(obj)

    async def update(self, id: int, schema: AuthorUpdate) -> AuthorRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.code is not None:
            existing.code = schema.code
        if schema.surname is not None:
            existing.surname = schema.surname
        if schema.name is not None:
            existing.name = schema.name
        if schema.country is not None:
            existing.country = schema.country
        if schema.year is not None:
            existing.year = schema.year
        await self._repo.update(id, existing)
        return AuthorRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)