from uuid import UUID

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr, Field
from uuid import UUID


class UserRead(schemas.BaseUser[UUID]):
    role: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str = Field(min_length=8)


class AuthMeResponse(UserRead):
    approval_status: str | None = None
    institution_id: UUID | None = None
    profile_id: UUID | None = None
