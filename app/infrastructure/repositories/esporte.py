from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.esporte import Esporte
from app.infrastructure.database.models import EsporteModel
from app.domain.repositories.base import BaseRepository

class EsporteRepositoryImpl(BaseRepository[Esporte, EsporteModel]):
    @property
    def model_class(self) -> type[EsporteModel]:
        return EsporteModel
    
    def _to_entity(self, model: EsporteModel) -> Esporte:
        return Esporte(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Esporte) -> EsporteModel:
        return EsporteModel(
            id=entity.id,
            nome=entity.nome,
            descricao=entity.descricao,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_treinador(self, treinador_id: int) -> list[Esporte]:
        stmt = select(EsporteModel).where(EsporteModel.treinador_id == treinador_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
    
    async def list_by_local(self, local_id: int) -> list[Esporte]:
        stmt = select(EsporteModel).where(EsporteModel.local_id == local_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
