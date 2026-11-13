from dataclasses import replace
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.atleta import AtletaDTO
from app.application.use_cases.atleta import AtletaUseCases
from app.infrastructure.database.models import UserModel
from app.presentation.dependencies import (
    get_atleta_use_cases,
    require_atleta,
)
from app.core.exceptions import Forbidden
from app.presentation.schemas.atleta import (
    AtletaCreate,
    AtletaResponse,
    AtletaUpdate,
)

router = APIRouter(prefix="/atletas", tags=["Atletas"])


@router.post("", response_model=AtletaResponse, status_code=status.HTTP_201_CREATED)
async def criar_atleta(
    data: AtletaCreate,
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
) -> AtletaResponse:
    atleta = await use_cases.create(AtletaDTO(user_id=user.id, **data.model_dump()))
    return AtletaResponse.model_validate(atleta)


@router.get("", response_model=list[AtletaResponse])
async def listar_atletas(
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
) -> list[AtletaResponse]:
    return [
        AtletaResponse.model_validate(item)
        for item in await use_cases.list_for_user(user.id, user.is_superuser)
    ]


@router.get("/{atleta_id}", response_model=AtletaResponse)
async def obter_atleta(
    atleta_id: UUID,
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
) -> AtletaResponse:
    return AtletaResponse.model_validate(
        await use_cases.get_for_user(atleta_id, user.id, user.is_superuser)
    )


@router.put("/{atleta_id}", response_model=AtletaResponse)
async def atualizar_atleta(
    atleta_id: UUID,
    data: AtletaUpdate,
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
) -> AtletaResponse:
    atual = await use_cases.get(atleta_id)
    if not user.is_superuser and atual.user_id != user.id:
        raise Forbidden("Você só pode alterar seu próprio perfil.")
    atualizado = replace(atual, **data.model_dump(exclude_unset=True))
    return AtletaResponse.model_validate(await use_cases.update(atleta_id, atualizado))


@router.delete("/{atleta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_atleta(
    atleta_id: UUID,
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaUseCases = Depends(get_atleta_use_cases),
) -> Response:
    atual = await use_cases.get(atleta_id)
    if not user.is_superuser and atual.user_id != user.id:
        raise Forbidden("Você só pode excluir seu próprio perfil.")
    await use_cases.delete(atleta_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
