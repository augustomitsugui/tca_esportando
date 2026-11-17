from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.role_request import RoleRequest
from app.domain.entities.user import RoleRequestRole, RoleRequestStatus
from app.domain.repositories.role_request import RoleRequestRepository
from app.infrastructure.database.models import (
    AtletaModel,
    CoordenadorModel,
    InstituicaoModel,
    RoleRequestModel,
    TreinadorModel,
    UserModel,
)


class RoleRequestRepositoryImpl(RoleRequestRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, request: RoleRequest) -> RoleRequest:
        model = RoleRequestModel(
            id=request.id,
            user_id=request.user_id,
            requested_role=request.requested_role.value,
            status=request.status.value,
            institution_id=request.institution_id,
            institution_name=request.institution_name,
            institution_description=request.institution_description,
            institution_latitude=request.institution_latitude,
            institution_longitude=request.institution_longitude,
            decided_by=request.decided_by,
            created_at=request.created_at,
            decided_at=request.decided_at,
            rejection_reason=request.rejection_reason,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get(self, request_id: UUID) -> RoleRequest | None:
        result = await self.session.execute(
            select(RoleRequestModel).where(RoleRequestModel.id == request_id)
        )
        model = result.scalar_one_or_none()
        return None if model is None else self._to_entity(model)

    async def list_for_user(self, user_id: UUID) -> list[RoleRequest]:
        result = await self.session.execute(
            select(RoleRequestModel).where(
                RoleRequestModel.user_id == user_id
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_pending_for_coordinator(
        self, institution_id: UUID
    ) -> list[RoleRequest]:
        result = await self.session.execute(
            select(RoleRequestModel).where(
                RoleRequestModel.institution_id == institution_id,
                RoleRequestModel.requested_role == RoleRequestRole.TREINADOR.value,
                RoleRequestModel.status == RoleRequestStatus.PENDENTE.value,
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_for_coordinator(
        self, institution_id: UUID
    ) -> list[RoleRequest]:
        result = await self.session.execute(
            select(RoleRequestModel).where(
                RoleRequestModel.institution_id == institution_id,
                RoleRequestModel.requested_role == RoleRequestRole.TREINADOR.value,
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_all_pending(self) -> list[RoleRequest]:
        result = await self.session.execute(
            select(RoleRequestModel).where(
                RoleRequestModel.status == RoleRequestStatus.PENDENTE.value,
                RoleRequestModel.requested_role
                == RoleRequestRole.COORDENADOR.value,
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def has_pending(
        self, user_id: UUID, requested_role: RoleRequestRole
    ) -> bool:
        result = await self.session.execute(
            select(RoleRequestModel.id).where(
                RoleRequestModel.user_id == user_id,
                RoleRequestModel.requested_role == requested_role.value,
                RoleRequestModel.status == RoleRequestStatus.PENDENTE.value,
            )
        )
        return result.scalar_one_or_none() is not None

    async def has_profile_for_role(
        self, user_id: UUID, requested_role: RoleRequestRole
    ) -> bool:
        model = (
            TreinadorModel
            if requested_role == RoleRequestRole.TREINADOR
            else CoordenadorModel
        )
        result = await self.session.execute(
            select(model.id).where(model.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None

    async def get_user_role(self, user_id: UUID) -> str | None:
        result = await self.session.execute(
            select(UserModel.role).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_coordinator_institution(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(CoordenadorModel.instituicao_id).where(
                CoordenadorModel.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_approved_institution(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(RoleRequestModel.institution_id).where(
                RoleRequestModel.user_id == user_id,
                RoleRequestModel.requested_role
                == RoleRequestRole.COORDENADOR.value,
                RoleRequestModel.status == RoleRequestStatus.APROVADA.value,
            ).order_by(RoleRequestModel.decided_at.desc())
        )
        return result.scalars().first()

    async def has_approved_role(self, user_id: UUID, role: str) -> bool:
        result = await self.session.execute(
            select(RoleRequestModel.id).where(
                RoleRequestModel.user_id == user_id,
                RoleRequestModel.requested_role == role,
                RoleRequestModel.status == RoleRequestStatus.APROVADA.value,
            )
        )
        return result.scalar_one_or_none() is not None

    async def decide(
        self,
        request: RoleRequest,
        role: str,
        approver_id: UUID,
    ) -> RoleRequest:
        result = await self.session.execute(
            select(RoleRequestModel)
            .where(
                RoleRequestModel.id == request.id,
                RoleRequestModel.status == RoleRequestStatus.PENDENTE.value,
            )
            .with_for_update()
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise ValueError("A solicitação não está mais pendente.")

        user_result = await self.session.execute(
            select(UserModel).where(UserModel.id == model.user_id).with_for_update()
        )
        user = user_result.scalar_one_or_none()
        if user is None:
            raise ValueError("Usuário solicitante não encontrado.")

        now = datetime.now(timezone.utc)
        model.status = RoleRequestStatus.APROVADA.value
        model.decided_by = approver_id
        model.decided_at = now
        model.rejection_reason = None
        user.role = role
        if request.requested_role == RoleRequestRole.COORDENADOR:
            if not model.institution_name:
                raise ValueError("Dados da instituição não encontrados.")
            institution = InstituicaoModel(
                id=__import__("uuid").uuid4(),
                criado_por_user_id=user.id,
                nome=model.institution_name,
                descricao=model.institution_description,
                latitude=model.institution_latitude,
                longitude=model.institution_longitude,
            )
            self.session.add(institution)
            coordinator = await self.session.scalar(
                select(CoordenadorModel).where(
                    CoordenadorModel.user_id == user.id
                ).with_for_update()
            )
            if coordinator is None or coordinator.instituicao_id is not None:
                raise ValueError("O coordenador já possui uma instituição.")
            coordinator.instituicao_id = institution.id

        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def reject(
        self,
        request: RoleRequest,
        approver_id: UUID,
        rejection_reason: str,
    ) -> RoleRequest:
        result = await self.session.execute(
            select(RoleRequestModel)
            .where(
                RoleRequestModel.id == request.id,
                RoleRequestModel.status == RoleRequestStatus.PENDENTE.value,
            )
            .with_for_update()
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise ValueError("A solicitação não está mais pendente.")

        model.status = RoleRequestStatus.REJEITADA.value
        model.decided_by = approver_id
        model.decided_at = datetime.now(timezone.utc)
        model.rejection_reason = rejection_reason
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: RoleRequestModel) -> RoleRequest:
        return RoleRequest(
            id=model.id,
            user_id=model.user_id,
            requested_role=RoleRequestRole(model.requested_role),
            status=RoleRequestStatus(model.status),
            institution_id=model.institution_id,
            institution_name=model.institution_name,
            institution_description=model.institution_description,
            institution_latitude=model.institution_latitude,
            institution_longitude=model.institution_longitude,
            decided_by=model.decided_by,
            created_at=model.created_at,
            decided_at=model.decided_at,
            rejection_reason=model.rejection_reason,
        )
