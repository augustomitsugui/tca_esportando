from app.domain.entities.coordenador import Coordenador
from app.domain.repositories.coordenador import CoordenadorRepository
from app.application.dtos.coordenador import CoodenadorDTO
from .base import BaseUseCase
from uuid import UUID
import uuid
from datetime import datetime, timezone
from app.core.exceptions import Forbidden

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

    async def list_for_user(
        self, user_id: UUID, is_superuser: bool = False
    ) -> list[Coordenador]:
        coordenadores = await self.repository.list_all()
        if is_superuser:
            return coordenadores
        return [item for item in coordenadores if item.user_id == user_id]

    async def get_for_user(
        self, coordenador_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> Coordenador:
        coordenador = await self.get(coordenador_id)
        if not is_superuser and coordenador.user_id != user_id:
            raise Forbidden("Você só pode visualizar seu próprio perfil.")
        return coordenador

    
    
from dataclasses import asdict
