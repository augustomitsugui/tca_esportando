from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.esporte import Esporte
from app.infrastructure.database.models import EsporteModel
from app.infrastructure.database.models import LocalEsporteModel
from app.infrastructure.repositories.base import BaseRepositoryImpl

from uuid import UUID

class EsporteRepositoryImpl(BaseRepositoryImpl[Esporte, EsporteModel]):
    @property
    def model_class(self) -> type[EsporteModel]:
        return EsporteModel
    
    def _to_entity(self, model: EsporteModel) -> Esporte:
        return Esporte(
            id=model.id,
            user_id=model.criado_por_user_id,
            nome=model.nome,
            descricao=model.descricao,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Esporte) -> EsporteModel:
        return EsporteModel(
            id=entity.id,
            criado_por_user_id=entity.user_id,
            nome=entity.nome,
            descricao=entity.descricao,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_treinador(self, treinador_id: UUID) -> list[Esporte]:
        raise NotImplementedError(
            "A relação Esporte-Treinador é tratada pela tabela associativa."
        )
    
    async def list_by_local(self, local_id: UUID) -> list[Esporte]:
        stmt = (
            select(EsporteModel)
            .join(LocalEsporteModel, LocalEsporteModel.esporte_id == EsporteModel.id)
            .where(LocalEsporteModel.local_id == local_id)
        )
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]
