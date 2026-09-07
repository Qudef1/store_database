from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Recipe
from app.repositories.interfaces.recipes import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class RecipeRepository(BaseRepository[Recipe], IRepository[Recipe]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Recipe)