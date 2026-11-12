from sqlalchemy import select
from app.domain.entities.local import Local
from app.infrastructure.database.models import LocalModel
from app.domain.repositories.base import BaseRepository

class LocalRepositoryImpl(BaseRepository[Local]):
    @property
    def model_class(self) -> type[LocalModel]:
        return LocalModel
    
    def _to_entity(self, model: LocalModel) -> Local:
        return Local(
            id=model.id,
            nome=model.nome,
            endereco=model.endereco,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Local) -> LocalModel:
        return LocalModel(
            id=entity.id,
            nome=entity.nome,
            endereco=entity.endereco,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_treinador(self, treinador_id: int) -> list[Local]:
        stmt = select(LocalModel).where(LocalModel.treinador_id == treinador_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
    
    async def list_by_esporte(self, esporte_id: int) -> list[Local]:
        stmt = select(LocalModel).where(LocalModel.esporte_id == esporte_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
    