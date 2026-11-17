from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.application.dtos.local_instituicao import LocalInstituicaoDTO
from app.domain.entities.local_instituicao import LocalInstituicao
from app.domain.repositories.local_instituicao import LocalInstituicaoRepository
from app.core.exceptions import Forbidden


class LocalInstituicaoUseCases:
    def __init__(self, repository: LocalInstituicaoRepository):
        self.repository = repository

    async def vincular(
        self, dto: LocalInstituicaoDTO, user_id: UUID, is_superuser: bool = False
    ) -> LocalInstituicao:
        if (
            not is_superuser
            and (
                not await self.repository.local_owned_by(dto.local_id, user_id)
                or not await self.repository.institution_owned_by(
                    dto.instituicao_id, user_id
                )
            )
        ):
            raise Forbidden("Você só pode administrar seus próprios locais.")
        agora = datetime.now(timezone.utc)
        vinculo = LocalInstituicao(
            id=uuid4(),
            local_id=dto.local_id,
            instituicao_id=dto.instituicao_id,
            criado_em=agora,
            alterado_em=agora,
        )
        return await self.repository.vincular(vinculo)

    async def desvincular(
        self,
        local_id: UUID,
        instituicao_id: UUID,
        user_id: UUID,
        is_superuser: bool = False,
    ) -> None:
        if (
            not is_superuser
            and (
                not await self.repository.local_owned_by(local_id, user_id)
                or not await self.repository.institution_owned_by(
                    instituicao_id, user_id
                )
            )
        ):
            raise Forbidden("Você só pode administrar seus próprios locais.")
        await self.repository.desvincular(local_id, instituicao_id)

    async def list_by_local(self, local_id: UUID) -> list[LocalInstituicao]:
        return await self.repository.list_by_local(local_id)

    async def list_by_instituicao(
        self, instituicao_id: UUID
    ) -> list[LocalInstituicao]:
        return await self.repository.list_by_instituicao(instituicao_id)

    async def list_by_local_for_user(
        self, local_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> list[LocalInstituicao]:
        if not is_superuser and not await self.repository.local_owned_by(
            local_id, user_id
        ):
            raise Forbidden("Você só pode consultar seus próprios locais.")
        return await self.repository.list_by_local(local_id)

    async def list_by_instituicao_for_user(
        self, instituicao_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> list[LocalInstituicao]:
        if not is_superuser and not await self.repository.institution_owned_by(
            instituicao_id, user_id
        ):
            raise Forbidden("Você só pode consultar sua própria instituição.")
        return await self.repository.list_by_instituicao(instituicao_id)
