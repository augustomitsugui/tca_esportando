from app.domain.entities.local import Local
from app.domain.repositories.local import LocalRepository
from app.application.dtos.local import LocalDTO
from .base import BaseUseCase

class LocalUseCases(BaseUseCase[Local]):
    def __init__(self, repository: LocalRepository):
            super().__init__(repository)
            
    async def create(self, local_dto: LocalDTO) -> Local:
        local = Local(**local_dto.model_dump())
        return await self.repository.create(local)
    
    async def list_by_treinador(self, treinador_id: int) -> list[Local]:
        return await self.repository.list_by_treinador(treinador_id)