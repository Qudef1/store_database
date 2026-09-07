from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_supplier_repository
from app.schemas.suppliers import SupplierCreate, SupplierRead, SupplierUpdate
from app.services.implementations.suppliers import SupplierService

router = APIRouter()


@router.post("/", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    schema: SupplierCreate,
    service: SupplierService = Depends(get_supplier_repository),
) -> SupplierRead:
    return await service.create(schema)


@router.get("/{supplier_id}", response_model=SupplierRead)
async def get_supplier(
    supplier_id: int,
    service: SupplierService = Depends(get_supplier_repository),
) -> SupplierRead:
    obj = await service.get(supplier_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return obj


@router.get("/", response_model=list[SupplierRead])
async def list_suppliers(
    offset: int = 0,
    limit: int = 100,
    service: SupplierService = Depends(get_supplier_repository),
) -> list[SupplierRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{supplier_id}", response_model=SupplierRead)
async def update_supplier(
    supplier_id: int,
    schema: SupplierUpdate,
    service: SupplierService = Depends(get_supplier_repository),
) -> SupplierRead:
    obj = await service.update(supplier_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return obj


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: int,
    service: SupplierService = Depends(get_supplier_repository),
) -> None:
    ok = await service.delete(supplier_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Supplier not found")