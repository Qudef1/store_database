from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Author,
    Ingredient,
    PreparationMethod,
    Recipe,
    RecipeIngredient,
)
from app.repositories.interfaces.recipes import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class RecipeRepository(BaseRepository[Recipe], IRepository[Recipe]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
            Recipe,
            "recipes",
            ("number", "name", "description", "product_id", "author_id"),
        )

    async def get(self, id: int) -> Recipe | None:
        rows = await self._load(
            "WHERE r.id = :id ORDER BY ri.id",
            {"id": id},
        )
        return rows[0] if rows else None

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[Recipe]:
        return await self._load(
            """
            WHERE r.id IN (
                SELECT id FROM recipes ORDER BY id LIMIT :limit OFFSET :offset
            )
            ORDER BY r.id, ri.id
            """,
            {"offset": offset, "limit": limit},
        )

    async def _load(self, filter_sql: str, params: dict[str, int]) -> list[Recipe]:
        sql = text(
            f"""
            SELECT
                r.id AS recipe_id,
                r.number AS recipe_number,
                r.name AS recipe_name,
                r.description,
                r.product_id,
                r.author_id,
                a.code AS author_code,
                a.surname AS author_surname,
                a.name AS author_name,
                a.country AS author_country,
                a.year AS author_year,
                ri.id AS recipe_ingredient_id,
                ri.ingredient_id,
                ri.preparation_method_id,
                ri.grams_per_kg,
                ing.name AS ingredient_name,
                ing.calories_per_gram,
                pm.code AS preparation_method_code,
                pm.name AS preparation_method_name
            FROM recipes AS r
            JOIN authors AS a ON a.id = r.author_id
            LEFT JOIN recipe_ingredients AS ri ON ri.recipe_id = r.id
            LEFT JOIN ingredients AS ing ON ing.id = ri.ingredient_id
            LEFT JOIN preparation_methods AS pm ON pm.id = ri.preparation_method_id
            {filter_sql}
            """
        )
        rows = (await self._session.execute(sql, params)).mappings()
        recipes: dict[int, Recipe] = {}
        for row in rows:
            recipe_id = row["recipe_id"]
            if recipe_id not in recipes:
                recipe = Recipe(
                    id=recipe_id,
                    number=row["recipe_number"],
                    name=row["recipe_name"],
                    description=row["description"],
                    product_id=row["product_id"],
                    author_id=row["author_id"],
                )
                recipe.author = Author(
                    id=row["author_id"],
                    code=row["author_code"],
                    surname=row["author_surname"],
                    name=row["author_name"],
                    country=row["author_country"],
                    year=row["author_year"],
                )
                recipe.ingredients = []
                recipes[recipe_id] = recipe

            if row["recipe_ingredient_id"] is not None:
                item = RecipeIngredient(
                    id=row["recipe_ingredient_id"],
                    recipe_id=recipe_id,
                    ingredient_id=row["ingredient_id"],
                    preparation_method_id=row["preparation_method_id"],
                    grams_per_kg=row["grams_per_kg"],
                )
                item.ingredient = Ingredient(
                    id=row["ingredient_id"],
                    name=row["ingredient_name"],
                    calories_per_gram=row["calories_per_gram"],
                )
                item.preparation_method = PreparationMethod(
                    id=row["preparation_method_id"],
                    code=row["preparation_method_code"],
                    name=row["preparation_method_name"],
                )
                recipes[recipe_id].ingredients.append(item)
        return list(recipes.values())
