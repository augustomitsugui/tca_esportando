from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.role_request import RoleRequest
from app.domain.entities.user import RoleRequestRole


class RoleRequestRepository(ABC):
    @abstractmethod
    async def create(self, request: RoleRequest) -> RoleRequest:
        ...

    @abstractmethod
    async def get(self, request_id: UUID) -> RoleRequest | None:
        ...

    @abstractmethod
    async def list_for_user(self, user_id: UUID) -> list[RoleRequest]:
        ...

    @abstractmethod
    async def list_pending_for_coordinator(
        self, institution_id: UUID
    ) -> list[RoleRequest]:
        ...

    @abstractmethod
    async def list_for_coordinator(self, institution_id: UUID) -> list[RoleRequest]:
        ...

    @abstractmethod
    async def list_all_pending(self) -> list[RoleRequest]:
        ...

    @abstractmethod
    async def has_pending(self, user_id: UUID, requested_role: RoleRequestRole) -> bool:
        ...

    @abstractmethod
    async def has_profile_for_role(
        self, user_id: UUID, requested_role: RoleRequestRole
    ) -> bool:
        ...

    @abstractmethod
    async def get_user_role(self, user_id: UUID) -> str | None:
        ...

    @abstractmethod
    async def get_coordinator_institution(self, user_id: UUID) -> UUID | None:
        ...

    @abstractmethod
    async def get_approved_institution(self, user_id: UUID) -> UUID | None:
        ...

    @abstractmethod
    async def has_approved_role(self, user_id: UUID, role: str) -> bool:
        ...

    @abstractmethod
    async def decide(
        self,
        request: RoleRequest,
        role: str,
        approver_id: UUID,
    ) -> RoleRequest:
        ...

    @abstractmethod
    async def reject(
        self,
        request: RoleRequest,
        approver_id: UUID,
        rejection_reason: str,
    ) -> RoleRequest:
        ...
