from sqlalchemy import select

from app.domain.entities.atleta import Atleta
from app.infrastructure.database.models import AtletaModel
from app.infrastructure.repositories.base import BaseRepositoryImpl
class AtletaRepositoryImpl(BaseRepositoryImpl[Atleta, AtletaModel]):

    @property
    def model_class(self) -> type[AtletaModel]:
        return AtletaModel

    def _to_entity(self, model: AtletaModel) -> Atleta:
        return Atleta(
            id=model.id,
            nome=model.nome,
            email=model.email,
            ano=model.ano,
            bio=model.bio,
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )

    def _to_model(self, entity: Atleta) -> AtletaModel:
        return AtletaModel(
            id=entity.id,
            nome=entity.nome,
            email=entity.email,
            ano=entity.ano,
            bio=entity.bio,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )
        
    async def list_by_treinador(self, treinador_id: int) -> list[Atleta]:
        stmt = select(AtletaModel).where(AtletaModel.treinador_id == treinador_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
    
    async def list_by_esporte(self, esporte_id: int) -> list[Atleta]:
        stmt = select(AtletaModel).where(AtletaModel.esporte_id == esporte_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(row[0]) for row in result.fetchall()]
