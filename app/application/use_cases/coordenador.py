from app.domain.entities.coordenador import Coordenador
from app.domain.repositories.coordenador import CoordenadorRepository
from app.application.dtos.coordenador import CoodenadorDTO
from .base import BaseUseCase
from uuid import UUID
import uuid
from datetime import datetime, timezone

class CoordenadorUseCases(BaseUseCase[Coordenador]):
    def __init__(self, repository: CoordenadorRepository):
        super().__init__(repository)
        
    async def create(self, coordenador_dto: CoodenadorDTO) -> Coordenador:
        agora = datetime.now(timezone.utc)
        coordenador = Coordenador(
            id=uuid.uuid4(),
            criado_em=agora,
            alterado_em=agora,
            **asdict(coordenador_dto),
        )
        return await self.repository.create(coordenador)
    
    async def list_by_esporte(self, esporte_id: UUID) -> list[Coordenador]:
        return await self.repository.list_by_esporte(esporte_id)

    
    
from dataclasses import asdict
