from typing import Generic, TypeVar
from app.core.exceptions import NotFoundException
from app.domain.repositories.base import BaseRepository

T = TypeVar("T")


class BaseUseCase(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def get(self, entity_id: int) -> T:
        entity = await self.repository.get(entity_id)

        if not entity:
            raise NotFoundException(f"Registro com ID {entity_id} não encontrado.")

        return entity

    async def list_all(self) -> list[T]:
        return await self.repository.list_all()

    async def update(self, entity_id: int, entity: T) -> T:
        existing = await self.get(entity_id)
        return await self.repository.update(entity)

    async def delete(self, entity_id: int) -> None:
        await self.get(entity_id)
        await self.repository.delete(entity_id)
