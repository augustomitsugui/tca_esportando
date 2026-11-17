from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.esporte import Esporte
from app.domain.entities.local import Local
from app.domain.repositories.local_esporte import LocalEsporteRepository
from app.infrastructure.database.models import (
    EsporteModel,
    LocalEsporteModel,
    LocalModel,
)


class LocalEsporteRepositoryImpl(LocalEsporteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def local_owned_by(self, local_id: UUID, user_id: UUID) -> bool:
        result = await self.session.execute(
            select(LocalModel.id).where(
                LocalModel.id == local_id,
                LocalModel.criado_por_user_id == user_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def esporte_owned_by(self, esporte_id: UUID, user_id: UUID) -> bool:
        result = await self.session.execute(
            select(EsporteModel.id).where(
                EsporteModel.id == esporte_id,
                EsporteModel.criado_por_user_id == user_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def add(self, local_id: UUID, esporte_id: UUID) -> None:
        existing = await self.session.execute(
            select(LocalEsporteModel).where(
                LocalEsporteModel.local_id == local_id,
                LocalEsporteModel.esporte_id == esporte_id,
            )
        )
        if existing.scalar_one_or_none() is not None:
            return

        self.session.add(
            LocalEsporteModel(local_id=local_id, esporte_id=esporte_id)
        )
        await self.session.commit()

    async def remove(self, local_id: UUID, esporte_id: UUID) -> bool:
        result = await self.session.execute(
            delete(LocalEsporteModel).where(
                LocalEsporteModel.local_id == local_id,
                LocalEsporteModel.esporte_id == esporte_id,
            )
        )
        await self.session.commit()
        return result.rowcount > 0

    async def list_by_local(self, local_id: UUID) -> list[Esporte]:
        result = await self.session.execute(
            select(EsporteModel)
            .join(LocalEsporteModel, LocalEsporteModel.esporte_id == EsporteModel.id)
            .where(LocalEsporteModel.local_id == local_id)
        )
        return [self._to_esporte(model) for model in result.scalars().all()]

    async def list_by_esporte(self, esporte_id: UUID) -> list[Local]:
        result = await self.session.execute(
            select(LocalModel)
            .join(LocalEsporteModel, LocalEsporteModel.local_id == LocalModel.id)
            .where(LocalEsporteModel.esporte_id == esporte_id)
        )
        return [self._to_local(model) for model in result.scalars().all()]

    @staticmethod
    def _to_esporte(model: EsporteModel) -> Esporte:
        return Esporte(
            id=model.id,
            user_id=model.criado_por_user_id,
            nome=model.nome,
            descricao=model.descricao,
            criado_em=model.criado_em,
            instituicao_id=model.instituicao_id,
            alterado_em=model.alterado_em,
        )

    @staticmethod
    def _to_local(model: LocalModel) -> Local:
        return Local(
            id=model.id,
            criado_por_user_id=model.criado_por_user_id,
            nome=model.nome,
            descricao=model.descricao,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
