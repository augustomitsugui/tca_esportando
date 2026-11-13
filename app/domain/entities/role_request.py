from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.user import RoleRequestRole, RoleRequestStatus


@dataclass(frozen=True)
class RoleRequest:
    id: UUID
    user_id: UUID
    requested_role: RoleRequestRole
    status: RoleRequestStatus
    institution_id: UUID | None
    decided_by: UUID | None
    created_at: datetime
    decided_at: datetime | None = None
    rejection_reason: str | None = None
