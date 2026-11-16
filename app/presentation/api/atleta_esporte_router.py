from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from app.presentation.schemas.treinador import TreinadorResumo

from app.application.use_cases.atleta_esporte import AtletaEsporteUseCases
from app.core.exceptions import InvalidReference
from app.domain.entities.atleta_esporte import AtletaEsporteStatus
from app.infrastructure.database.models import UserModel
from app.presentation.dependencies import (
    get_atleta_esporte_use_cases,
    require_atleta,
    require_treinador,
)
from app.presentation.schemas.atleta_esporte import (
    AtletaEsporteDecision,
    AtletaEsporteResponse,
)
from app.presentation.schemas.esporte import EsporteResumo

router = APIRouter(tags=["Atleta-Esporte"])

@router.get(
    "/atletas/me/esportes/{esporte_id}/treinadores",
    response_model=list[TreinadorResumo],
)
async def listar_treinadores_do_esporte(
    esporte_id: UUID,
    _user: UserModel = Depends(require_atleta),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> list[TreinadorResumo]:
    treinadores = await use_cases.listar_treinadores_do_esporte(esporte_id)
    return [TreinadorResumo.model_validate(t) for t in treinadores]

@router.get(
    "/atletas/me/esportes/disponiveis",
    response_model=list[EsporteResumo],
)
async def listar_esportes_disponiveis(
    _user: UserModel = Depends(require_atleta),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> list[EsporteResumo]:
    esportes = await use_cases.listar_esportes_disponiveis()
    return [EsporteResumo.model_validate(item) for item in esportes]


@router.post(
    "/atletas/me/esportes/{esporte_id}/solicitacoes",
    response_model=AtletaEsporteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def solicitar_vinculo(
    esporte_id: UUID,
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> AtletaEsporteResponse:
    atleta_id = await use_cases.get_atleta_id_by_user(user.id)
    vinculo = await use_cases.solicitar(atleta_id, esporte_id, user.id)
    return AtletaEsporteResponse.model_validate(vinculo)


@router.get(
    "/atletas/me/solicitacoes-esporte",
    response_model=list[AtletaEsporteResponse],
)
async def listar_solicitacoes(
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> list[AtletaEsporteResponse]:
    atleta_id = await use_cases.get_atleta_id_by_user(user.id)
    vinculos = await use_cases.listar_solicitacoes(atleta_id, user.id)
    return [AtletaEsporteResponse.model_validate(item) for item in vinculos]


@router.get(
    "/atletas/me/esportes",
    response_model=list[AtletaEsporteResponse],
)
async def listar_esportes_aprovados(
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> list[AtletaEsporteResponse]:
    atleta_id = await use_cases.get_atleta_id_by_user(user.id)
    vinculos = await use_cases.listar_aprovados(atleta_id, user.id)
    return [AtletaEsporteResponse.model_validate(item) for item in vinculos]


@router.delete(
    "/atletas/me/solicitacoes-esporte/{vinculo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancelar_solicitacao(
    vinculo_id: UUID,
    user: UserModel = Depends(require_atleta),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> Response:
    atleta_id = await use_cases.get_atleta_id_by_user(user.id)
    await use_cases.cancelar(vinculo_id, atleta_id, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/treinadores/me/solicitacoes-esporte",
    response_model=list[AtletaEsporteResponse],
)
async def listar_solicitacoes_do_treinador(
    user: UserModel = Depends(require_treinador),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> list[AtletaEsporteResponse]:
    vinculos = await use_cases.listar_pendentes_do_treinador(user.id)
    return [AtletaEsporteResponse.model_validate(item) for item in vinculos]


@router.get(
    "/treinadores/me/atletas",
    response_model=list[AtletaEsporteResponse],
)
async def listar_atletas_vinculados(
    user: UserModel = Depends(require_treinador),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> list[AtletaEsporteResponse]:
    vinculos = await use_cases.listar_atletas_do_treinador(user.id)
    return [AtletaEsporteResponse.model_validate(item) for item in vinculos]


@router.post(
    "/treinadores/me/solicitacoes-esporte/{vinculo_id}/decisao",
    response_model=AtletaEsporteResponse,
)
async def decidir_solicitacao(
    vinculo_id: UUID,
    data: AtletaEsporteDecision,
    user: UserModel = Depends(require_treinador),
    use_cases: AtletaEsporteUseCases = Depends(get_atleta_esporte_use_cases),
) -> AtletaEsporteResponse:
    if data.status not in (
        AtletaEsporteStatus.APROVADO,
        AtletaEsporteStatus.RECUSADO,
    ):
        raise InvalidReference("A decisão deve ser aprovada ou recusada.")
    vinculo = await use_cases.decidir(vinculo_id, user.id, data.status)
    return AtletaEsporteResponse.model_validate(vinculo)
