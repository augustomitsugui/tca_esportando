from app.domain.entities.local import Local
from app.domain.repositories.local import LocalRepository
from app.application.dtos.local import LocalDTO
from .base import BaseUseCase
from uuid import UUID
import uuid
from datetime import datetime, timezone


class LocalUseCases(BaseUseCase[Local]):
    def __init__(self, repository: LocalRepository):
            super().__init__(repository)
            
    async def create(self, local_dto: LocalDTO) -> Local:
        agora = datetime.now(timezone.utc)
        local = Local(
            id=uuid.uuid4(),
            criado_em=agora,
            alterado_em=agora,
            **asdict(local_dto),
        )
        return await self.repository.create(local)
    
    async def list_by_treinador(self, treinador_id: UUID) -> list[Local]:
        return await self.repository.list_by_treinador(treinador_id)
from dataclasses import asdict
