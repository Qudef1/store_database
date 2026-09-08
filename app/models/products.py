from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("product_groups.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )

    group: Mapped["ProductGroup"] = relationship(
        back_populates="products",
        lazy="selectin",
    )

    recipes: Mapped[list["Recipe"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    