from .base import BaseRepositoryImpl
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import select
from app.domain.entities.atleta_esporte import AtletaEsporte
from app.infrastructure.database.models import AtletaEsporteModel
from uuid import UUID

class AtletaEsporteRepositoryImpl(BaseRepositoryImpl[AtletaEsporte, AtletaEsporteModel]):
    @property
    def model_class(self) -> type[AtletaEsporteModel]:
        return AtletaEsporteModel
    
    def _to_entity(self, model: AtletaEsporteModel) -> AtletaEsporte:
        return AtletaEsporte(
            id=model.id,
            atleta_id=model.atleta_id,
            esporte_id=model.esporte_id,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: AtletaEsporte) -> AtletaEsporteModel:
        return AtletaEsporteModel(
            id=entity.id,
            atleta_id=entity.atleta_id,
            esporte_id=entity.esporte_id,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    
    async def inscrever(self, atleta_id: UUID, esporte_id: UUID) -> AtletaEsporte:
        agora = datetime.now(timezone.utc)
        entity = AtletaEsporte(
            id=uuid4(),
            atleta_id=atleta_id,
            esporte_id=esporte_id,
            criado_em=agora,
            alterado_em=agora,
        )
        return await self.create(entity)
    
    async def cancelar_inscricao(self, atleta_id: UUID, esporte_id: UUID) -> None:
        stmt = select(AtletaEsporteModel).where(
            AtletaEsporteModel.atleta_id == atleta_id,
            AtletaEsporteModel.esporte_id == esporte_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.delete(model.id)
           
    async def list_by_atleta(self, atleta_id: UUID) -> list[AtletaEsporte]:
        stmt = select(AtletaEsporteModel).where(AtletaEsporteModel.atleta_id == atleta_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]
    
    async def list_by_esporte(self, esporte_id: UUID) -> list[AtletaEsporte]:
        stmt = select(AtletaEsporteModel).where(AtletaEsporteModel.esporte_id == esporte_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]
