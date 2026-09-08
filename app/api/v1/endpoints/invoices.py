from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_invoice_service
from app.schemas.invoices import InvoiceCreate, InvoiceRead, InvoiceUpdate

router = APIRouter()


@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    schema: InvoiceCreate,
    service = Depends(get_invoice_service),
) -> InvoiceRead:
    return await service.create(schema)


@router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(
    invoice_id: int,
    service = Depends(get_invoice_service),
) -> InvoiceRead:
    obj = await service.get(invoice_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return obj


@router.get("/", response_model=list[InvoiceRead])
async def list_invoices(
    offset: int = 0,
    limit: int = 100,
    service = Depends(get_invoice_service),
) -> list[InvoiceRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(
    invoice_id: int,
    schema: InvoiceUpdate,
    service = Depends(get_invoice_service),
) -> InvoiceRead:
    obj = await service.update(invoice_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return obj


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: int,
    service = Depends(get_invoice_service),
) -> None:
    ok = await service.delete(invoice_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Invoice not found")
