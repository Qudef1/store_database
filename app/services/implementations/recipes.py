from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Recipe
from app.repositories.interfaces.recipes import IRepository as IRecipeRepository
from app.repositories.sqlalchemy.recipes import RecipeRepository
from app.schemas.recipes import RecipeCreate, RecipeListRead, RecipeRead, RecipeUpdate


class RecipeService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = RecipeRepository(session)

    async def get(self, id: int) -> RecipeRead | None:
        obj = await self._repo.get(id)
        if obj is None:
            return None
        return RecipeRead.model_validate(obj)

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[RecipeListRead]:
        objs = await self._repo.list(offset=offset, limit=limit)
        return [RecipeListRead.model_validate(o) for o in objs]

    async def create(self, schema: RecipeCreate) -> RecipeRead:
        obj = Recipe(
            number=schema.number,
            name=schema.name,
            description=schema.description,
            product_id=schema.product_id,
            author_id=schema.author_id,
        )
        await self._repo.create(obj)
        return RecipeRead.model_validate(obj)

    async def update(self, id: int, schema: RecipeUpdate) -> RecipeRead | None:
        existing = await self._repo.get(id)
        if existing is None:
            return None
        if schema.number is not None:
            existing.number = schema.number
        if schema.name is not None:
            existing.name = schema.name
        if schema.description is not None:
            existing.description = schema.description
        if schema.product_id is not None:
            existing.product_id = schema.product_id
        if schema.author_id is not None:
            existing.author_id = schema.author_id
        await self._repo.update(id, existing)
        return RecipeRead.model_validate(existing)

    async def delete(self, id: int) -> bool:
        return await self._repo.delete(id)