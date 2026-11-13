from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.instituicao import InstituicaoDTO
from app.application.use_cases.instituicao import InstituicaoUseCases
from app.presentation.dependencies import get_instituicao_use_cases
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
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> InstituicaoResponse:
    instituicao = await use_cases.create(InstituicaoDTO(**data.model_dump()))
    return InstituicaoResponse.model_validate(instituicao)


@router.get("", response_model=list[InstituicaoResponse])
async def list_instituicoes(
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> list[InstituicaoResponse]:
    instituicoes = await use_cases.list_all()
    return [InstituicaoResponse.model_validate(item) for item in instituicoes]


@router.get("/{instituicao_id}", response_model=InstituicaoResponse)
async def get_instituicao(
    instituicao_id: UUID,
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> InstituicaoResponse:
    instituicao = await use_cases.get(instituicao_id)
    return InstituicaoResponse.model_validate(instituicao)


@router.put("/{instituicao_id}", response_model=InstituicaoResponse)
async def update_instituicao(
    instituicao_id: UUID,
    data: InstituicaoUpdate,
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> InstituicaoResponse:
    instituicao = await use_cases.update(
        instituicao_id, InstituicaoDTO(**data.model_dump())
    )
    return InstituicaoResponse.model_validate(instituicao)


@router.delete("/{instituicao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instituicao(
    instituicao_id: UUID,
    use_cases: InstituicaoUseCases = Depends(get_instituicao_use_cases),
) -> Response:
    await use_cases.delete(instituicao_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
