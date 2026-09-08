from __future__ import annotations

from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Ingredient(Base):
    __tablename__ = "ingredients"
    __table_args__ = (
        CheckConstraint(
            "calories_per_gram >= 0",
            name="ingredients_calories_per_gram_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    calories_per_gram: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient",
    )

    invoice_items: Mapped[list["InvoiceItem"]] = relationship(
        back_populates="ingredient",
    )