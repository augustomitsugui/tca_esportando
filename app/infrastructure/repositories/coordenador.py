from app.domain.entities.coordenador import Coordenador
from app.infrastructure.repositories.base import BaseRepositoryImpl
from app.infrastructure.database.models import CoordenadorModel
from uuid import UUID
from sqlalchemy import select

class CoordenadorRepositoryImpl(BaseRepositoryImpl[Coordenador, CoordenadorModel]):
   
        
    @property
    def model_class(self) -> type[CoordenadorModel]:
        return CoordenadorModel
    
    def _to_entity(self, model: CoordenadorModel) -> Coordenador:
        return Coordenador(
            id=model.id,
            user_id=model.user_id,
            instituicao_id=model.instituicao_id,
            nome=model.nome,
            email=model.email,
            bio=model.bio,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Coordenador) -> CoordenadorModel:
        return CoordenadorModel(
            id=entity.id,
            user_id=entity.user_id,
            instituicao_id=entity.instituicao_id,
            nome=entity.nome,
            email=entity.email,
            bio=entity.bio,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_esporte(self, esporte_id: UUID) -> list[Coordenador]:
        raise NotImplementedError(
            "A relação Coordenador-Esporte ainda não possui tabela associativa."
        )
        
    