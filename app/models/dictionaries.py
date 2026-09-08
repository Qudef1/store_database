from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProductGroup(Base):
    __tablename__ = "product_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        back_populates="group",
        passive_deletes=True,
    )


class PreparationMethod(Base):
    __tablename__ = "preparation_methods"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="preparation_method",
        passive_deletes=True,
    )
    
