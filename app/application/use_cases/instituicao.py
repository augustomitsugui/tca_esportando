import uuid
from datetime import datetime, timezone
from uuid import UUID

from app.application.dtos.instituicao import InstituicaoDTO
from app.core.exceptions import Forbidden, NotFound
from app.domain.entities.instituicao import Instituicao
from app.domain.repositories.instituicao import InstituicaoRepository


class InstituicaoUseCases:
    def __init__(self, repository: InstituicaoRepository):
        self.repository = repository

    async def create(
        self, instituicao_dto: InstituicaoDTO, user_id: UUID
    ) -> Instituicao:
        agora = datetime.now(timezone.utc)
        instituicao = Instituicao(
            id=uuid.uuid4(),
            criado_por_user_id=user_id,
            nome=instituicao_dto.nome,
            descricao=instituicao_dto.descricao,
            latitude=instituicao_dto.latitude,
            longitude=instituicao_dto.longitude,
            criado_em=agora,
            alterado_em=agora,
        )
        return await self.repository.create(instituicao)

    async def get(self, instituicao_id: UUID) -> Instituicao:
        instituicao = await self.repository.get(instituicao_id)
        if instituicao is None:
            raise NotFound(
                f"Registro com ID {instituicao_id} não encontrado."
            )
        return instituicao

    async def list_all(self) -> list[Instituicao]:
        return await self.repository.list_all()

    async def list_for_user(
        self, user_id: UUID, is_superuser: bool = False
    ) -> list[Instituicao]:
        instituicoes = await self.repository.list_all()
        if is_superuser:
            return instituicoes
        return [
            item for item in instituicoes if item.criado_por_user_id == user_id
        ]

    async def update(
        self,
        instituicao_id: UUID,
        instituicao_dto: InstituicaoDTO,
        user_id: UUID,
        is_superuser: bool = False,
    ) -> Instituicao:
        existente = await self.get(instituicao_id)
        if not is_superuser and existente.criado_por_user_id != user_id:
            raise Forbidden("Você só pode alterar sua própria instituição.")
        atualizada = Instituicao(
            id=existente.id,
            criado_por_user_id=existente.criado_por_user_id,
            nome=instituicao_dto.nome,
            descricao=instituicao_dto.descricao,
            latitude=instituicao_dto.latitude,
            longitude=instituicao_dto.longitude,
            criado_em=existente.criado_em,
            alterado_em=existente.alterado_em,
        )
        return await self.repository.update(atualizada)

    async def get_for_user(
        self, instituicao_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> Instituicao:
        instituicao = await self.get(instituicao_id)
        if not is_superuser and instituicao.criado_por_user_id != user_id:
            raise Forbidden("Você só pode visualizar sua própria instituição.")
        return instituicao

    async def delete(
        self, instituicao_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> None:
        instituicao = await self.get(instituicao_id)
        if not is_superuser and instituicao.criado_por_user_id != user_id:
            raise Forbidden("Você só pode excluir sua própria instituição.")
        await self.repository.delete(instituicao_id)
