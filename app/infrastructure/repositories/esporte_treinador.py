from sqlalchemy import select
from .base import BaseRepository

from app.domain.entities.esporte_treinador import EsporteTreinador
from app.infrastructure.database.models import EsporteTreinadorModel

class EsporteTreinadorRepositoryImpl(BaseRepository[EsporteTreinador]):
    @property
    def model_class(self) -> type[EsporteTreinadorModel]:
        return EsporteTreinadorModel
    
    def _to_entity(self, model: EsporteTreinadorModel) -> EsporteTreinador:
        return EsporteTreinador(
            id=model.id,
            treinador_id=model.treinador_id,
            esporte_id=model.esporte_id,
        )
        
    def _to_model(self, entity: EsporteTreinador) -> EsporteTreinadorModel:
        return EsporteTreinadorModel(
            id=entity.id,
            treinador_id=entity.treinador_id,
            esporte_id=entity.esporte_id,
        )
        
    async def vincular(self, treinador_id: int, esporte_id: int) -> EsporteTreinador:
        entity = EsporteTreinador(
            id=None,
            treinador_id=treinador_id,
            esporte_id=esporte_id,
        )
        return await self.create(entity)
    
    async def desvincular(self, treinador_id: int, esporte_id: int) -> None: 
        stmt = select(EsporteTreinadorModel).where(
            EsporteTreinadorModel.treinador_id == treinador_id,
            EsporteTreinadorModel.esporte_id == esporte_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.delete(model.id)
        
    
    async def list_by_esporte(self, esporte_id: int) -> list[EsporteTreinador]:
        stmt = select(EsporteTreinadorModel).where(EsporteTreinadorModel.esporte_id == esporte_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
