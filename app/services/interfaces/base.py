from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.models import Base

T = TypeVar("T", bound=Base)
C = TypeVar("C", bound=Base)
U = TypeVar("U", bound=Base)


class ICrudService(ABC, Generic[T, C, U]):
    @abstractmethod
    async def get(self, id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, *, offset: int = 0, limit: int = 100) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, obj: C) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, obj: U) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError