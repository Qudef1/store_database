from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_product_group_service
from app.schemas.dictionaries import ProductGroupCreate, ProductGroupRead, ProductGroupUpdate

router = APIRouter()


@router.post("/", response_model=ProductGroupRead, status_code=status.HTTP_201_CREATED)
async def create_product_group(
    schema: ProductGroupCreate,
    service = Depends(get_product_group_service),
) -> ProductGroupRead:
    return await service.create(schema)


@router.get("/{product_group_id}", response_model=ProductGroupRead)
async def get_product_group(
    product_group_id: int,
    service = Depends(get_product_group_service),
) -> ProductGroupRead:
    obj = await service.get(product_group_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ProductGroup not found")
    return obj


@router.get("/", response_model=list[ProductGroupRead])
async def list_product_groups(
    offset: int = 0,
    limit: int = 100,
    service = Depends(get_product_group_service),
) -> list[ProductGroupRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{product_group_id}", response_model=ProductGroupRead)
async def update_product_group(
    product_group_id: int,
    schema: ProductGroupUpdate,
    service = Depends(get_product_group_service),
) -> ProductGroupRead:
    obj = await service.update(product_group_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="ProductGroup not found")
    return obj


@router.delete("/{product_group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_group(
    product_group_id: int,
    service = Depends(get_product_group_service),
) -> None:
    ok = await service.delete(product_group_id)
    if not ok:
        raise HTTPException(status_code=404, detail="ProductGroup not found")
