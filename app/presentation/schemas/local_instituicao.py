from uuid import UUID

from pydantic import BaseModel


class LocalInstituicaoResponse(BaseModel):
    id: UUID
    local_id: UUID
    instituicao_id: UUID


class LocalInstituicaoCreate(BaseModel):
    local_id: UUID
    instituicao_id: UUID
