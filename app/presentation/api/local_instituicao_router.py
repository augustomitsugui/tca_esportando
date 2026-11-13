from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from app.infrastructure.database.models import UserModel

from app.application.dtos.local_instituicao import LocalInstituicaoDTO
from app.application.use_cases.local_instituicao import LocalInstituicaoUseCases
from app.presentation.dependencies import get_local_instituicao_use_cases
from app.presentation.schemas.local_instituicao import (
    LocalInstituicaoResponse,
)
from app.presentation.dependencies import (
    require_coordenador,
)

router = APIRouter(tags=["LocalInstituicao"])


@router.post(
    "/locais/{local_id}/instituicoes/{instituicao_id}",
    response_model=LocalInstituicaoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def vincular_local_instituicao(
    local_id: UUID,
    instituicao_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> LocalInstituicaoResponse:
    vinculo = await use_cases.vincular(
        LocalInstituicaoDTO(local_id=local_id, instituicao_id=instituicao_id),
        user.id,
        user.is_superuser,
    )
    return LocalInstituicaoResponse.model_validate(vinculo)


@router.delete(
    "/locais/{local_id}/instituicoes/{instituicao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def desvincular_local_instituicao(
    local_id: UUID,
    instituicao_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> Response:
    await use_cases.desvincular(
        local_id, instituicao_id, user.id, user.is_superuser
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/locais/{local_id}/instituicoes",
    response_model=list[LocalInstituicaoResponse],
)
async def listar_instituicoes_do_local(
    local_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> list[LocalInstituicaoResponse]:
    vinculos = await use_cases.list_by_local_for_user(
        local_id, user.id, user.is_superuser
    )
    return [LocalInstituicaoResponse.model_validate(vinculo) for vinculo in vinculos]


@router.get(
    "/instituicoes/{instituicao_id}/locais",
    response_model=list[LocalInstituicaoResponse],
)
async def listar_locais_da_instituicao(
    instituicao_id: UUID,
    user: UserModel = Depends(require_coordenador),
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> list[LocalInstituicaoResponse]:
    vinculos = await use_cases.list_by_instituicao_for_user(
        instituicao_id, user.id, user.is_superuser
    )
    return [LocalInstituicaoResponse.model_validate(vinculo) for vinculo in vinculos]
