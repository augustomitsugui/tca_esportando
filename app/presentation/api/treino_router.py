from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.dtos.treino import TreinoCreateDTO, TreinoUpdateDTO
from app.application.use_cases.treino import TreinoUseCases
from app.core.exceptions import Forbidden
from app.presentation.dependencies import get_treino_use_cases, require_atleta
from app.presentation.schemas.treino import (
    TreinoAgendaResponse,
    TreinoCreate,
    TreinoResponse,
    TreinoUpdate,
)
from app.presentation.dependencies import require_treinador
from app.infrastructure.database.models import UserModel

router = APIRouter(tags=["Treinos"])


@router.post(
    "/treinos",
    response_model=TreinoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_treino(
    data: TreinoCreate,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> TreinoResponse:
    dto = TreinoCreateDTO(**data.model_dump())
    treino = (
        await use_cases.create(dto)
        if user.is_superuser
        else await use_cases.create_for_user(dto, user.id)
    )
    return TreinoResponse.model_validate(treino)


@router.get("/treinos", response_model=list[TreinoResponse])
async def listar_treinos(
    user: UserModel = Depends(require_treinador),
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> list[TreinoResponse]:
    return [
        TreinoResponse.model_validate(item)
        for item in await use_cases.list_for_user(user.id, user.is_superuser)
    ]


@router.get("/treinos/{treino_id}", response_model=TreinoResponse)
async def obter_treino(
    treino_id: UUID,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> TreinoResponse:
    return TreinoResponse.model_validate(
        await use_cases.get_for_user(treino_id, user.id, user.is_superuser)
    )


@router.put("/treinos/{treino_id}", response_model=TreinoResponse)
async def atualizar_treino(
    treino_id: UUID,
    data: TreinoUpdate,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> TreinoResponse:
    dto = TreinoUpdateDTO(**data.model_dump())
    treino = (
        await use_cases.update(treino_id, dto)
        if user.is_superuser
        else await use_cases.update_for_user(treino_id, dto, user.id)
    )
    return TreinoResponse.model_validate(treino)


@router.delete("/treinos/{treino_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_treino(
    treino_id: UUID,
    user: UserModel = Depends(require_treinador),
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> Response:
    if user.is_superuser:
        await use_cases.delete(treino_id)
    else:
        await use_cases.delete_for_user(treino_id, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/atletas/{atleta_id}/treinos",
    response_model=list[TreinoResponse],
)
async def listar_treinos_do_atleta(
    atleta_id: UUID,
    user: UserModel = Depends(require_atleta),
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> list[TreinoResponse]:
    atleta = await use_cases.get_atleta_by_user(user.id)
    if atleta != atleta_id:
        raise Forbidden("Você só pode consultar seus próprios treinos.")
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
    user: UserModel = Depends(require_atleta),
    use_cases: TreinoUseCases = Depends(get_treino_use_cases),
) -> list[TreinoAgendaResponse]:
    atleta = await use_cases.get_atleta_by_user(user.id)
    if atleta != atleta_id:
        raise Forbidden("Você só pode consultar seus próprios treinos.")
    return [
        TreinoAgendaResponse.model_validate(item)
        for item in await use_cases.list_upcoming_by_atleta(atleta_id)
    ]
