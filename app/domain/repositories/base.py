from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def get(self, entity_id: UUID) -> T | None: ...

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> T | None: ...

    @abstractmethod
    async def list_all(self) -> list[T]: ...

    @abstractmethod
    async def list_public(self) -> list[T]: ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool: ...
    
    @abstractmethod
    async def update(self, entity: T) -> T: ...
