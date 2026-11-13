from app.domain.entities.treinador import Treinador
from app.infrastructure.database.models import (
    CoordenadorModel,
    EsporteTreinadorModel,
    RoleRequestModel,
    TreinadorModel,
)
from app.infrastructure.repositories.base import BaseRepositoryImpl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


class TreinadorRepositoryImpl(BaseRepositoryImpl[Treinador, TreinadorModel]):

    @property
    def model_class(self) -> type[TreinadorModel]:
        return TreinadorModel

    def _to_entity(self, model: TreinadorModel) -> Treinador:   
        return Treinador(
            id=model.id,
            user_id=model.user_id,
            nome=model.nome,
            email=model.email,
            bio=model.bio,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
    
    def _to_model(self, entity: Treinador) -> TreinadorModel:
        return TreinadorModel(
            id=entity.id,
            user_id=entity.user_id,
            nome=entity.nome,
            email=entity.email,
            bio=entity.bio,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_coordenador(self, coordenador_id: UUID) -> list[Treinador]:
        result = await self.session.execute(
            select(TreinadorModel)
            .join(RoleRequestModel, RoleRequestModel.user_id == TreinadorModel.user_id)
            .join(
                CoordenadorModel,
                CoordenadorModel.instituicao_id == RoleRequestModel.institution_id,
            )
            .where(
                CoordenadorModel.id == coordenador_id,
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
    
    async def list_by_esporte(self, esporte_id: UUID) -> list[Treinador]:
        result = await self.session.execute(
            select(TreinadorModel)
            .join(
                EsporteTreinadorModel,
                EsporteTreinadorModel.treinador_id == TreinadorModel.id,
            )
            .where(EsporteTreinadorModel.esporte_id == esporte_id)
        )
        return [self._to_entity(model) for model in result.scalars().all()]
    
    