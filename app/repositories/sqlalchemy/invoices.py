from __future__ import annotations

from sqlalchemy import Date, Numeric, bindparam, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ingredient, Invoice, InvoiceItem, Supplier
from app.repositories.interfaces.invoices import IRepository
from app.repositories.sqlalchemy.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice], IRepository[Invoice]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
            Invoice,
            "invoices",
            ("supplier_id", "number", "invoice_date"),
            {"invoice_date": Date()},
        )

    async def create(self, obj: Invoice) -> Invoice:
        invoice_sql = text(
            """
            INSERT INTO invoices (supplier_id, number, invoice_date)
            VALUES (:supplier_id, :number, :invoice_date)
            RETURNING id
            """
        ).bindparams(bindparam("invoice_date", type_=Date()))
        try:
            invoice_id = (
                await self._session.execute(
                    invoice_sql,
                    {
                        "supplier_id": obj.supplier_id,
                        "number": obj.number,
                        "invoice_date": obj.invoice_date,
                    },
                )
            ).scalar_one()
            await self._replace_items(invoice_id, obj.items)
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_conflict(exc)
        except Exception:
            await self._session.rollback()
            raise

        created = await self.get(invoice_id)
        assert created is not None
        return created

    async def update(self, id: int, obj: Invoice) -> Invoice | None:
        invoice_sql = text(
            """
            UPDATE invoices
            SET supplier_id = :supplier_id,
                number = :number,
                invoice_date = :invoice_date
            WHERE id = :id
            RETURNING id
            """
        ).bindparams(bindparam("invoice_date", type_=Date()))
        try:
            updated_id = (
                await self._session.execute(
                    invoice_sql,
                    {
                        "id": id,
                        "supplier_id": obj.supplier_id,
                        "number": obj.number,
                        "invoice_date": obj.invoice_date,
                    },
                )
            ).scalar_one_or_none()
            if updated_id is None:
                await self._session.rollback()
                return None
            await self._replace_items(updated_id, obj.items)
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            self._raise_conflict(exc)
        except Exception:
            await self._session.rollback()
            raise

        return await self.get(updated_id)

    async def _replace_items(
        self,
        invoice_id: int,
        items: list[InvoiceItem],
    ) -> None:
        await self._session.execute(
            text("DELETE FROM invoice_items WHERE invoice_id = :invoice_id"),
            {"invoice_id": invoice_id},
        )
        item_sql = text(
            """
            INSERT INTO invoice_items
                (invoice_id, ingredient_id, quantity, unit_price)
            VALUES
                (:invoice_id, :ingredient_id, :quantity, :unit_price)
            """
        ).bindparams(
            bindparam("quantity", type_=Numeric(14, 3)),
            bindparam("unit_price", type_=Numeric(14, 4)),
        )
        for item in items:
            await self._session.execute(
                item_sql,
                {
                    "invoice_id": invoice_id,
                    "ingredient_id": item.ingredient_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                },
            )

    async def get(self, id: int) -> Invoice | None:
        rows = await self._load(
            "WHERE inv.id = :id ORDER BY ii.id",
            {"id": id},
        )
        return rows[0] if rows else None

    async def list(self, *, offset: int = 0, limit: int = 100) -> list[Invoice]:
        return await self._load(
            """
            WHERE inv.id IN (
                SELECT id FROM invoices ORDER BY id LIMIT :limit OFFSET :offset
            )
            ORDER BY inv.id, ii.id
            """,
            {"offset": offset, "limit": limit},
        )

    async def _load(self, filter_sql: str, params: dict[str, int]) -> list[Invoice]:
        sql = text(
            f"""
            SELECT
                inv.id AS invoice_id,
                inv.supplier_id,
                inv.number AS invoice_number,
                inv.invoice_date,
                s.code AS supplier_code,
                s.name AS supplier_name,
                s.address AS supplier_address,
                s.phone AS supplier_phone,
                ii.id AS invoice_item_id,
                ii.ingredient_id,
                ii.quantity,
                ii.unit_price,
                ing.name AS ingredient_name,
                ing.calories_per_gram
            FROM invoices AS inv
            JOIN suppliers AS s ON s.id = inv.supplier_id
            LEFT JOIN invoice_items AS ii ON ii.invoice_id = inv.id
            LEFT JOIN ingredients AS ing ON ing.id = ii.ingredient_id
            {filter_sql}
            """
        ).columns(
            invoice_date=Date(),
            quantity=Numeric(14, 3),
            unit_price=Numeric(14, 4),
        )
        rows = (await self._session.execute(sql, params)).mappings()
        invoices: dict[int, Invoice] = {}
        for row in rows:
            invoice_id = row["invoice_id"]
            if invoice_id not in invoices:
                invoice = Invoice(
                    id=invoice_id,
                    supplier_id=row["supplier_id"],
                    number=row["invoice_number"],
                    invoice_date=row["invoice_date"],
                )
                invoice.supplier = Supplier(
                    id=row["supplier_id"],
                    code=row["supplier_code"],
                    name=row["supplier_name"],
                    address=row["supplier_address"],
                    phone=row["supplier_phone"],
                )
                invoice.items = []
                invoices[invoice_id] = invoice

            if row["invoice_item_id"] is not None:
                item = InvoiceItem(
                    id=row["invoice_item_id"],
                    invoice_id=invoice_id,
                    ingredient_id=row["ingredient_id"],
                    quantity=row["quantity"],
                    unit_price=row["unit_price"],
                )
                item.ingredient = Ingredient(
                    id=row["ingredient_id"],
                    name=row["ingredient_name"],
                    calories_per_gram=row["calories_per_gram"],
                )
                invoices[invoice_id].items.append(item)
        return list(invoices.values())


class InvoiceItemRepository(BaseRepository[InvoiceItem], IRepository[InvoiceItem]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
            InvoiceItem,
            "invoice_items",
            ("invoice_id", "ingredient_id", "quantity", "unit_price"),
            {"quantity": Numeric(14, 3), "unit_price": Numeric(14, 4)},
        )
