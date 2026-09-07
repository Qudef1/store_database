from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Author
from app.repositories.interfaces.authors import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class AuthorRepository(BaseRepository[Author], IRepository[Author]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Author)