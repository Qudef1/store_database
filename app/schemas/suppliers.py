from pydantic import Field

from app.schemas.base import BaseSchema


class SupplierBase(BaseSchema):
    code: str = Field(max_length=32)
    name: str = Field(max_length=255)
    address: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseSchema):
    code: str | None = Field(default=None, max_length=32)
    name: str | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)


class SupplierRead(SupplierBase):
    id: int
