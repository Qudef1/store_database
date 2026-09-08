from fastapi import APIRouter, Depends, HTTPException, status

from app.db.repositories import get_author_service
from app.schemas.authors import AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter()


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
async def create_author(
    schema: AuthorCreate,
    service = Depends(get_author_service),
) -> AuthorRead:
    return await service.create(schema)


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author(
    author_id: int,
    service = Depends(get_author_service),
) -> AuthorRead:
    obj = await service.get(author_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return obj


@router.get("/", response_model=list[AuthorRead])
async def list_authors(
    offset: int = 0,
    limit: int = 100,
    service = Depends(get_author_service),
) -> list[AuthorRead]:
    return await service.list(offset=offset, limit=limit)


@router.put("/{author_id}", response_model=AuthorRead)
async def update_author(
    author_id: int,
    schema: AuthorUpdate,
    service = Depends(get_author_service),
) -> AuthorRead:
    obj = await service.update(author_id, schema)
    if obj is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return obj


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    service = Depends(get_author_service),
) -> None:
    ok = await service.delete(author_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Author not found")
