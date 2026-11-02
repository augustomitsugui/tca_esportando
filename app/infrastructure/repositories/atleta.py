from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.atleta import Atleta
from app.domain.repositories.atleta import AtletaRepository

from app.infrastructure.database.models import (
    AtletaModel,
    AtletaEsporteModel,
    TreinadorEsporteModel,
)

from .base import BaseRepositoryImpl


class AtletaRepositoryImpl(BaseRepositoryImpl[Atleta, AtletaModel], AtletaRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session, AtletaModel)

    def _to_entity(self, model: AtletaModel) -> Atleta:
        return Atleta(
            id=model.id,
            nome=model.nome,
            email=model.email,
            ano=model.ano,
            bio=model.bio,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )

    def _to_model(self, entity: Atleta) -> AtletaModel:
        return AtletaModel(
            id=entity.id,
            nome=entity.nome,
            email=entity.email,
            ano=entity.ano,
            bio=entity.bio,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )

    async def list_by_esporte(self, esporte_id: UUID) -> list[Atleta]:

        stmt = (
            select(AtletaModel)
            .join(AtletaEsporteModel, AtletaModel.id == AtletaEsporteModel.atleta_id)
            .where(AtletaEsporteModel.esporte_id == esporte_id)
        )

        result = await self.session.execute(stmt)

        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_by_treinador(self, treinador_id: UUID) -> list[Atleta]:

        stmt = (
            select(AtletaModel)
            .join(AtletaEsporteModel, AtletaModel.id == AtletaEsporteModel.atleta_id)
            .join(
                TreinadorEsporteModel,
                AtletaEsporteModel.esporte_id == TreinadorEsporteModel.esporte_id,
            )
            .where(TreinadorEsporteModel.treinador_id == treinador_id)
            .distinct()
        )

        result = await self.session.execute(stmt)

        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_by_name(self, nome: str) -> list[Atleta]:

        stmt = select(AtletaModel).where(AtletaModel.nome.ilike(f"%{nome}%"))

        result = await self.session.execute(stmt)

        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_by_year(self, ano: int) -> list[Atleta]:

        stmt = select(AtletaModel).where(AtletaModel.ano == ano)

        result = await self.session.execute(stmt)

        return [self._to_entity(model) for model in result.scalars().all()]
