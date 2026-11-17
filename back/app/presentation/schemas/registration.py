from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AthleteRegistration(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nome: str = Field(max_length=100)
    ano: int
    bio: str | None = Field(default=None, max_length=1024)


class TrainerRegistration(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nome: str = Field(max_length=100)
    bio: str | None = Field(default=None, max_length=1024)
    institution_id: UUID


class CoordinatorRegistration(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nome: str = Field(max_length=100)
    bio: str | None = Field(default=None, max_length=1024)
    institution_name: str = Field(max_length=100)
    institution_description: str | None = Field(default=None, max_length=1024)
    institution_latitude: float | None = None
    institution_longitude: float | None = None
