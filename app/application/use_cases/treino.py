import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from uuid import UUID

from app.application.dtos.treino import TreinoCreateDTO, TreinoUpdateDTO
from app.core.exceptions import NotFound
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

    async def get(self, treino_id: UUID) -> Treino:
        treino = await self.repository.get(treino_id)
        if treino is None:
            raise NotFound(f"Treino com ID {treino_id} não encontrado.")
        return treino

    async def list_all(self) -> list[Treino]:
        return await self.repository.list_all()

    async def update(self, treino_id: UUID, dto: TreinoUpdateDTO) -> Treino:
        existing = await self.get(treino_id)
        values = {key: value for key, value in asdict(dto).items() if value is not None}
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

    async def delete(self, treino_id: UUID) -> None:
        await self.get(treino_id)
        await self.repository.delete(treino_id)

    async def list_by_atleta(self, atleta_id: UUID) -> list[Treino]:
        return await self.repository.list_by_atleta(atleta_id)

    async def list_upcoming_by_atleta(self, atleta_id: UUID) -> list[TreinoAgenda]:
        return await self.repository.list_upcoming_by_atleta(atleta_id)