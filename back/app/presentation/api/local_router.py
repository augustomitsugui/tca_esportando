from dataclasses import replace
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.local import LocalDTO
from app.application.use_cases.local import LocalUseCases
from app.presentation.dependencies import get_local_use_cases
from app.presentation.dependencies import (
    require_coordenador,
    require_treinador,
)
from app.infrastructure.database.models import UserModel
from app.presentation.schemas.local import LocalCreate, LocalResponse, LocalUpdate

router = APIRouter(prefix="/locais", tags=["Locais"])
trainer_router = APIRouter(prefix="/treinadores", tags=["Locais"])


@trainer_router.get(
    "/me/locais",
    response_model=list[LocalResponse],
)
async def listar_locais_do_treinador(
    user: UserModel = Depends(require_treinador),
    use_cases: LocalUseCases = Depends(get_local_use_cases),
) -> list[LocalResponse]:
    locais = await use_cases.list_by_treinador_user(user.id)
    return [LocalResponse.model_validate(item) for item in locais]


@router.post("", response_model=LocalResponse, status_code=status.HTTP_201_CREATED)
async def criar_local(
    data: LocalCreate,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalUseCases = Depends(get_local_use_cases),
) -> LocalResponse:
    local = await use_cases.create(LocalDTO(**data.model_dump()), user.id)
    return LocalResponse.model_validate(local)


@router.get("", response_model=list[LocalResponse])
async def listar_locais(
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalUseCases = Depends(get_local_use_cases),
) -> list[LocalResponse]:
    return [
        LocalResponse.model_validate(item)
        for item in await use_cases.list_for_user(user.id, user.is_superuser)
    ]


@router.get("/{local_id}", response_model=LocalResponse)
async def obter_local(
    local_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalUseCases = Depends(get_local_use_cases),
) -> LocalResponse:
    return LocalResponse.model_validate(
        await use_cases.get_for_user(local_id, user.id, user.is_superuser)
    )


@router.put("/{local_id}", response_model=LocalResponse)
async def atualizar_local(
    local_id: UUID,
    data: LocalUpdate,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalUseCases = Depends(get_local_use_cases),
) -> LocalResponse:
    atual = await use_cases.get(local_id)
    atualizado = replace(atual, **data.model_dump(exclude_unset=True))
    return LocalResponse.model_validate(
        await use_cases.update_for_user(local_id, atualizado, user.id, user.is_superuser)
    )


@router.delete("/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_local(
    local_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalUseCases = Depends(get_local_use_cases),
) -> Response:
    await use_cases.delete_for_user(local_id, user.id, user.is_superuser)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
