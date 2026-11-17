from sqlalchemy import select
from .base import BaseRepositoryImpl
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.esporte_treinador import EsporteTreinador
from app.infrastructure.database.models import EsporteTreinadorModel, TreinadorModel
from uuid import UUID

class EsporteTreinadorRepositoryImpl(
    BaseRepositoryImpl[EsporteTreinador, EsporteTreinadorModel]
):
    @property
    def model_class(self) -> type[EsporteTreinadorModel]:
        return EsporteTreinadorModel
    
    def _to_entity(self, model: EsporteTreinadorModel) -> EsporteTreinador:
        return EsporteTreinador(
            id=model.id,
            treinador_id=model.treinador_id,
            esporte_id=model.esporte_id,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: EsporteTreinador) -> EsporteTreinadorModel:
        return EsporteTreinadorModel(
            id=entity.id,
            treinador_id=entity.treinador_id,
            esporte_id=entity.esporte_id,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def vincular(self, esporte_id: UUID, treinador_id: UUID) -> EsporteTreinador:
        agora = datetime.now(timezone.utc)
        entity = EsporteTreinador(
            id=uuid4(),
            treinador_id=treinador_id,
            esporte_id=esporte_id,
            criado_em=agora,
            alterado_em=agora,
        )
        return await self.create(entity)
    
    async def desvincular(self, esporte_id: UUID, treinador_id: UUID) -> None:
        stmt = select(EsporteTreinadorModel).where(
            EsporteTreinadorModel.treinador_id == treinador_id,
            EsporteTreinadorModel.esporte_id == esporte_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.delete(model.id)
        
    
    async def list_by_esporte(self, esporte_id: UUID) -> list[EsporteTreinador]:
        stmt = select(EsporteTreinadorModel).where(EsporteTreinadorModel.esporte_id == esporte_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]

    async def get_treinador_id_by_user(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(TreinadorModel.id).where(TreinadorModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def exists(self, esporte_id: UUID, treinador_id: UUID) -> bool:
        result = await self.session.execute(
            select(EsporteTreinadorModel.id).where(
                EsporteTreinadorModel.esporte_id == esporte_id,
                EsporteTreinadorModel.treinador_id == treinador_id,
            )
        )
        return result.scalar_one_or_none() is not None
