from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.domain.entities.user import RoleRequestRole, RoleRequestStatus


class RoleRequestCreate(BaseModel):
    requested_role: RoleRequestRole
    institution_id: UUID | None = None
    institution_name: str | None = Field(default=None, max_length=100)
    institution_description: str | None = Field(default=None, max_length=1024)
    institution_latitude: float | None = None
    institution_longitude: float | None = None


class RoleRequestDecision(BaseModel):
    rejection_reason: str | None = None


class RoleRequestResponse(BaseModel):
    id: UUID
    user_id: UUID
    requested_role: RoleRequestRole
    status: RoleRequestStatus
    institution_id: UUID | None
    institution_name: str | None
    institution_description: str | None
    institution_latitude: float | None
    institution_longitude: float | None
    decided_by: UUID | None
    created_at: datetime
    decided_at: datetime | None
    rejection_reason: str | None

    model_config = ConfigDict(from_attributes=True)
