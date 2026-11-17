from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.esporte import Esporte
from app.infrastructure.database.models import (
    CoordenadorModel,
    EsporteModel,
    EsporteTreinadorModel,
    RoleRequestModel,
)
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
            instituicao_id=model.instituicao_id,
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
            instituicao_id=entity.instituicao_id,
        )
        
    async def list_by_treinador(self, treinador_id: UUID) -> list[Esporte]:
        result = await self.session.execute(
            select(EsporteModel)
            .join(
                EsporteTreinadorModel,
                EsporteTreinadorModel.esporte_id == EsporteModel.id,
            )
            .where(EsporteTreinadorModel.treinador_id == treinador_id)
        )
        return [self._to_entity(model) for model in result.scalars().all()]
    
    async def list_by_local(self, local_id: UUID) -> list[Esporte]:
        stmt = (
            select(EsporteModel)
            .join(LocalEsporteModel, LocalEsporteModel.esporte_id == EsporteModel.id)
            .where(LocalEsporteModel.local_id == local_id)
        )
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]

    async def get_institution_id_by_user(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(RoleRequestModel.institution_id)
            .where(
                RoleRequestModel.user_id == user_id,
                RoleRequestModel.requested_role == "treinador",
                RoleRequestModel.status == "aprovada",
            )
            .order_by(RoleRequestModel.decided_at.desc())
        )
        return result.scalars().first()

    async def list_by_institution(self, institution_id: UUID) -> list[Esporte]:
        result = await self.session.execute(
            select(EsporteModel).where(
                EsporteModel.instituicao_id == institution_id
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def get_institution_id_by_coordinator(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(CoordenadorModel.instituicao_id).where(
                CoordenadorModel.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
