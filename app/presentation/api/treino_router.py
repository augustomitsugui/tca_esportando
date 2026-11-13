from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.treino import TreinoCreateDTO, TreinoUpdateDTO
from app.application.use_cases.treino import TreinoUseCases
from app.presentation.dependencies import get_treino_use_cases
from app.presentation.schemas.treino import (
    TreinoAgendaResponse,
    TreinoCreate,
    TreinoResponse,
    TreinoUpdate,
)

router = APIRouter(tags=["Treinos"])


@router.post(
    "/treinos",
    response_model=TreinoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_treino(
    data: TreinoCreate,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> TreinoResponse:
    treino = await use_cases.create(TreinoCreateDTO(**data.model_dump()))
    return TreinoResponse.model_validate(treino)


@router.get("/treinos", response_model=list[TreinoResponse])
async def listar_treinos(
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> list[TreinoResponse]:
    return [
        TreinoResponse.model_validate(item)
        for item in await use_cases.list_all()
    ]


@router.get("/treinos/{treino_id}", response_model=TreinoResponse)
async def obter_treino(
    treino_id: UUID,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> TreinoResponse:
    return TreinoResponse.model_validate(await use_cases.get(treino_id))


@router.put("/treinos/{treino_id}", response_model=TreinoResponse)
async def atualizar_treino(
    treino_id: UUID,
    data: TreinoUpdate,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> TreinoResponse:
    treino = await use_cases.update(
        treino_id, TreinoUpdateDTO(**data.model_dump())
    )
    return TreinoResponse.model_validate(treino)


@router.delete("/treinos/{treino_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_treino(
    treino_id: UUID,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> Response:
    await use_cases.delete(treino_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/atletas/{atleta_id}/treinos",
    response_model=list[TreinoResponse],
)
async def listar_treinos_do_atleta(
    atleta_id: UUID,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> list[TreinoResponse]:
    return [
        TreinoResponse.model_validate(item)
        for item in await use_cases.list_by_atleta(atleta_id)
    ]


@router.get(
    "/atletas/{atleta_id}/proximos-treinos",
    response_model=list[TreinoAgendaResponse],
)
async def listar_proximos_treinos_do_atleta(
    atleta_id: UUID,
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> list[TreinoAgendaResponse]:
    return [
        TreinoAgendaResponse.model_validate(item)
        for item in await use_cases.list_upcoming_by_atleta(atleta_id)
    ]
