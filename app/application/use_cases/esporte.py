from app.domain.entities.esporte import Esporte
from app.domain.repositories.esporte import EsporteRepository
from app.application.dtos.esporte import EsporteDTO
from .base import BaseUseCase
from uuid import UUID
import uuid
from datetime import datetime, timezone

class EsporteUseCases(BaseUseCase[Esporte]):
    def __init__(self, repository: EsporteRepository):
        super().__init__(repository)
        
    async def create(self, esporte_dto: EsporteDTO) -> Esporte:
        agora = datetime.now(timezone.utc)
        esporte = Esporte(
            id=uuid.uuid4(),
            criado_em=agora,
            alterado_em=agora,
            **asdict(esporte_dto),
        )
        return await self.repository.create(esporte)
    
    async def list_by_treinador(self, treinador_id: UUID) -> list[Esporte]:
        return await self.repository.list_by_treinador(treinador_id)
    
    async def list_by_local(self, local_id: UUID) -> list[Esporte]:
        return await self.repository.list_by_local(local_id)
    
from dataclasses import asdict
