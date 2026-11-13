import uuid
from datetime import datetime, timezone
from uuid import UUID

from app.application.dtos.role_request import (
    RoleRequestCreateDTO,
    RoleRequestDecisionDTO,
)
from app.core.exceptions import Forbidden, InvalidReference, NotFound
from app.domain.entities.role_request import RoleRequest
from app.domain.entities.user import (
    RoleRequestRole,
    RoleRequestStatus,
    UserRole,
)
from app.domain.repositories.role_request import RoleRequestRepository


class RoleRequestUseCases:
    def __init__(self, repository: RoleRequestRepository):
        self.repository = repository

    async def request(
        self, user_id: UUID, dto: RoleRequestCreateDTO
    ) -> RoleRequest:
        if dto.requested_role not in (
            RoleRequestRole.TREINADOR,
            RoleRequestRole.COORDENADOR,
        ):
            raise Forbidden("Esse cargo não pode ser solicitado.")

        if dto.requested_role == RoleRequestRole.TREINADOR and dto.institution_id is None:
            raise InvalidReference("A instituição é obrigatória para treinadores.")
        if dto.requested_role == RoleRequestRole.COORDENADOR and (
            not dto.institution_name or not dto.institution_name.strip()
        ):
            raise InvalidReference("O nome da instituição é obrigatório.")

        current_role = await self.repository.get_user_role(user_id)
        if current_role == dto.requested_role.value and await self.repository.has_approved_role(
            user_id, dto.requested_role.value
        ):
            raise InvalidReference("O usuário já possui esse cargo aprovado.")

        if await self.repository.has_pending(user_id, dto.requested_role):
            raise InvalidReference("Já existe uma solicitação pendente para esse cargo.")
        if not await self.repository.has_profile_for_role(
            user_id, dto.requested_role
        ):
            raise InvalidReference(
                "O perfil correspondente ao cargo deve ser criado pelo cadastro especializado."
            )

        request = RoleRequest(
            id=uuid.uuid4(),
            user_id=user_id,
            requested_role=dto.requested_role,
            status=RoleRequestStatus.PENDENTE,
            institution_id=dto.institution_id,
            institution_name=dto.institution_name,
            institution_description=dto.institution_description,
            institution_latitude=dto.institution_latitude,
            institution_longitude=dto.institution_longitude,
            decided_by=None,
            created_at=datetime.now(timezone.utc),
        )
        return await self.repository.create(request)

    async def get(self, request_id: UUID) -> RoleRequest:
        request = await self.repository.get(request_id)
        if request is None:
            raise NotFound("Solicitação não encontrada.")
        return request

    async def list_my_requests(self, user_id: UUID) -> list[RoleRequest]:
        return await self.repository.list_for_user(user_id)

    async def list_for_coordinator(self, coordinator_id: UUID) -> list[RoleRequest]:
        institution_id = await self.repository.get_coordinator_institution(
            coordinator_id
        )
        if institution_id is None:
            raise Forbidden("O coordenador não possui instituição definida.")
        return await self.repository.list_pending_for_coordinator(institution_id)

    async def list_coordinator_history(
        self, coordinator_id: UUID
    ) -> list[RoleRequest]:
        institution_id = await self.repository.get_coordinator_institution(
            coordinator_id
        )
        if institution_id is None:
            raise Forbidden("O coordenador não possui instituição definida.")
        return await self.repository.list_for_coordinator(institution_id)

    async def list_for_superadmin(self) -> list[RoleRequest]:
        return await self.repository.list_all_pending()

    async def validate_coordinator_institution(
        self, user_id: UUID, institution_id: UUID
    ) -> None:
        approved_institution = await self.repository.get_approved_institution(user_id)
        if approved_institution != institution_id:
            raise Forbidden(
                "A instituição não corresponde à aprovação do coordenador."
            )

    async def approve(
        self,
        request_id: UUID,
        approver_id: UUID,
        is_superadmin: bool,
    ) -> RoleRequest:
        request = await self.get(request_id)
        if request.status != RoleRequestStatus.PENDENTE:
            raise InvalidReference("A solicitação já foi decidida.")

        if request.user_id == approver_id:
            raise Forbidden("O solicitante não pode aprovar a própria solicitação.")

        if request.requested_role == RoleRequestRole.COORDENADOR:
            if not is_superadmin:
                raise Forbidden("Apenas o Super Admin pode aprovar coordenadores.")
        elif request.requested_role == RoleRequestRole.TREINADOR:
            approver_role = await self.repository.get_user_role(approver_id)
            if approver_role != UserRole.COORDENADOR.value:
                raise Forbidden("Apenas um coordenador pode aprovar treinadores.")
            institution_id = await self.repository.get_coordinator_institution(
                approver_id
            )
            if institution_id != request.institution_id:
                raise Forbidden("A solicitação está fora da sua instituição.")
        else:
            raise Forbidden("Cargo solicitado inválido.")

        try:
            return await self.repository.decide(
                request, request.requested_role.value, approver_id
            )
        except ValueError as exc:
            raise InvalidReference(str(exc)) from exc

    async def reject(
        self,
        request_id: UUID,
        approver_id: UUID,
        is_superadmin: bool,
        dto: RoleRequestDecisionDTO,
    ) -> RoleRequest:
        request = await self.get(request_id)
        if request.status != RoleRequestStatus.PENDENTE:
            raise InvalidReference("A solicitação já foi decidida.")
        if request.user_id == approver_id:
            raise Forbidden("O solicitante não pode rejeitar a própria solicitação.")
        if not dto.rejection_reason or not dto.rejection_reason.strip():
            raise InvalidReference("O motivo da rejeição é obrigatório.")

        if request.requested_role == RoleRequestRole.COORDENADOR:
            if not is_superadmin:
                raise Forbidden("Apenas o Super Admin pode rejeitar coordenadores.")
        elif request.requested_role == RoleRequestRole.TREINADOR:
            approver_role = await self.repository.get_user_role(approver_id)
            if approver_role != UserRole.COORDENADOR.value:
                raise Forbidden("Apenas um coordenador pode rejeitar treinadores.")
            institution_id = await self.repository.get_coordinator_institution(
                approver_id
            )
            if institution_id != request.institution_id:
                raise Forbidden("A solicitação está fora da sua instituição.")
        else:
            raise Forbidden("Cargo solicitado inválido.")

        try:
            return await self.repository.reject(
                request, approver_id, dto.rejection_reason.strip()
            )
        except ValueError as exc:
            raise InvalidReference(str(exc)) from exc
