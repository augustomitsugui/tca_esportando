from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.application.dtos.local_instituicao import LocalInstituicaoDTO
from app.domain.entities.local_instituicao import LocalInstituicao
from app.domain.repositories.local_instituicao import LocalInstituicaoRepository


class LocalInstituicaoUseCases:
    def __init__(self, repository: LocalInstituicaoRepository):
        self.repository = repository

    async def vincular(self, dto: LocalInstituicaoDTO) -> LocalInstituicao:
        agora = datetime.now(timezone.utc)
        vinculo = LocalInstituicao(
            id=uuid4(),
            local_id=dto.local_id,
            instituicao_id=dto.instituicao_id,
            criado_em=agora,
            alterado_em=agora,
        )
        return await self.repository.vincular(vinculo)

    async def desvincular(self, local_id: UUID, instituicao_id: UUID) -> None:
        await self.repository.desvincular(local_id, instituicao_id)

    async def list_by_local(self, local_id: UUID) -> list[LocalInstituicao]:
        return await self.repository.list_by_local(local_id)

    async def list_by_instituicao(
        self, instituicao_id: UUID
    ) -> list[LocalInstituicao]:
        return await self.repository.list_by_instituicao(instituicao_id)
