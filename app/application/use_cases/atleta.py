from app.application.dtos.atleta import AtletaDTO
from app.domain.entities.atleta import Atleta
from app.domain.repositories.atleta import AtletaRepository
from .base import BaseUseCase
from uuid import UUID
import uuid
from datetime import datetime, timezone


class AtletaUseCases(BaseUseCase[Atleta]):
    def __init__(self, repository: AtletaRepository):
        super().__init__(repository)

    async def create(self, atleta_dto: AtletaDTO) -> Atleta:
        agora = datetime.now(timezone.utc)
        atleta = Atleta(
            id=uuid.uuid4(),
            criado_em=agora,
            alterado_em=agora,
            **asdict(atleta_dto),
        )
        ## model dump pega os dados do DTO e cria uma instância da entidade Atleta e ai os
        ## asteriscos desempacotam os dados do DTO e passam como argumentos para o construtor da entidade Atleta wow!
        
        return await self.repository.create(atleta)

    async def list_by_treinador(self, treinador_id: UUID) -> list[Atleta]:
        return await self.repository.list_by_treinador(treinador_id)

    async def list_by_esporte(self, esporte_id: UUID) -> list[Atleta]:
        return await self.repository.list_by_esporte(esporte_id)

    async def list_by_nome(self, nome: str) -> list[Atleta]:
        return await self.repository.list_by_nome(nome)

    async def list_by_ano(self, ano: UUID) -> list[Atleta]:
        return await self.repository.list_by_ano(ano)
from dataclasses import asdict
