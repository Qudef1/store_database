from pydantic import Field

from app.schemas.base import BaseSchema


class AuthorBase(BaseSchema):
    code: str = Field(max_length=32)
    surname: str = Field(max_length=255)
    name: str = Field(max_length=255)
    country: str = Field(max_length=255)
    year: int = Field(ge=1800, le=2100)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseSchema):
    code: str | None = Field(default=None, max_length=32)
    surname: str | None = Field(default=None, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=255)
    year: int | None = Field(default=None, ge=1800, le=2100)


class AuthorRead(AuthorBase):
    id: int
    