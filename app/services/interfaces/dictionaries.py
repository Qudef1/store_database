from app.services.interfaces.base import ICrudService
from app.models import ProductGroup, PreparationMethod
from app.schemas.dictionaries import (
    PreparationMethodCreate,
    PreparationMethodRead,
    PreparationMethodUpdate,
    ProductGroupCreate,
    ProductGroupRead,
    ProductGroupUpdate,
)

__all__ = [
    "ICrudService",
    "ProductGroup",
    "PreparationMethod",
    "ProductGroupCreate",
    "ProductGroupRead",
    "ProductGroupUpdate",
    "PreparationMethodCreate",
    "PreparationMethodRead",
    "PreparationMethodUpdate",
]