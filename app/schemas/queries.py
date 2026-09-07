from datetime import date

from pydantic import Field

from app.schemas.base import BaseSchema


class PaginationQuery(BaseSchema):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)


class ProductListQuery(PaginationQuery):
    group_id: int | None = None
    name: str | None = Field(default=None, max_length=255)


class RecipeListQuery(PaginationQuery):
    product_id: int | None = None
    author_id: int | None = None


class SupplierListQuery(PaginationQuery):
    name: str | None = Field(default=None, max_length=255)


class IngredientListQuery(PaginationQuery):
    name: str | None = Field(default=None, max_length=255)


class InvoiceListQuery(PaginationQuery):
    supplier_id: int | None = None
    invoice_date: date | None = None


class PriceListQuery(BaseSchema):
    supplier_id: int
    price_date: date


class MinCalorieDishesQuery(BaseSchema):
    limit: int = Field(default=10, ge=1, le=100)


class DishWithRecipesQuery(PaginationQuery):
    group_id: int | None = None
    product_name: str | None = Field(default=None, max_length=255)
    