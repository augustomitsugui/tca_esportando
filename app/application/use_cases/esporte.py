from app.domain.entities.esporte import Esporte
from app.domain.repositories.esporte import EsporteRepository
from app.application.dtos.esporte import EsporteDTO
from .base import BaseUseCase

class EsporteUseCases(BaseUseCase[Esporte]):
    def __init__(self, repository: EsporteRepository):
        super().__init__(repository)
        
    async def create(self, esporte_dto: EsporteDTO) -> Esporte:
        esporte = Esporte(**esporte_dto.model_dump())
        return await self.repository.create(esporte)
    
    async def list_by_treinador(self, treinador_id: int) -> list[Esporte]:
        return await self.repository.list_by_treinador(treinador_id)
    
    async def list_by_local(self, local_id: int) -> list[Esporte]:
        return await self.repository.list_by_local(local_id)
    