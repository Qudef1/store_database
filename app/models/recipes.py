from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        back_populates="recipes",
    )
    author: Mapped["Author"] = relationship(
        back_populates="recipes",
    )
    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = (
        UniqueConstraint(
            "recipe_id",
            "ingredient_id",
            "preparation_method_id",
            name="uq_recipe_ingredients",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    preparation_method_id: Mapped[int] = mapped_column(
        ForeignKey("preparation_methods.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    grams_per_kg: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
    )

    recipe: Mapped["Recipe"] = relationship(
        back_populates="ingredients",
    )
    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipe_ingredients",
    )
    preparation_method: Mapped["PreparationMethod"] = relationship(
        back_populates="recipe_ingredients",
    )