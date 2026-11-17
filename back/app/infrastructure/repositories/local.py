from sqlalchemy import select
from app.domain.entities.local import Local
from app.infrastructure.database.models import (
    InstituicaoLocalModel,
    LocalModel,
    LocalEsporteModel,
    RoleRequestModel,
    TreinadorModel,
)
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

    async def get_treinador_id_by_user(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(TreinadorModel.id).where(TreinadorModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_by_creator(self, user_id: UUID) -> list[Local]:
        result = await self.session.execute(
            select(LocalModel).where(LocalModel.criado_por_user_id == user_id)
        )
        return [self._to_entity(model) for model in result.scalars().all()]
        
    async def list_by_treinador(self, treinador_id: UUID) -> list[Local]:
        result = await self.session.execute(
            select(LocalModel)
            .join(
                InstituicaoLocalModel,
                InstituicaoLocalModel.local_id == LocalModel.id,
            )
            .join(
                RoleRequestModel,
                RoleRequestModel.institution_id == InstituicaoLocalModel.instituicao_id,
            )
            .join(
                TreinadorModel,
                TreinadorModel.user_id == RoleRequestModel.user_id,
            )
            .where(
                TreinadorModel.id == treinador_id,
                RoleRequestModel.requested_role == "treinador",
                RoleRequestModel.status == "aprovada",
            )
        )
        return list(
            {
                model.id: self._to_entity(model)
                for model in result.scalars().all()
            }.values()
        )
    
    async def list_by_esporte(self, esporte_id: UUID) -> list[Local]:
        stmt = (
            select(LocalModel)
            .join(LocalEsporteModel, LocalEsporteModel.local_id == LocalModel.id)
            .where(LocalEsporteModel.esporte_id == esporte_id)
        )
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]
