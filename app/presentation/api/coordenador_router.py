from dataclasses import replace
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.coordenador import CoordenadorDTO
from app.application.use_cases.coordenador import CoordenadorUseCases
from app.infrastructure.database.models import UserModel
from app.presentation.dependencies import (
    get_coordenador_use_cases,
    get_role_request_use_cases,
    require_coordenador,
)
from app.infrastructure.security.user_manager import current_active_user
from app.application.use_cases.role_request import RoleRequestUseCases
from app.core.exceptions import Forbidden
from app.presentation.schemas.coordenador import (
    CoordenadorCreate,
    CoordenadorResponse,
    CoordenadorUpdate,
)

router = APIRouter(prefix="/coordenadores", tags=["Coordenadores"])


@router.post("", response_model=CoordenadorResponse, status_code=status.HTTP_201_CREATED)
async def criar_coordenador(
    data: CoordenadorCreate,
    user: UserModel = Depends(require_coordenador),
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
    role_requests: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> CoordenadorResponse:
    await role_requests.validate_coordinator_institution(
        user.id, data.instituicao_id
    )
    coordenador = await use_cases.create(
        CoordenadorDTO(user_id=user.id, **data.model_dump())
    )
    return CoordenadorResponse.model_validate(coordenador)


@router.get("", response_model=list[CoordenadorResponse])
async def listar_coordenadores(
    user: UserModel = Depends(current_active_user),
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> list[CoordenadorResponse]:
    return [
        CoordenadorResponse.model_validate(item)
        for item in await use_cases.list_for_user(user.id, user.is_superuser)
    ]


@router.get("/{coordenador_id}", response_model=CoordenadorResponse)
async def obter_coordenador(
    coordenador_id: UUID,
    user: UserModel = Depends(current_active_user),
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> CoordenadorResponse:
    return CoordenadorResponse.model_validate(
        await use_cases.get_for_user(
            coordenador_id, user.id, user.is_superuser
        )
    )


@router.put("/{coordenador_id}", response_model=CoordenadorResponse)
async def atualizar_coordenador(
    coordenador_id: UUID,
    data: CoordenadorUpdate,
    user: UserModel = Depends(require_coordenador),
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> CoordenadorResponse:
    atual = await use_cases.get(coordenador_id)
    if atual.user_id != user.id:
        raise Forbidden("Você só pode alterar seu próprio perfil.")
    atualizado = replace(atual, **data.model_dump(exclude_unset=True))
    return CoordenadorResponse.model_validate(await use_cases.update(coordenador_id, atualizado))


@router.delete("/{coordenador_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_coordenador(
    coordenador_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: CoordenadorUseCases = Depends(get_coordenador_use_cases),
) -> Response:
    atual = await use_cases.get(coordenador_id)
    if atual.user_id != user.id:
        raise Forbidden("Você só pode excluir seu próprio perfil.")
    await use_cases.delete(coordenador_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
