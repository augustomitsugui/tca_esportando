from app.domain.entities.coordenador import Coordenador
from app.domain.repositories.base import BaseRepository
from app.infrastructure.database.models import CoordenadorModel

class CoordenadorRepositoryImpl(BaseRepository[Coordenador, CoordenadorModel]):
   
        
    @property
    def model_class(self) -> type[CoordenadorModel]:
        return CoordenadorModel
    
    def _to_entity(self, model: CoordenadorModel) -> Coordenador:
        return Coordenador(
            id=model.id,
            nome=model.nome,
            email=model.email,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )
        
    def _to_model(self, entity: Coordenador) -> CoordenadorModel:
        return CoordenadorModel(
            id=entity.id,
            nome=entity.nome,
            email=entity.email,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    