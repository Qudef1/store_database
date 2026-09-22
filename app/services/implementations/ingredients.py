from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ingredient
from app.repositories.sqlalchemy.ingredients import IngredientRepository
from app.schemas.ingredients import IngredientCreate, IngredientRead, IngredientUpdate


class IngredientService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = IngredientRepository(session)

    async def get(self, id: int) -> IngredientRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return IngredientRead.model_validate(obj)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[IngredientRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [IngredientRead.model_validate(o) for o in objs]

    async def create(self, schema: IngredientCreate) -> IngredientRead:
        obj = Ingredient(
            name=schema.name,
            calories_per_gram=schema.calories_per_gram,
        )
        obj = await self._repo.create(obj)
        return IngredientRead.model_validate(obj)

    async def update(self, id: int, schema: IngredientUpdate) -> IngredientRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.name is not None:
            existing.name = schema.name
        if schema.calories_per_gram is not None:
            existing.calories_per_gram = schema.calories_per_gram
        existing = await self._repo.update(id, existing)
        assert existing is not None
        return IngredientRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)
