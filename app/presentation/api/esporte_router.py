from dataclasses import replace
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.esporte import EsporteDTO
from app.application.use_cases.esporte import EsporteUseCases
from app.presentation.dependencies import get_esporte_use_cases
from app.presentation.dependencies import require_treinador
from app.infrastructure.database.models import UserModel
from app.presentation.schemas.esporte import (
    EsporteCreate,
    EsporteResponse,
    EsporteUpdate,
)

router = APIRouter(prefix="/esportes", tags=["Esportes"])


@router.post("", response_model=EsporteResponse, status_code=status.HTTP_201_CREATED)
async def criar_esporte(
    data: EsporteCreate,
    user: UserModel = Depends(require_treinador),
    use_cases: EsporteUseCases = Depends(get_esporte_use_cases),
) -> EsporteResponse:
    esporte = await use_cases.create(EsporteDTO(**data.model_dump()), user.id)
    return EsporteResponse.model_validate(esporte)


@router.get("", response_model=list[EsporteResponse])
async def listar_esportes(
    user: UserModel = Depends(require_treinador),
    use_cases: EsporteUseCases = Depends(get_esporte_use_cases),
) -> list[EsporteResponse]:
    return [
        EsporteResponse.model_validate(item)
        for item in await use_cases.list_for_user(user.id, user.is_superuser)
    ]


@router.get("/{esporte_id}", response_model=EsporteResponse)
async def obter_esporte(
    esporte_id: UUID,
    user: UserModel = Depends(require_treinador),
    use_cases: EsporteUseCases = Depends(get_esporte_use_cases),
) -> EsporteResponse:
    return EsporteResponse.model_validate(
        await use_cases.get_for_user(esporte_id, user.id, user.is_superuser)
    )


@router.put("/{esporte_id}", response_model=EsporteResponse)
async def atualizar_esporte(
    esporte_id: UUID,
    data: EsporteUpdate,
    user: UserModel = Depends(require_treinador),
    use_cases: EsporteUseCases = Depends(get_esporte_use_cases),
) -> EsporteResponse:
    atual = await use_cases.get(esporte_id)
    atualizado = replace(atual, **data.model_dump(exclude_unset=True))
    return EsporteResponse.model_validate(
        await use_cases.update_for_user(
            esporte_id, atualizado, user.id, user.is_superuser
        )
    )


@router.delete("/{esporte_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_esporte(
    esporte_id: UUID,
    user: UserModel = Depends(require_treinador),
    use_cases: EsporteUseCases = Depends(get_esporte_use_cases),
) -> Response:
    await use_cases.delete_for_user(esporte_id, user.id, user.is_superuser)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
