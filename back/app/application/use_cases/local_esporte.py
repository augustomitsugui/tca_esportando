from uuid import UUID

from app.core.exceptions import NotFound
from app.core.exceptions import Forbidden
from app.domain.entities.esporte import Esporte
from app.domain.entities.local import Local
from app.domain.repositories.local_esporte import LocalEsporteRepository


class LocalEsporteUseCases:
    def __init__(self, repository: LocalEsporteRepository):
        self.repository = repository

    async def add(
        self, local_id: UUID, esporte_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> None:
        if not is_superuser and not await self.repository.local_owned_by(local_id, user_id):
            raise Forbidden("Você só pode administrar seus próprios locais.")
        await self.repository.add(local_id, esporte_id)

    async def remove(
        self, local_id: UUID, esporte_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> None:
        if not is_superuser and not await self.repository.local_owned_by(local_id, user_id):
            raise Forbidden("Você só pode administrar seus próprios locais.")
        removed = await self.repository.remove(local_id, esporte_id)
        if not removed:
            raise NotFound("Vínculo entre local e esporte não encontrado.")

    async def list_by_local(self, local_id: UUID) -> list[Esporte]:
        return await self.repository.list_by_local(local_id)

    async def list_by_esporte(self, esporte_id: UUID) -> list[Local]:
        return await self.repository.list_by_esporte(esporte_id)

    async def list_by_local_for_user(
        self, local_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> list[Esporte]:
        if not is_superuser and not await self.repository.local_owned_by(
            local_id, user_id
        ):
            raise Forbidden("Você só pode consultar seus próprios locais.")
        return await self.repository.list_by_local(local_id)

    async def list_by_esporte_for_user(
        self, esporte_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> list[Local]:
        if not is_superuser and not await self.repository.esporte_owned_by(
            esporte_id, user_id
        ):
            raise Forbidden("Você só pode consultar seus próprios esportes.")
        return await self.repository.list_by_esporte(esporte_id)
