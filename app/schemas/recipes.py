from decimal import Decimal

from pydantic import Field

from app.schemas.authors import AuthorRead
from app.schemas.base import BaseSchema
from app.schemas.dictionaries import PreparationMethodRead
from app.schemas.ingredients import IngredientRead


class RecipeTitle(BaseSchema):
    id: int
    number: str
    name: str


class RecipeIngredientBase(BaseSchema):
    ingredient_id: int
    grams_per_kg: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=3,
    )
    preparation_method_id: int


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientUpdate(BaseSchema):
    ingredient_id: int | None = None
    grams_per_kg: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=3,
    )
    preparation_method_id: int | None = None


class RecipeIngredientRead(RecipeIngredientBase):
    id: int
    ingredient: IngredientRead | None = None
    preparation_method: PreparationMethodRead | None = None


class RecipeBase(BaseSchema):
    number: str = Field(max_length=64)
    name: str = Field(max_length=255)
    description: str | None = None
    product_id: int
    author_id: int


class RecipeCreate(RecipeBase):
    ingredients: list[RecipeIngredientCreate] = Field(default_factory=list)


class RecipeUpdate(BaseSchema):
    number: str | None = Field(default=None, max_length=64)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    product_id: int | None = None
    author_id: int | None = None
    ingredients: list[RecipeIngredientCreate] | None = Field(
        default=None,
    )


class RecipeRead(RecipeBase):
    id: int
    author: AuthorRead | None = None
    ingredients: list[RecipeIngredientRead] = Field(default_factory=list)


class RecipeListRead(RecipeBase):
    id: int
    author: AuthorRead | None = None
