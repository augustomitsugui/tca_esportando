from uuid import UUID

from app.core.exceptions import Forbidden, InvalidReference, NotFound
from app.domain.entities.atleta_esporte import (
    AtletaEsporte,
    AtletaEsporteStatus,
)
from app.domain.repositories.atleta_esporte import AtletaEsporteRepository
from app.domain.entities.esporte import Esporte


class AtletaEsporteUseCases:
    def __init__(self, repository: AtletaEsporteRepository):
        self.repository = repository

    async def get_atleta_id_by_user(self, user_id: UUID) -> UUID:
        atleta_id = await self.repository.get_atleta_id_by_user(user_id)
        if atleta_id is None:
            raise Forbidden("O usuário não possui perfil de atleta.")
        return atleta_id

    async def listar_esportes_disponiveis(self) -> list[Esporte]:
        return await self.repository.list_available_esportes()

    async def solicitar(
        self, atleta_id: UUID, esporte_id: UUID, user_id: UUID
    ) -> AtletaEsporte:
        if atleta_id != await self.get_atleta_id_by_user(user_id):
            raise Forbidden("Você só pode solicitar vínculos para si mesmo.")
        if not await self.repository.esporte_exists(esporte_id):
            raise NotFound("Esporte não encontrado.")
        try:
            return await self.repository.solicitar(atleta_id, esporte_id)
        except ValueError as exc:
            raise InvalidReference(str(exc)) from exc

    async def listar_solicitacoes(
        self, atleta_id: UUID, user_id: UUID
    ) -> list[AtletaEsporte]:
        if atleta_id != await self.get_atleta_id_by_user(user_id):
            raise Forbidden("Você só pode consultar suas próprias solicitações.")
        return await self.repository.list_by_atleta_status(
            atleta_id, AtletaEsporteStatus.PENDENTE
        )

    async def listar_aprovados(
        self, atleta_id: UUID, user_id: UUID
    ) -> list[AtletaEsporte]:
        if atleta_id != await self.get_atleta_id_by_user(user_id):
            raise Forbidden("Você só pode consultar seus próprios vínculos.")
        return await self.repository.list_by_atleta_status(
            atleta_id, AtletaEsporteStatus.APROVADO
        )

    async def listar_pendentes_do_treinador(
        self, user_id: UUID
    ) -> list[AtletaEsporte]:
        return await self.repository.list_pending_for_trainer(user_id)

    async def listar_atletas_do_treinador(
        self, user_id: UUID
    ) -> list[AtletaEsporte]:
        return await self.repository.list_approved_for_trainer(user_id)

    async def decidir(
        self,
        vinculo_id: UUID,
        user_id: UUID,
        status: AtletaEsporteStatus,
    ) -> AtletaEsporte:
        vinculo = await self.repository.get(vinculo_id)
        if vinculo is None:
            raise NotFound("Vínculo atleta-esporte não encontrado.")
        if vinculo.status is not AtletaEsporteStatus.PENDENTE:
            raise InvalidReference("O vínculo já foi decidido.")
        if not await self.repository.trainer_can_manage_esporte(
            vinculo.esporte_id, user_id
        ):
            raise Forbidden("Você não administra o esporte desta solicitação.")
        return await self.repository.decide(vinculo_id, user_id, status)

    async def cancelar(
        self, vinculo_id: UUID, atleta_id: UUID, user_id: UUID
    ) -> None:
        if atleta_id != await self.get_atleta_id_by_user(user_id):
            raise Forbidden("Você só pode cancelar suas próprias solicitações.")
        if not await self.repository.cancel_pending(vinculo_id, atleta_id):
            raise NotFound("Solicitação pendente não encontrada.")
