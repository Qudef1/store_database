from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_product_service
from app.schemas.products import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    schema: ProductCreate,
    service = Depends(get_product_service),
) -> ProductRead:
    return await service.create(schema)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    service = Depends(get_product_service),
) -> ProductRead:
    obj = await service.get(product_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


@router.get("/", response_model=list[ProductRead])
async def list_products(
    offset: int = 0,
    limit: int = 100,
    service = Depends(get_product_service),
) -> list[ProductRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    schema: ProductUpdate,
    service = Depends(get_product_service),
) -> ProductRead:
    obj = await service.update(product_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    service = Depends(get_product_service),
) -> None:
    ok = await service.delete(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")