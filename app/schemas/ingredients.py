from decimal import Decimal

from pydantic import Field

from app.schemas.base import BaseSchema


class IngredientBase(BaseSchema):
    name: str = Field(max_length=255)
    calories_per_gram: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=4,
    )


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseSchema):
    name: str | None = Field(default=None, max_length=255)
    calories_per_gram: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=4,
    )


class IngredientRead(IngredientBase):
    id: int


class IngredientShort(BaseSchema):
    id: int
    name: str
    calories_per_gram: Decimal
    