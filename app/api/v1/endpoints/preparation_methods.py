from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_preparation_method_service
from app.schemas.dictionaries import PreparationMethodCreate, PreparationMethodRead, PreparationMethodUpdate

router = APIRouter()


@router.post("/", response_model=PreparationMethodRead, status_code=status.HTTP_201_CREATED)
async def create_preparation_method(
    schema: PreparationMethodCreate,
    service = Depends(get_preparation_method_service),
) -> PreparationMethodRead:
    return await service.create(schema)


@router.get("/{preparation_method_id}", response_model=PreparationMethodRead)
async def get_preparation_method(
    preparation_method_id: int,
    service = Depends(get_preparation_method_service),
) -> PreparationMethodRead:
    obj = await service.get(preparation_method_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="PreparationMethod not found")
    return obj


@router.get("/", response_model=list[PreparationMethodRead])
async def list_preparation_methods(
    offset: int = 0,
    limit: int = 100,
    service = Depends(get_preparation_method_service),
) -> list[PreparationMethodRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{preparation_method_id}", response_model=PreparationMethodRead)
async def update_preparation_method(
    preparation_method_id: int,
    schema: PreparationMethodUpdate,
    service = Depends(get_preparation_method_service),
) -> PreparationMethodRead:
    obj = await service.update(preparation_method_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="PreparationMethod not found")
    return obj


@router.delete("/{preparation_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_preparation_method(
    preparation_method_id: int,
    service = Depends(get_preparation_method_service),
) -> None:
    ok = await service.delete(preparation_method_id)
    if not ok:
        raise HTTPException(status_code=404, detail="PreparationMethod not found")
