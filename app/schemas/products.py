from pydantic import Field

from app.schemas.base import BaseSchema
from app.schemas.dictionaries import ProductGroupRead
from app.schemas.recipes import RecipeTitle


class ProductBase(BaseSchema):
    name: str = Field(max_length=255)
    group_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseSchema):
    name: str | None = Field(default=None, max_length=255)
    group_id: int | None = None


class ProductRead(ProductBase):
    id: int
    group: ProductGroupRead | None = None


class ProductShort(BaseSchema):
    id: int
    name: str


class ProductWithRecipes(ProductRead):
    recipes: list[RecipeTitle] = Field(default_factory=list)
    