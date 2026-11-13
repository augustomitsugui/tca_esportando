from app.domain.entities.esporte import Esporte
from app.domain.repositories.esporte import EsporteRepository
from app.domain.repositories.esporte_treinador import EsporteTreinadorRepository
from app.application.dtos.esporte import EsporteDTO
from .base import BaseUseCase
from uuid import UUID
import uuid
from datetime import datetime, timezone
from app.core.exceptions import Forbidden

class EsporteUseCases(BaseUseCase[Esporte]):
    def __init__(
        self,
        repository: EsporteRepository,
        treinador_repository: EsporteTreinadorRepository,
    ):
        super().__init__(repository)
        self.treinador_repository = treinador_repository
        
    async def create(
        self, esporte_dto: EsporteDTO, user_id: UUID, is_superuser: bool = False
    ) -> Esporte:
        institution_id = await self.repository.get_institution_id_by_user(user_id)
        if institution_id is None and not is_superuser:
            raise Forbidden("O treinador não possui instituição aprovada.")
        agora = datetime.now(timezone.utc)
        esporte = Esporte(
            id=uuid.uuid4(),
            user_id=user_id,
            criado_em=agora,
            alterado_em=agora,
            instituicao_id=institution_id,
            **asdict(esporte_dto),
        )
        esporte = await self.repository.create(esporte)
        treinador_id = await self.treinador_repository.get_treinador_id_by_user(user_id)
        if treinador_id is not None:
            await self.treinador_repository.vincular(esporte.id, treinador_id)
        return esporte
    
    async def update_for_user(
        self,
        esporte_id: UUID,
        entity: Esporte,
        user_id: UUID,
        is_superuser: bool = False,
    ) -> Esporte:
        atual = await self.get(esporte_id)
        if not is_superuser and atual.user_id != user_id:
            raise Forbidden("Você só pode alterar seus próprios esportes.")
        return await self.repository.update(
            Esporte(
                id=atual.id,
                nome=entity.nome,
                descricao=entity.descricao,
                criado_em=atual.criado_em,
                alterado_em=entity.alterado_em,
                user_id=atual.user_id,
                instituicao_id=atual.instituicao_id,
            )
        )

    async def list_for_user(
        self, user_id: UUID, is_superuser: bool = False
    ) -> list[Esporte]:
        if is_superuser:
            return await self.repository.list_all()
        treinador_id = await self.treinador_repository.get_treinador_id_by_user(user_id)
        if treinador_id is None:
            raise Forbidden("O usuário não possui perfil de treinador.")
        return await self.repository.list_by_treinador(treinador_id)

    async def get_for_user(
        self, esporte_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> Esporte:
        esporte = await self.get(esporte_id)
        if not is_superuser and esporte.user_id != user_id:
            raise Forbidden("Você só pode visualizar seus próprios esportes.")
        return esporte

    async def delete_for_user(
        self, esporte_id: UUID, user_id: UUID, is_superuser: bool = False
    ) -> None:
        atual = await self.get(esporte_id)
        if not is_superuser and atual.user_id != user_id:
            raise Forbidden("Você só pode excluir seus próprios esportes.")
        await self.repository.delete(esporte_id)

    async def list_by_treinador(self, treinador_id: UUID) -> list[Esporte]:
        return await self.repository.list_by_treinador(treinador_id)
    
    async def list_by_local(self, local_id: UUID) -> list[Esporte]:
        return await self.repository.list_by_local(local_id)

    async def list_for_coordinator(self, user_id: UUID) -> list[Esporte]:
        institution_id = await self.repository.get_institution_id_by_coordinator(user_id)
        if institution_id is None:
            raise Forbidden("O coordenador não possui instituição aprovada.")
        return await self.repository.list_by_institution(institution_id)
    
from dataclasses import asdict
