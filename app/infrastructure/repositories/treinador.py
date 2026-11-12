from app.domain.entities.treinador import Treinador
from app.infrastructure.database.models import TreinadorModel
from app.domain.repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TreinadorRepositoryImpl(BaseRepository[Treinador, TreinadorModel]):

    @property
    def model_class(self) -> type[TreinadorModel]:
        return TreinadorModel

    def _to_entity(self, model: TreinadorModel) -> Treinador:   
        return Treinador(
            id=model.id,
            nome=model.nome,
            email=model.email,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
    
    def _to_model(self, entity: Treinador) -> TreinadorModel:
        return TreinadorModel(
            id=entity.id,
            nome=entity.nome,
            email=entity.email,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_coordenador(self, coordenador_id: int) -> list[Treinador]:
        stmt = select(TreinadorModel).where(TreinadorModel.coordenador_id == coordenador_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
    
    async def list_by_esporte(self, esporte_id: int) -> list[Treinador]:
        stmt = select(TreinadorModel).where(TreinadorModel.esporte_id == esporte_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
    
    