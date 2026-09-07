from app.services.interfaces.base import ICrudService
from app.models import Supplier
from app.schemas.suppliers import SupplierCreate, SupplierUpdate, SupplierRead

__all__ = [
    "ICrudService",
    "Supplier",
    "SupplierCreate",
    "SupplierRead",
    "SupplierUpdate",
]