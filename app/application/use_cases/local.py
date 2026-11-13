from app.domain.entities.local import Local
from app.domain.repositories.local import LocalRepository
from app.application.dtos.local import LocalDTO
from .base import BaseUseCase
from uuid import UUID
import uuid
from datetime import datetime, timezone
from app.core.exceptions import Forbidden


class LocalUseCases(BaseUseCase[Local]):
    def __init__(self, repository: LocalRepository):
            super().__init__(repository)
            
    async def create(self, local_dto: LocalDTO, user_id: UUID) -> Local:
        agora = datetime.now(timezone.utc)
        local = Local(
            id=uuid.uuid4(),
            criado_por_user_id=user_id,
            criado_em=agora,
            alterado_em=agora,
            **asdict(local_dto),
        )
        return await self.repository.create(local)
    
    async def list_by_treinador(self, treinador_id: UUID) -> list[Local]:
        return await self.repository.list_by_treinador(treinador_id)

    async def list_by_treinador_user(self, user_id: UUID) -> list[Local]:
        treinador_id = await self.repository.get_treinador_id_by_user(user_id)
        if treinador_id is None:
            raise Forbidden("O usuário não possui perfil de treinador.")
        return await self.repository.list_by_treinador(treinador_id)

    async def list_for_user(
        self, user_id: UUID, is_superuser: bool = False
    ) -> list[Local]:
        locais = await self.repository.list_all()
        if is_superuser:
            return locais
        return await self.repository.list_by_creator(user_id)

    async def get_for_user(
        self, local_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> Local:
        local = await self.get(local_id)
        if not is_superuser and local.criado_por_user_id != user_id:
            raise Forbidden("Você só pode visualizar seus próprios locais.")
        return local

    async def update_for_user(self, local_id: UUID, local: Local, user_id: UUID, is_superuser: bool = False) -> Local:
        atual = await self.get(local_id)
        if not is_superuser and atual.criado_por_user_id != user_id:
            raise Forbidden("Você só pode alterar seus próprios locais.")
        return await self.repository.update(local)

    async def delete_for_user(self, local_id: UUID, user_id: UUID, is_superuser: bool = False) -> None:
        atual = await self.get(local_id)
        if not is_superuser and atual.criado_por_user_id != user_id:
            raise Forbidden("Você só pode excluir seus próprios locais.")
        await self.repository.delete(local_id)
from dataclasses import asdict
