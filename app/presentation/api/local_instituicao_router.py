from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.local_instituicao import LocalInstituicaoDTO
from app.application.use_cases.local_instituicao import LocalInstituicaoUseCases
from app.presentation.dependencies import get_local_instituicao_use_cases
from app.presentation.schemas.local_instituicao import (
    LocalInstituicaoResponse,
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
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> LocalInstituicaoResponse:
    vinculo = await use_cases.vincular(
        LocalInstituicaoDTO(local_id=local_id, instituicao_id=instituicao_id)
    )
    return LocalInstituicaoResponse.model_validate(vinculo)


@router.delete(
    "/locais/{local_id}/instituicoes/{instituicao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def desvincular_local_instituicao(
    local_id: UUID,
    instituicao_id: UUID,
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> Response:
    await use_cases.desvincular(local_id, instituicao_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/locais/{local_id}/instituicoes",
    response_model=list[LocalInstituicaoResponse],
)
async def listar_instituicoes_do_local(
    local_id: UUID,
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> list[LocalInstituicaoResponse]:
    vinculos = await use_cases.list_by_local(local_id)
    return [LocalInstituicaoResponse.model_validate(vinculo) for vinculo in vinculos]


@router.get(
    "/instituicoes/{instituicao_id}/locais",
    response_model=list[LocalInstituicaoResponse],
)
async def listar_locais_da_instituicao(
    instituicao_id: UUID,
    use_cases: LocalInstituicaoUseCases = Depends(
        get_local_instituicao_use_cases
    ),
) -> list[LocalInstituicaoResponse]:
    vinculos = await use_cases.list_by_instituicao(instituicao_id)
    return [LocalInstituicaoResponse.model_validate(vinculo) for vinculo in vinculos]
