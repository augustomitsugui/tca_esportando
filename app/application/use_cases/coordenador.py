from app.domain.entities.coordenador import Coordenador
from app.domain.repositories.coordenador import CoordenadorRepository
from app.application.dtos.coordenador import CoodenadorDTO
from .base import BaseUseCase

class CoordenadorUseCases(BaseUseCase[Coordenador]):
    def __init__(self, repository: CoordenadorRepository):
        super().__init__(repository)
        
    async def create(self, coordenador_dto: CoodenadorDTO) -> Coordenador:
        coordenador = Coordenador(**coordenador_dto.model_dump())
        return await self.repository.create(coordenador)

    
    