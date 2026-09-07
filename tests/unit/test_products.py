import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sqlalchemy.products import ProductRepository
from app.schemas.products import ProductCreate, ProductRead
from app.services.implementations.products import ProductService


@pytest.mark.asyncio
async def test_product_service_create(db_session: AsyncSession):
    repo = ProductRepository(db_session)
    service = ProductService(db_session)
    schema = ProductCreate(name="Test", group_id=1)
    result = await service.create(schema)
    assert isinstance(result, ProductRead)
    assert result.name == "Test"