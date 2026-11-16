from uuid import UUID
from pydantic import ConfigDict

from pydantic import BaseModel


class LocalInstituicaoResponse(BaseModel):
    id: UUID
    local_id: UUID
    instituicao_id: UUID
    model_config = ConfigDict(from_attributes=True)


class LocalInstituicaoCreate(BaseModel):
    local_id: UUID
    instituicao_id: UUID
