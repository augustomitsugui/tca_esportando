from sqlalchemy import select
from app.domain.entities.local import Local
from app.infrastructure.database.models import LocalModel
from app.infrastructure.database.models import LocalEsporteModel
from app.infrastructure.repositories.base import BaseRepositoryImpl

from uuid import UUID

class LocalRepositoryImpl(BaseRepositoryImpl[Local, LocalModel]):
    @property
    def model_class(self) -> type[LocalModel]:
        return LocalModel
    
    def _to_entity(self, model: LocalModel) -> Local:
        return Local(
            id=model.id,
            criado_por_user_id=model.criado_por_user_id,
            nome=model.nome,
            descricao=model.descricao,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Local) -> LocalModel:
        return LocalModel(
            id=entity.id,
            criado_por_user_id=entity.criado_por_user_id,
            nome=entity.nome,
            descricao=entity.descricao,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_treinador(self, treinador_id: UUID) -> list[Local]:
        raise NotImplementedError(
            "A relação Local-Treinador ainda não possui tabela associativa."
        )
    
    async def list_by_esporte(self, esporte_id: UUID) -> list[Local]:
        stmt = (
            select(LocalModel)
            .join(LocalEsporteModel, LocalEsporteModel.local_id == LocalModel.id)
            .where(LocalEsporteModel.esporte_id == esporte_id)
        )
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]
