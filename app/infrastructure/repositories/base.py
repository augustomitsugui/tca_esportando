from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.base import BaseRepository

T = TypeVar("T")
M = TypeVar("M")


class BaseRepositoryImpl(BaseRepository[T], Generic[T, M], ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model_class(self) -> type[M]:
        pass

    @abstractmethod
    def _to_entity(self, model: M) -> T:
        pass

    @abstractmethod
    def _to_model(self, entity: T) -> M:
        pass

    async def create(self, entity: T) -> T:
        model = self._to_model(entity)

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def get(self, entity_id: UUID) -> T | None:
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == entity_id)
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)

    async def update(self, entity: T) -> T:
        model_data = self._to_model(entity)

        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == model_data.id)
        )

        existing_model = result.scalar_one_or_none()

        if existing_model is None:
            raise ValueError("Entidade não encontrada.")

        for column in self.model_class.__table__.columns:
            if column.primary_key:
                continue

            setattr(existing_model, column.name, getattr(model_data, column.name))

        await self.session.commit()
        await self.session.refresh(existing_model)

        return self._to_entity(existing_model)

    async def delete(self, entity_id: UUID) -> None:
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == entity_id)
        )

        model = result.scalar_one_or_none()

        if model is None:
            return

        await self.session.delete(model)
        await self.session.commit()

    async def list_all(self) -> list[T]:
        result = await self.session.execute(select(self.model_class))

        models = result.scalars().all()

        return [self._to_entity(model) for model in models]
