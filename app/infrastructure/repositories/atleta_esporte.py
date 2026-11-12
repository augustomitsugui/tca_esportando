from .base import BaseRepository
from sqlalchemy import select
from app.domain.entities.atleta_esporte import AtletaEsporte
from app.infrastructure.database.models import AtletaEsporteModel

class AtletaEsporteRepositoryImpl(BaseRepository[AtletaEsporte]):
    @property
    def model_class(self) -> type[AtletaEsporteModel]:
        return AtletaEsporteModel
    
    def _to_entity(self, model: AtletaEsporteModel) -> AtletaEsporte:
        return AtletaEsporte(
            id=model.id,
            atleta_id=model.atleta_id,
            esporte_id=model.esporte_id,
        )
        
    def _to_model(self, entity: AtletaEsporte) -> AtletaEsporteModel:
        return AtletaEsporteModel(
            id=entity.id,
            atleta_id=entity.atleta_id,
            esporte_id=entity.esporte_id,
        )
        
    
    async def inscrever(self, atleta_id: int, esporte_id: int) -> AtletaEsporte:
        entity = AtletaEsporte(
            id=None,
            atleta_id=atleta_id,
            esporte_id=esporte_id,
        )
        return await self.create(entity)
    
    async def cancelar_inscricao(self, atleta_id: int, esporte_id: int) -> None:
        stmt = select(AtletaEsporteModel).where(
            AtletaEsporteModel.atleta_id == atleta_id,
            AtletaEsporteModel.esporte_id == esporte_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.delete(model.id)
           
    async def list_by_atleta(self, atleta_id: int) -> list[AtletaEsporte]:
        stmt = select(AtletaEsporteModel).where(AtletaEsporteModel.atleta_id == atleta_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
    
    async def list_by_esporte(self, esporte_id: int) -> list[AtletaEsporte]:
        stmt = select(AtletaEsporteModel).where(AtletaEsporteModel.esporte_id == esporte_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]