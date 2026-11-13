from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entities.user import RoleRequestRole, RoleRequestStatus


class RoleRequestCreate(BaseModel):
    requested_role: RoleRequestRole
    institution_id: UUID


class RoleRequestDecision(BaseModel):
    rejection_reason: str | None = None


class RoleRequestResponse(BaseModel):
    id: UUID
    user_id: UUID
    requested_role: RoleRequestRole
    status: RoleRequestStatus
    institution_id: UUID | None
    decided_by: UUID | None
    created_at: datetime
    decided_at: datetime | None
    rejection_reason: str | None

    model_config = ConfigDict(from_attributes=True)
