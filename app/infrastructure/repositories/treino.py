from sqlalchemy import select
from .base import BaseRepository
from app.domain.entities.treino import Treino
from app.infrastructure.database.models import TreinoModel

class TreinoRepositoryImpl(BaseRepository[Treino]):
    @property
    def model_class(self) -> type[TreinoModel]:
        return TreinoModel
    
    def _to_entity(self, model: TreinoModel) -> Treino:
        return Treino(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            data_inicio=model.data_inicio,
            data_fim=model.data_fim,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Treino) -> TreinoModel:
        return TreinoModel(
            id=entity.id,
            nome=entity.nome,
            descricao=entity.descricao,
            data_inicio=entity.data_inicio,
            data_fim=entity.data_fim,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_atleta(self, atleta_id: int) -> list[Treino]:
        stmt = select(TreinoModel).where(TreinoModel.atleta_id == atleta_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]