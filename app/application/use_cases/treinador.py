from app.application.dtos.treinador import TreinadorDTO
from app.domain.entities.treinador import Treinador
from app.domain.repositories.treinador import TreinadorRepository
from .base import BaseUseCase

class TreinadorUseCases(BaseUseCase[Treinador]):
    def __init__(self, repository: TreinadorRepository):
        super().__init__(repository)
        
    async def create(self, treinador_dto: TreinadorDTO) -> Treinador:
        treinador = Treinador(**treinador_dto.model_dump())
        return await self.repository.create(treinador)
    
    async def list_by_coordenador(self, coordenador_id: int) -> list[Treinador]:
        return await self.repository.list_by_coordenador(coordenador_id)
    
    async def list_by_esporte(self, esporte_id: int) -> list[Treinador]:
        return await self.repository.list_by_esporte(esporte_id)
    