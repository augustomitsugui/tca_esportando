from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.instituicao import Instituicao
from app.domain.repositories.instituicao import InstituicaoRepository
from app.infrastructure.database.models import CoordenadorModel, InstituicaoModel


class InstituicaoRepositoryImpl(InstituicaoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: Instituicao) -> Instituicao:
        model = self._to_model(entity)
        self.session.add(model)
        coordinator = await self.session.scalar(
            select(CoordenadorModel).where(
                CoordenadorModel.user_id == entity.criado_por_user_id
            )
        )
        if coordinator is not None:
            coordinator.instituicao_id = entity.id
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get(self, entity_id: UUID) -> Instituicao | None:
        result = await self.session.execute(
            select(InstituicaoModel).where(InstituicaoModel.id == entity_id)
        )
        model = result.scalar_one_or_none()
        return None if model is None else self._to_entity(model)

    async def get_by_id(self, entity_id: UUID) -> Instituicao | None:
        return await self.get(entity_id)

    async def list_all(self) -> list[Instituicao]:
        result = await self.session.execute(select(InstituicaoModel))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def update(self, entity: Instituicao) -> Instituicao:
        model = await self._get_model(entity.id)
        if model is None:
            raise ValueError("Entidade não encontrada.")

        model.nome = entity.nome
        model.descricao = entity.descricao
        model.latitude = entity.latitude
        model.longitude = entity.longitude
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, entity_id: UUID) -> bool:
        model = await self._get_model(entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def _get_model(self, entity_id: UUID) -> InstituicaoModel | None:
        result = await self.session.execute(
            select(InstituicaoModel).where(InstituicaoModel.id == entity_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: InstituicaoModel) -> Instituicao:
        return Instituicao(
            id=model.id,
            criado_por_user_id=model.criado_por_user_id,
            nome=model.nome,
            descricao=model.descricao,
            latitude=model.latitude,
            longitude=model.longitude,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )

    @staticmethod
    def _to_model(entity: Instituicao) -> InstituicaoModel:
        return InstituicaoModel(
            id=entity.id,
            criado_por_user_id=entity.criado_por_user_id,
            nome=entity.nome,
            descricao=entity.descricao,
            latitude=entity.latitude,
            longitude=entity.longitude,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
