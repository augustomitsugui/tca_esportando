from app.application.dtos.treinador import TreinadorDTO
from app.domain.entities.treinador import Treinador
from app.domain.repositories.treinador import TreinadorRepository
from .base import BaseUseCase
from dataclasses import asdict
from uuid import UUID
import uuid
from datetime import datetime, timezone

class TreinadorUseCases(BaseUseCase[Treinador]):
    def __init__(self, repository: TreinadorRepository):
        super().__init__(repository)
        
    async def create(self, treinador_dto: TreinadorDTO) -> Treinador:
        agora = datetime.now(timezone.utc)
        treinador = Treinador(
            id=uuid.uuid4(),
            criado_em=agora,
            alterado_em=agora,
            **asdict(treinador_dto),
        )
        return await self.repository.create(treinador)
    
    async def list_by_coordenador(self, coordenador_id: UUID) -> list[Treinador]:
        return await self.repository.list_by_coordenador(coordenador_id)
    
    async def list_by_esporte(self, esporte_id: UUID) -> list[Treinador]:
        return await self.repository.list_by_esporte(esporte_id)
    
