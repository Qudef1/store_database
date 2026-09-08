from pydantic import Field

from app.schemas.base import BaseSchema


class ProductGroupBase(BaseSchema):
    code: str = Field(max_length=32)
    name: str = Field(max_length=255)


class ProductGroupCreate(ProductGroupBase):
    pass


class ProductGroupUpdate(BaseSchema):
    code: str | None = Field(default=None, max_length=32)
    name: str | None = Field(default=None, max_length=255)


class ProductGroupRead(ProductGroupBase):
    id: int


class PreparationMethodBase(BaseSchema):
    code: str = Field(max_length=32)
    name: str = Field(max_length=255)


class PreparationMethodCreate(PreparationMethodBase):
    pass


class PreparationMethodUpdate(BaseSchema):
    code: str | None = Field(default=None, max_length=32)
    name: str | None = Field(default=None, max_length=255)


class PreparationMethodRead(PreparationMethodBase):
    id: int