import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from uuid import UUID

from app.application.dtos.treino import UNSET, TreinoCreateDTO, TreinoUpdateDTO
from app.core.exceptions import Forbidden, NotFound
from app.domain.entities.treino import Treino, TreinoAgenda
from app.domain.repositories.treino import TreinoRepository


class TreinoUseCases:
    def __init__(self, repository: TreinoRepository):
        self.repository = repository

    async def create(self, dto: TreinoCreateDTO) -> Treino:
        agora = datetime.now(timezone.utc)
        treino = Treino(
            id=uuid.uuid4(),
            criado_em=agora,
            alterado_em=agora,
            **asdict(dto),
        )
        return await self.repository.create(treino)

    async def create_for_user(self, dto: TreinoCreateDTO, user_id: UUID) -> Treino:
        treinador_id = await self.repository.get_treinador_id_by_user(user_id)
        if treinador_id is None:
            raise Forbidden("O usuário não possui perfil de treinador.")
        if dto.treinador_id != treinador_id:
            raise Forbidden("O treino deve pertencer ao treinador autenticado.")
        if not await self.repository.trainer_can_use_resources(
            treinador_id, dto.esporte_id, dto.local_id
        ):
            raise Forbidden(
                "O esporte e o local devem pertencer à instituição do treinador."
            )
        return await self.create(dto)

    async def get(self, treino_id: UUID) -> Treino:
        treino = await self.repository.get(treino_id)
        if treino is None:
            raise NotFound(f"Treino com ID {treino_id} não encontrado.")
        return treino

    async def list_all(self) -> list[Treino]:
        return await self.repository.list_all()

    async def list_for_user(
        self, user_id: UUID, is_superuser: bool = False
    ) -> list[Treino]:
        if is_superuser:
            return await self.repository.list_all()
        treinador_id = await self.repository.get_treinador_id_by_user(user_id)
        if treinador_id is None:
            raise Forbidden("O usuário não possui perfil de treinador.")
        return await self.repository.list_by_treinador(treinador_id)

    async def get_for_user(
        self, treino_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> Treino:
        treino = await self.get(treino_id)
        if not is_superuser:
            treinador_id = await self.repository.get_treinador_id_by_user(user_id)
            if treinador_id is None or treino.treinador_id != treinador_id:
                raise Forbidden("Você só pode visualizar seus próprios treinos.")
        return treino

    async def update(self, treino_id: UUID, dto: TreinoUpdateDTO) -> Treino:
        existing = await self.get(treino_id)
        values = {
            key: value
            for key, value in asdict(dto).items()
            if value is not UNSET
        }
        updated = Treino(
            id=existing.id,
            nome=values.get("nome", existing.nome),
            descricao=values.get("descricao", existing.descricao),
            data_hora=values.get("data_hora", existing.data_hora),
            treinador_id=values.get("treinador_id", existing.treinador_id),
            local_id=values.get("local_id", existing.local_id),
            esporte_id=values.get("esporte_id", existing.esporte_id),
            criado_em=existing.criado_em,
            alterado_em=datetime.now(timezone.utc),
        )
        return await self.repository.update(updated)

    async def update_for_user(
        self, treino_id: UUID, dto: TreinoUpdateDTO, user_id: UUID
    ) -> Treino:
        existing = await self.get(treino_id)
        treinador_id = await self.repository.get_treinador_id_by_user(user_id)
        if treinador_id is None or existing.treinador_id != treinador_id:
            raise Forbidden("Você só pode alterar seus próprios treinos.")
        if (
            dto.treinador_id is not UNSET
            and dto.treinador_id is not None
            and dto.treinador_id != treinador_id
        ):
            raise Forbidden("O treino deve permanecer vinculado ao treinador autenticado.")
        esporte_id = (
            dto.esporte_id
            if dto.esporte_id is not UNSET and dto.esporte_id is not None
            else existing.esporte_id
        )
        local_id = (
            dto.local_id
            if dto.local_id is not UNSET and dto.local_id is not None
            else existing.local_id
        )
        if not await self.repository.trainer_can_use_resources(
            treinador_id, esporte_id, local_id
        ):
            raise Forbidden(
                "O esporte e o local devem pertencer à instituição do treinador."
            )
        return await self.update(
            treino_id,
            TreinoUpdateDTO(
                nome=dto.nome,
                data_hora=dto.data_hora,
                treinador_id=treinador_id,
                local_id=dto.local_id,
                esporte_id=dto.esporte_id,
                descricao=dto.descricao,
            ),
        )

    async def delete(self, treino_id: UUID) -> None:
        await self.get(treino_id)
        await self.repository.delete(treino_id)

    async def delete_for_user(self, treino_id: UUID, user_id: UUID) -> None:
        existing = await self.get(treino_id)
        treinador_id = await self.repository.get_treinador_id_by_user(user_id)
        if treinador_id is None or existing.treinador_id != treinador_id:
            raise Forbidden("Você só pode excluir seus próprios treinos.")
        await self.repository.delete(treino_id)

    async def list_by_atleta(self, atleta_id: UUID) -> list[Treino]:
        return await self.repository.list_by_atleta(atleta_id)

    async def get_atleta_by_user(self, user_id: UUID) -> UUID | None:
        return await self.repository.get_atleta_id_by_user(user_id)

    async def list_upcoming_by_atleta(self, atleta_id: UUID) -> list[TreinoAgenda]:
        return await self.repository.list_upcoming_by_atleta(atleta_id)