from typing import Generic, TypeVar, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
Model = TypeVar("Model")


class BaseRepositoryImpl(Generic[T, Model]):

    def __init__(self, session: AsyncSession, model: Type[Model]):
        self.session = session
        self.model = model

    async def create(self, entity: T) -> T:
        db_obj = self.model(**entity.__dict__)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        return db_obj

    async def get(self, entity_id) -> Model | None:
        result = await self.session.get(self.model, entity_id)
        return result

    async def list_all(self) -> list[Model]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def delete(self, entity_id) -> None:
        obj = await self.get(entity_id)

        if obj:
            await self.session.delete(obj)
            await self.session.commit()
