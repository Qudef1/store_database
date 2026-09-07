from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_recipe_repository
from app.schemas.recipes import RecipeCreate, RecipeRead, RecipeUpdate
from app.services.implementations.recipes import RecipeService

router = APIRouter()


@router.post("/", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    schema: RecipeCreate,
    service: RecipeService = Depends(get_recipe_repository),
) -> RecipeRead:
    return await service.create(schema)


@router.get("/{recipe_id}", response_model=RecipeRead)
async def get_recipe(
    recipe_id: int,
    service: RecipeService = Depends(get_recipe_repository),
) -> RecipeRead:
    obj = await service.get(recipe_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return obj


@router.get("/", response_model=list[RecipeRead])
async def list_recipes(
    offset: int = 0,
    limit: int = 100,
    service: RecipeService = Depends(get_recipe_repository),
) -> list[RecipeRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{recipe_id}", response_model=RecipeRead)
async def update_recipe(
    recipe_id: int,
    schema: RecipeUpdate,
    service: RecipeService = Depends(get_recipe_repository),
) -> RecipeRead:
    obj = await service.update(recipe_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return obj


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: int,
    service: RecipeService = Depends(get_recipe_repository),
) -> None:
    ok = await service.delete(recipe_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Recipe not found")