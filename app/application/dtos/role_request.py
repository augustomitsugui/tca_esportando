from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.user import RoleRequestRole


@dataclass(frozen=True)
class RoleRequestCreateDTO:
    requested_role: RoleRequestRole
    institution_id: UUID | None = None


@dataclass(frozen=True)
class RoleRequestDecisionDTO:
    rejection_reason: str | None = None
