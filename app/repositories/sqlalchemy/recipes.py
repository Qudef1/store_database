from __future__ import annotations

from sqlalchemy import Numeric, bindparam, text
from sqlalchemy.exc import IntegrityError
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

    async def create(self, obj: Recipe) -> Recipe:
        recipe_sql = text(
            """
            INSERT INTO recipes (number, name, description, product_id, author_id)
            VALUES (:number, :name, :description, :product_id, :author_id)
            RETURNING id
            """
        )
        try:
            recipe_id = (
                await self._session.execute(
                    recipe_sql,
                    {
                        "number": obj.number,
                        "name": obj.name,
                        "description": obj.description,
                        "product_id": obj.product_id,
                        "author_id": obj.author_id,
                    },
                )
            ).scalar_one()
            await self._replace_ingredients(recipe_id, obj.ingredients)
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_conflict(exc)
        except Exception:
            await self._session.rollback()
            raise

        created = await self.get(recipe_id)
        assert created is not None
        return created

    async def update(self, id: int, obj: Recipe) -> Recipe | None:
        recipe_sql = text(
            """
            UPDATE recipes
            SET number = :number,
                name = :name,
                description = :description,
                product_id = :product_id,
                author_id = :author_id
            WHERE id = :id
            RETURNING id
            """
        )
        try:
            updated_id = (
                await self._session.execute(
                    recipe_sql,
                    {
                        "id": id,
                        "number": obj.number,
                        "name": obj.name,
                        "description": obj.description,
                        "product_id": obj.product_id,
                        "author_id": obj.author_id,
                    },
                )
            ).scalar_one_or_none()
            if updated_id is None:
                await self._session.rollback()
                return None
            await self._replace_ingredients(updated_id, obj.ingredients)
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_conflict(exc)
        except Exception:
            await self._session.rollback()
            raise

        return await self.get(updated_id)

    async def _replace_ingredients(
        self,
        recipe_id: int,
        ingredients: list[RecipeIngredient],
    ) -> None:
        await self._session.execute(
            text("DELETE FROM recipe_ingredients WHERE recipe_id = :recipe_id"),
            {"recipe_id": recipe_id},
        )
        item_sql = text(
            """
            INSERT INTO recipe_ingredients
                (recipe_id, ingredient_id, preparation_method_id, grams_per_kg)
            VALUES
                (:recipe_id, :ingredient_id, :preparation_method_id, :grams_per_kg)
            """
        ).bindparams(bindparam("grams_per_kg", type_=Numeric(12, 3)))
        for item in ingredients:
            await self._session.execute(
                item_sql,
                {
                    "recipe_id": recipe_id,
                    "ingredient_id": item.ingredient_id,
                    "preparation_method_id": item.preparation_method_id,
                    "grams_per_kg": item.grams_per_kg,
                },
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
