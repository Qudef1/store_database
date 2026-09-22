from __future__ import annotations

from typing import Generic, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import bindparam, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base
from app.repositories.interfaces.base import IRepository

T = TypeVar("T", bound=Base)


class BaseRepository(IRepository[T], Generic[T]):
    """CRUD repository implemented with explicit, parameterized SQL.

    SQLAlchemy is used only for the async connection/transaction and bind
    parameters. No ORM query or persistence API is used here.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[T],
        table: str,
        columns: tuple[str, ...],
        bind_types: dict[str, object] | None = None,
    ) -> None:
        self._session = session
        self._model = model
        self._table = table
        self._columns = columns
        self._bind_types = bind_types or {}

    async def get(self, id: int) -> T | None:
        sql = text(
            f"SELECT id, {', '.join(self._columns)} FROM {self._table} WHERE id = :id"
        )
        row = (await self._session.execute(sql, {"id": id})).mappings().one_or_none()
        return self._from_row(row) if row is not None else None

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[T]:
        sql = text(
            f"SELECT id, {', '.join(self._columns)} FROM {self._table} "
            "ORDER BY id LIMIT :limit OFFSET :offset"
        )
        rows = (
            await self._session.execute(sql, {"offset": offset, "limit": limit})
        ).mappings()
        return [self._from_row(row) for row in rows]

    async def create(self, obj: T) -> T:
        column_list = ", ".join(self._columns)
        placeholders = ", ".join(f":{column}" for column in self._columns)
        sql = text(
            f"INSERT INTO {self._table} ({column_list}) "
            f"VALUES ({placeholders}) RETURNING id, {column_list}"
        )
        sql = self._with_typed_binds(sql)
        params = {column: getattr(obj, column) for column in self._columns}
        try:
            row = (await self._session.execute(sql, params)).mappings().one()
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_conflict(exc)
        return self._from_row(row)

    async def update(self, id: int, obj: T) -> T | None:
        assignments = ", ".join(f"{column} = :{column}" for column in self._columns)
        column_list = ", ".join(self._columns)
        sql = text(
            f"UPDATE {self._table} SET {assignments} WHERE id = :id "
            f"RETURNING id, {column_list}"
        )
        sql = self._with_typed_binds(sql)
        params = {
            "id": id,
            **{column: getattr(obj, column) for column in self._columns},
        }
        try:
            row = (await self._session.execute(sql, params)).mappings().one_or_none()
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_conflict(exc)
        return self._from_row(row) if row is not None else None

    async def delete(self, id: int) -> bool:
        sql = text(f"DELETE FROM {self._table} WHERE id = :id RETURNING id")
        try:
            deleted_id = (
                await self._session.execute(sql, {"id": id})
            ).scalar_one_or_none()
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_conflict(exc)
        return deleted_id is not None

    def _from_row(self, row) -> T:
        return self._model(**dict(row))

    def _with_typed_binds(self, sql):
        if not self._bind_types:
            return sql
        return sql.bindparams(
            *(bindparam(name, type_=type_) for name, type_ in self._bind_types.items())
        )

    @staticmethod
    def _raise_conflict(exc: IntegrityError) -> None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Operation violates database constraints. "
                "Check linked records and unique fields."
            ),
        ) from exc
