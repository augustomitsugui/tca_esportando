from app.application.dtos.atleta import AtletaDTO
from app.domain.entities.atleta import Atleta
from app.domain.repositories.atleta import AtletaRepository
from .base import BaseUseCase


class AtletaUseCases(BaseUseCase[Atleta]):
    def __init__(self, repository: AtletaRepository):
        super().__init__(repository)

    async def create(self, atleta_dto: AtletaDTO) -> Atleta:
        atleta = Atleta(**atleta_dto.model_dump())
        ## model dump pega os dados do DTO e cria uma instância da entidade Atleta e ai os
        ## asteriscos desempacotam os dados do DTO e passam como argumentos para o construtor da entidade Atleta wow!
        
        return await self.repository.create(atleta)

    async def list_by_treinador(self, treinador_id: int) -> list[Atleta]:
        return await self.repository.list_by_treinador(treinador_id)

    async def list_by_esporte(self, esporte_id: int) -> list[Atleta]:
        return await self.repository.list_by_esporte(esporte_id)

    async def list_by_nome(self, nome: str) -> list[Atleta]:
        return await self.repository.list_by_nome(nome)

    async def list_by_ano(self, ano: int) -> list[Atleta]:
        return await self.repository.list_by_ano(ano)
