from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entities.atleta_esporte import AtletaEsporteStatus


class AtletaEsporteCreate(BaseModel):
    esporte_id: UUID


class AtletaEsporteDecision(BaseModel):
    status: AtletaEsporteStatus


class AtletaEsporteResponse(BaseModel):
    id: UUID
    atleta_id: UUID
    esporte_id: UUID
    status: AtletaEsporteStatus
    atleta_nome: str | None = None
    esporte_nome: str | None = None

    model_config = ConfigDict(from_attributes=True)
