from dataclasses import replace
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.coordenador import CoordenadorDTO
from app.application.use_cases.coordenador import CoordenadorUseCases
from app.infrastructure.database.models import UserModel
from app.infrastructure.security.user_manager import current_active_user
from app.presentation.dependencies import get_coordenador_use_cases
from app.presentation.schemas.coordenador import (
    CoordenadorCreate,
    CoordenadorResponse,
    CoordenadorUpdate,
)

router = APIRouter(prefix="/coordenadores", tags=["Coordenadores"])


@router.post("", response_model=CoordenadorResponse, status_code=status.HTTP_201_CREATED)
async def criar_coordenador(
    data: CoordenadorCreate,
    user: UserModel = Depends(current_active_user),
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> CoordenadorResponse:
    coordenador = await use_cases.create(
        CoordenadorDTO(user_id=user.id, **data.model_dump())
    )
    return CoordenadorResponse.model_validate(coordenador)


@router.get("", response_model=list[CoordenadorResponse])
async def listar_coordenadores(
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> list[CoordenadorResponse]:
    return [CoordenadorResponse.model_validate(item) for item in await use_cases.list_all()]


@router.get("/{coordenador_id}", response_model=CoordenadorResponse)
async def obter_coordenador(
    coordenador_id: UUID,
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> CoordenadorResponse:
    return CoordenadorResponse.model_validate(await use_cases.get(coordenador_id))


@router.put("/{coordenador_id}", response_model=CoordenadorResponse)
async def atualizar_coordenador(
    coordenador_id: UUID,
    data: CoordenadorUpdate,
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> CoordenadorResponse:
    atual = await use_cases.get(coordenador_id)
    atualizado = replace(atual, **data.model_dump(exclude_unset=True))
    return CoordenadorResponse.model_validate(await use_cases.update(coordenador_id, atualizado))


@router.delete("/{coordenador_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_coordenador(
    coordenador_id: UUID,
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> Response:
    await use_cases.delete(coordenador_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
