from datetime import date
from decimal import Decimal

from pydantic import Field

from app.schemas.base import BaseSchema
from app.schemas.ingredients import IngredientRead
from app.schemas.suppliers import SupplierRead


class InvoiceItemBase(BaseSchema):
    ingredient_id: int
    quantity: Decimal = Field(
        gt=0,
        max_digits=14,
        decimal_places=3,
    )
    unit_price: Decimal = Field(
        gt=0,
        max_digits=14,
        decimal_places=4,
    )


class InvoiceItemCreate(InvoiceItemBase):
    pass


class InvoiceItemUpdate(BaseSchema):
    ingredient_id: int | None = None
    quantity: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=14,
        decimal_places=3,
    )
    unit_price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=14,
        decimal_places=4,
    )


class InvoiceItemRead(InvoiceItemBase):
    id: int
    ingredient: IngredientRead | None = None


class InvoiceBase(BaseSchema):
    number: str | None = Field(default=None, max_length=64)
    supplier_id: int
    invoice_date: date


class InvoiceCreate(InvoiceBase):
    items: list[InvoiceItemCreate] = Field(default_factory=list)


class InvoiceUpdate(BaseSchema):
    number: str | None = Field(default=None, max_length=64)
    supplier_id: int | None = None
    invoice_date: date | None = None
    items: list[InvoiceItemCreate] | None = Field(
        default=None,
    )


class InvoiceRead(InvoiceBase):
    id: int
    supplier: SupplierRead | None = None
    items: list[InvoiceItemRead] = Field(default_factory=list)
