from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.treino import Treino
from app.domain.entities.treino import TreinoAgenda
from app.infrastructure.database.models import (
    AtletaEsporteModel,
    AtletaModel,
    EsporteModel,
    LocalModel,
    InstituicaoLocalModel,
    InstituicaoModel,
    RoleRequestModel,
    TreinadorModel,
    TreinoModel,
    EsporteTreinadorModel,
)
from app.infrastructure.repositories.base import BaseRepositoryImpl


class TreinoRepositoryImpl(BaseRepositoryImpl[Treino, TreinoModel]):
    @property
    def model_class(self) -> type[TreinoModel]:
        return TreinoModel
    
    def _to_entity(self, model: TreinoModel) -> Treino:
        return Treino(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            data_hora=model.data_hora,
            treinador_id=model.treinador_id,
            local_id=model.local_id,
            esporte_id=model.esporte_id,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Treino) -> TreinoModel:
        return TreinoModel(
            id=entity.id,
            nome=entity.nome,
            descricao=entity.descricao,
            data_hora=entity.data_hora,
            treinador_id=entity.treinador_id,
            local_id=entity.local_id,
            esporte_id=entity.esporte_id,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )

    async def list_by_treinador(self, treinador_id: UUID) -> list[Treino]:
        result = await self.session.execute(
            select(TreinoModel).where(TreinoModel.treinador_id == treinador_id)
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def get_treinador_id_by_user(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(TreinadorModel.id).where(TreinadorModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_atleta_id_by_user(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(AtletaModel.id).where(AtletaModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def treinador_manages_esporte(
        self, treinador_id: UUID, esporte_id: UUID
    ) -> bool:
        result = await self.session.execute(
            select(EsporteTreinadorModel.id).where(
                EsporteTreinadorModel.treinador_id == treinador_id,
                EsporteTreinadorModel.esporte_id == esporte_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def trainer_can_use_resources(
        self, treinador_id: UUID, esporte_id: UUID, local_id: UUID
    ) -> bool:
        result = await self.session.execute(
            select(EsporteModel.id).distinct()
            .join(
                RoleRequestModel,
                RoleRequestModel.institution_id == EsporteModel.instituicao_id,
            )
            .join(TreinadorModel, TreinadorModel.user_id == RoleRequestModel.user_id)
            .join(
                InstituicaoLocalModel,
                InstituicaoLocalModel.instituicao_id
                == EsporteModel.instituicao_id,
            )
            .where(
                TreinadorModel.id == treinador_id,
                EsporteModel.id == esporte_id,
                InstituicaoLocalModel.local_id == local_id,
                RoleRequestModel.requested_role == "treinador",
                RoleRequestModel.status == "aprovada",
            )
        )
        return result.scalar_one_or_none() is not None
        
    async def list_by_atleta(self, atleta_id: UUID) -> list[Treino]:
        stmt = (
            select(TreinoModel)
            .join(
                AtletaEsporteModel,
                AtletaEsporteModel.esporte_id == TreinoModel.esporte_id,
            )
            .where(AtletaEsporteModel.atleta_id == atleta_id)
            .where(AtletaEsporteModel.status == "aprovado")
            .order_by(TreinoModel.data_hora)
        )
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_upcoming_by_atleta(
        self, atleta_id: UUID
    ) -> list[TreinoAgenda]:
        agora = datetime.now(timezone.utc)
        stmt = (
            select(
                TreinoModel.id,
                TreinoModel.nome,
                EsporteModel.nome,
                TreinoModel.data_hora,
                TreinadorModel.nome,
                LocalModel.nome,
            )
            .join(
                AtletaEsporteModel,
                AtletaEsporteModel.esporte_id == TreinoModel.esporte_id,
            )
            .join(EsporteModel, EsporteModel.id == TreinoModel.esporte_id)
            .join(TreinadorModel, TreinadorModel.id == TreinoModel.treinador_id)
            .join(LocalModel, LocalModel.id == TreinoModel.local_id)
            .where(
                AtletaEsporteModel.atleta_id == atleta_id,
                AtletaEsporteModel.status == "aprovado",
                TreinoModel.data_hora >= agora,
            )
            .order_by(TreinoModel.data_hora)
        )
        result = await self.session.execute(stmt)
        return [
            TreinoAgenda(
                treino_id=row[0],
                treino_nome=row[1],
                esporte_nome=row[2],
                data_hora=row[3],
                treinador_nome=row[4],
                local_nome=row[5],
            )
            for row in result.all()
        ]
