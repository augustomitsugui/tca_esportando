from sqlalchemy import select

from app.domain.entities.atleta import Atleta
from app.infrastructure.database.models import (
    AtletaEsporteModel,
    AtletaModel,
    EsporteTreinadorModel,
)
from uuid import UUID

from app.infrastructure.repositories.base import BaseRepositoryImpl
class AtletaRepositoryImpl(BaseRepositoryImpl[Atleta, AtletaModel]):


    @property
    def model_class(self) -> type[AtletaModel]:
        return AtletaModel

    def _to_entity(self, model: AtletaModel) -> Atleta:
        return Atleta(
            id=model.id,
            user_id=model.user_id,
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
            user_id=entity.user_id,
            nome=entity.nome,
            email=entity.email,
            ano=entity.ano,
            bio=entity.bio,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_treinador(self, treinador_id: UUID) -> list[Atleta]:
        result = await self.session.execute(
            select(AtletaModel)
            .join(AtletaEsporteModel, AtletaEsporteModel.atleta_id == AtletaModel.id)
            .join(
                EsporteTreinadorModel,
                EsporteTreinadorModel.esporte_id == AtletaEsporteModel.esporte_id,
            )
            .where(
                EsporteTreinadorModel.treinador_id == treinador_id,
                AtletaEsporteModel.status == "aprovado",
            )
        )
        return list(
            {
                model.id: self._to_entity(model)
                for model in result.scalars().all()
            }.values()
        )

    async def list_by_esporte(self, esporte_id: UUID) -> list[Atleta]:
        result = await self.session.execute(
            select(AtletaModel)
            .join(AtletaEsporteModel, AtletaEsporteModel.atleta_id == AtletaModel.id)
            .where(
                AtletaEsporteModel.esporte_id == esporte_id,
                AtletaEsporteModel.status == "aprovado",
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]
