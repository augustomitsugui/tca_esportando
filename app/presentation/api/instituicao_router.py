from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from app.infrastructure.database.models import UserModel

from app.application.dtos.instituicao import InstituicaoDTO
from app.application.use_cases.instituicao import InstituicaoUseCases
from app.presentation.dependencies import get_instituicao_use_cases
from app.presentation.dependencies import (
    require_coordenador,
)
from app.presentation.schemas.instituicao import (
    InstituicaoCreate,
    InstituicaoResponse,
    InstituicaoUpdate,
)

router = APIRouter(prefix="/instituicoes", tags=["Instituicoes"])


@router.post(
    "",
    response_model=InstituicaoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_instituicao(
    data: InstituicaoCreate,
    user: UserModel = Depends(require_coordenador),
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> InstituicaoResponse:
    instituicao = await use_cases.create(
        InstituicaoDTO(**data.model_dump()), user.id
    )
    return InstituicaoResponse.model_validate(instituicao)


@router.get("", response_model=list[InstituicaoResponse])
async def list_instituicoes(
    user: UserModel = Depends(require_coordenador),
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> list[InstituicaoResponse]:
    instituicoes = await use_cases.list_for_user(user.id, user.is_superuser)
    return [InstituicaoResponse.model_validate(item) for item in instituicoes]


@router.get("/{instituicao_id}", response_model=InstituicaoResponse)
async def get_instituicao(
    instituicao_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> InstituicaoResponse:
    instituicao = await use_cases.get_for_user(
        instituicao_id, user.id, user.is_superuser
    )
    return InstituicaoResponse.model_validate(instituicao)


@router.put("/{instituicao_id}", response_model=InstituicaoResponse)
async def update_instituicao(
    instituicao_id: UUID,
    data: InstituicaoUpdate,
    user: UserModel = Depends(require_coordenador),
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> InstituicaoResponse:
    instituicao = await use_cases.update(
        instituicao_id,
        InstituicaoDTO(**data.model_dump()),
        user.id,
        user.is_superuser,
    )
    return InstituicaoResponse.model_validate(instituicao)


@router.delete("/{instituicao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instituicao(
    instituicao_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> Response:
    await use_cases.delete(instituicao_id, user.id, user.is_superuser)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
