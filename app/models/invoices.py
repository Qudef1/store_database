from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        UniqueConstraint(
            "supplier_id",
            "number",
            name="uq_invoices_supplier_id_number",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )

    number: Mapped[str | None] = mapped_column(String(64))

    invoice_date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    supplier: Mapped["Supplier"] = relationship(
        back_populates="invoices",
        lazy="selectin",
    )

    items: Mapped[list["InvoiceItem"]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    __table_args__ = (
        UniqueConstraint(
            "invoice_id",
            "ingredient_id",
            name="uq_invoice_items_invoice_id_ingredient_id",
        ),
        CheckConstraint(
            "quantity > 0",
            name="invoice_items_quantity_positive",
        ),
        CheckConstraint(
            "unit_price > 0",
            name="invoice_items_unit_price_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(14, 4),
        nullable=False,
    )

    invoice: Mapped["Invoice"] = relationship(
        back_populates="items",
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="invoice_items",
        lazy="selectin",
    )
    