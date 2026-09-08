from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_ingredient_service
from app.schemas.ingredients import IngredientCreate, IngredientRead, IngredientUpdate

router = APIRouter()


@router.post("/", response_model=IngredientRead, status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    schema: IngredientCreate,
    service = Depends(get_ingredient_service),
) -> IngredientRead:
    return await service.create(schema)


@router.get("/{ingredient_id}", response_model=IngredientRead)
async def get_ingredient(
    ingredient_id: int,
    service = Depends(get_ingredient_service),
) -> IngredientRead:
    obj = await service.get(ingredient_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return obj


@router.get("/", response_model=list[IngredientRead])
async def list_ingredients(
    offset: int = 0,
    limit: int = 100,
    service = Depends(get_ingredient_service),
) -> list[IngredientRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{ingredient_id}", response_model=IngredientRead)
async def update_ingredient(
    ingredient_id: int,
    schema: IngredientUpdate,
    service = Depends(get_ingredient_service),
) -> IngredientRead:
    obj = await service.update(ingredient_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return obj


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
    ingredient_id: int,
    service = Depends(get_ingredient_service),
) -> None:
    ok = await service.delete(ingredient_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ingredient not found")
