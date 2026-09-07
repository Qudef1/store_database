from app.services.interfaces.base import ICrudService
from app.models import Product
from app.schemas.products import ProductCreate, ProductUpdate, ProductRead

__all__ = [
    "ICrudService",
    "Product",
    "ProductCreate",
    "ProductRead",
    "ProductUpdate",
]