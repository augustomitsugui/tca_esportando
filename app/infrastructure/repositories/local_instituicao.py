from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.local_instituicao import LocalInstituicao
from app.domain.repositories.local_instituicao import LocalInstituicaoRepository
from app.infrastructure.database.models import InstituicaoLocalModel


class LocalInstituicaoRepositoryImpl(LocalInstituicaoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def vincular(self, entity: LocalInstituicao) -> LocalInstituicao:
        model = InstituicaoLocalModel(
            id=entity.id,
            local_id=entity.local_id,
            instituicao_id=entity.instituicao_id,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def desvincular(self, local_id: UUID, instituicao_id: UUID) -> None:
        result = await self.session.execute(
            select(InstituicaoLocalModel).where(
                InstituicaoLocalModel.local_id == local_id,
                InstituicaoLocalModel.instituicao_id == instituicao_id,
            )
        )
        model = result.scalar_one_or_none()
        if model is not None:
            await self.session.delete(model)
            await self.session.commit()

    async def list_by_local(self, local_id: UUID) -> list[LocalInstituicao]:
        result = await self.session.execute(
            select(InstituicaoLocalModel).where(
                InstituicaoLocalModel.local_id == local_id
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_by_instituicao(self, instituicao_id: UUID) -> list[LocalInstituicao]:
        result = await self.session.execute(
            select(InstituicaoLocalModel).where(
                InstituicaoLocalModel.instituicao_id == instituicao_id
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    @staticmethod
    def _to_entity(model: InstituicaoLocalModel) -> LocalInstituicao:
        return LocalInstituicao(
            id=model.id,
            local_id=model.local_id,
            instituicao_id=model.instituicao_id,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
