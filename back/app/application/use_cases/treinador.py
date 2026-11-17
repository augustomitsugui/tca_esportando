from app.application.dtos.treinador import TreinadorDTO
from app.domain.entities.treinador import Treinador
from app.domain.repositories.treinador import TreinadorRepository
from .base import BaseUseCase
from dataclasses import asdict
from uuid import UUID
import uuid
from datetime import datetime, timezone
from app.core.exceptions import Forbidden

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

    async def list_for_user(
        self, user_id: UUID, is_superuser: bool = False
    ) -> list[Treinador]:
        if is_superuser:
            return await self.repository.list_all()
        return [
            item for item in await self.repository.list_all()
            if item.user_id == user_id
        ]

    async def get_for_user(
        self, treinador_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> Treinador:
        treinador = await self.get(treinador_id)
        if not is_superuser and treinador.user_id != user_id:
            raise Forbidden("Você só pode visualizar seus próprios dados.")
        return treinador
    
