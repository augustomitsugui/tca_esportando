from dataclasses import replace
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.treinador import TreinadorDTO
from app.application.use_cases.treinador import TreinadorUseCases
from app.infrastructure.database.models import UserModel
from app.presentation.dependencies import get_treinador_use_cases, require_treinador
from app.core.exceptions import Forbidden
from app.presentation.schemas.treinador import (
    TreinadorCreate,
    TreinadorResponse,
    TreinadorUpdate,
)

router = APIRouter(prefix="/treinadores", tags=["Treinadores"])


@router.post("", response_model=TreinadorResponse, status_code=status.HTTP_201_CREATED)
async def criar_treinador(
    data: TreinadorCreate,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinadorUseCases = Depends(get_treinador_use_cases),
) -> TreinadorResponse:
    treinador = await use_cases.create(
        TreinadorDTO(user_id=user.id, **data.model_dump())
    )
    return TreinadorResponse.model_validate(treinador)


@router.get("", response_model=list[TreinadorResponse])
async def listar_treinadores(
    user: UserModel = Depends(require_treinador),
    use_cases: TreinadorUseCases = Depends(get_treinador_use_cases),
) -> list[TreinadorResponse]:
    return [
        TreinadorResponse.model_validate(item)
        for item in await use_cases.list_for_user(user.id, user.is_superuser)
    ]


@router.get("/{treinador_id}", response_model=TreinadorResponse)
async def obter_treinador(
    treinador_id: UUID,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinadorUseCases = Depends(get_treinador_use_cases),
) -> TreinadorResponse:
    return TreinadorResponse.model_validate(
        await use_cases.get_for_user(treinador_id, user.id, user.is_superuser)
    )


@router.put("/{treinador_id}", response_model=TreinadorResponse)
async def atualizar_treinador(
    treinador_id: UUID,
    data: TreinadorUpdate,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinadorUseCases = Depends(get_treinador_use_cases),
) -> TreinadorResponse:
    atual = await use_cases.get(treinador_id)
    if not user.is_superuser and atual.user_id != user.id:
        raise Forbidden("Você só pode alterar seu próprio perfil.")
    atualizado = replace(atual, **data.model_dump(exclude_unset=True))
    return TreinadorResponse.model_validate(await use_cases.update(treinador_id, atualizado))


@router.delete("/{treinador_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_treinador(
    treinador_id: UUID,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinadorUseCases = Depends(get_treinador_use_cases),
) -> Response:
    atual = await use_cases.get(treinador_id)
    if not user.is_superuser and atual.user_id != user.id:
        raise Forbidden("Você só pode excluir seu próprio perfil.")
    await use_cases.delete(treinador_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
