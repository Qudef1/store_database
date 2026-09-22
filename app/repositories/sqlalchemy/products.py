from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product, ProductGroup
from app.repositories.interfaces.products import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class ProductRepository(BaseRepository[Product], IRepository[Product]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Product, "products", ("name", "group_id"))

    async def get(self, id: int) -> Product | None:
        sql = text(
            """
            SELECT
                p.id, p.name, p.group_id,
                pg.id AS group_object_id,
                pg.code AS group_code,
                pg.name AS group_name
            FROM products AS p
            JOIN product_groups AS pg ON pg.id = p.group_id
            WHERE p.id = :id
            """
        )
        row = (await self._session.execute(sql, {"id": id})).mappings().one_or_none()
        return self._from_joined_row(row) if row is not None else None

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[Product]:
        sql = text(
            """
            SELECT
                p.id, p.name, p.group_id,
                pg.id AS group_object_id,
                pg.code AS group_code,
                pg.name AS group_name
            FROM products AS p
            JOIN product_groups AS pg ON pg.id = p.group_id
            ORDER BY p.id
            LIMIT :limit OFFSET :offset
            """
        )
        rows = (
            await self._session.execute(sql, {"offset": offset, "limit": limit})
        ).mappings()
        return [self._from_joined_row(row) for row in rows]

    @staticmethod
    def _from_joined_row(row) -> Product:
        product = Product(id=row["id"], name=row["name"], group_id=row["group_id"])
        product.group = ProductGroup(
            id=row["group_object_id"],
            code=row["group_code"],
            name=row["group_name"],
        )
        return product
