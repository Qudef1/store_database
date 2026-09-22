from __future__ import annotations

from sqlalchemy import Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ingredient
from app.repositories.interfaces.ingredients import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class IngredientRepository(BaseRepository[Ingredient], IRepository[Ingredient]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
            Ingredient,
            "ingredients",
            ("name", "calories_per_gram"),
            {"calories_per_gram": Numeric(12, 4)},
        )
