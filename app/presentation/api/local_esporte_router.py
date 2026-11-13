from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.application.use_cases.local_esporte import LocalEsporteUseCases
from app.presentation.schemas.esporte import EsporteResumo
from app.presentation.schemas.local import LocalResumo
from app.presentation.dependencies import get_local_esporte_use_cases

router = APIRouter(tags=["Local-Esporte"])


@router.post(
    "/locais/{local_id}/esportes/{esporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def vincular_esporte_ao_local(
    local_id: UUID,
    esporte_id: UUID,
    use_cases: LocalEsporteUseCases = Depends(get_local_esporte_use_cases),
) -> Response:
    await use_cases.add(local_id, esporte_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/locais/{local_id}/esportes/{esporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def desvincular_esporte_do_local(
    local_id: UUID,
    esporte_id: UUID,
    use_cases: LocalEsporteUseCases = Depends(get_local_esporte_use_cases),
) -> Response:
    await use_cases.remove(local_id, esporte_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/locais/{local_id}/esportes",
    response_model=list[EsporteResumo],
)
async def listar_esportes_do_local(
    local_id: UUID,
    use_cases: LocalEsporteUseCases = Depends(get_local_esporte_use_cases),
) -> list[EsporteResumo]:
    return [
        EsporteResumo.model_validate(item)
        for item in await use_cases.list_by_local(local_id)
    ]


@router.get(
    "/esportes/{esporte_id}/locais",
    response_model=list[LocalResumo],
)
async def listar_locais_do_esporte(
    esporte_id: UUID,
    use_cases: LocalEsporteUseCases = Depends(get_local_esporte_use_cases),
) -> list[LocalResumo]:
    return [
        LocalResumo.model_validate(item)
        for item in await use_cases.list_by_esporte(esporte_id)
    ]
