from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.dtos.role_request import (
    RoleRequestCreateDTO,
    RoleRequestDecisionDTO,
)
from app.application.use_cases.role_request import RoleRequestUseCases
from app.infrastructure.database.models import UserModel
from app.infrastructure.security.user_manager import current_active_user
from app.presentation.dependencies import (
    get_role_request_use_cases,
    require_coordenador,
    require_superadmin,
)
from app.presentation.schemas.role_request import (
    RoleRequestCreate,
    RoleRequestDecision,
    RoleRequestResponse,
)

router = APIRouter(prefix="/role-requests", tags=["Solicitações de cargo"])


@router.post(
    "",
    response_model=RoleRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def solicitar_cargo(
    data: RoleRequestCreate,
    user: UserModel = Depends(current_active_user),
    use_cases: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> RoleRequestResponse:
    request = await use_cases.request(
        user.id,
        RoleRequestCreateDTO(
            requested_role=data.requested_role,
            institution_id=data.institution_id,
            institution_name=data.institution_name,
            institution_description=data.institution_description,
            institution_latitude=data.institution_latitude,
            institution_longitude=data.institution_longitude,
        ),
    )
    return RoleRequestResponse.model_validate(request)


@router.get("/me", response_model=list[RoleRequestResponse])
async def minhas_solicitacoes(
    user: UserModel = Depends(current_active_user),
    use_cases: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> list[RoleRequestResponse]:
    requests = await use_cases.list_my_requests(user.id)
    return [RoleRequestResponse.model_validate(item) for item in requests]


@router.get(
    "/pending/coordinator",
    response_model=list[RoleRequestResponse],
)
async def solicitacoes_para_coordenador(
    _user: UserModel = Depends(require_coordenador),
    use_cases: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> list[RoleRequestResponse]:
    requests = await use_cases.list_for_coordinator(_user.id)
    return [RoleRequestResponse.model_validate(item) for item in requests]


@router.get(
    "/coordinator/history",
    response_model=list[RoleRequestResponse],
)
async def historico_para_coordenador(
    _user: UserModel = Depends(require_coordenador),
    use_cases: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> list[RoleRequestResponse]:
    requests = await use_cases.list_coordinator_history(_user.id)
    return [RoleRequestResponse.model_validate(item) for item in requests]


@router.get(
    "/pending/superadmin",
    response_model=list[RoleRequestResponse],
)
async def solicitacoes_para_superadmin(
    _user: UserModel = Depends(require_superadmin),
    use_cases: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> list[RoleRequestResponse]:
    requests = await use_cases.list_for_superadmin()
    return [RoleRequestResponse.model_validate(item) for item in requests]


@router.post(
    "/{request_id}/approve",
    response_model=RoleRequestResponse,
)
async def aprovar_solicitacao(
    request_id: UUID,
    user: UserModel = Depends(current_active_user),
    use_cases: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> RoleRequestResponse:
    request = await use_cases.approve(
        request_id,
        user.id,
        user.is_superuser,
    )
    return RoleRequestResponse.model_validate(request)


@router.post(
    "/{request_id}/reject",
    response_model=RoleRequestResponse,
)
async def rejeitar_solicitacao(
    request_id: UUID,
    data: RoleRequestDecision,
    user: UserModel = Depends(current_active_user),
    use_cases: RoleRequestUseCases = Depends(get_role_request_use_cases),
) -> RoleRequestResponse:
    request = await use_cases.reject(
        request_id,
        user.id,
        user.is_superuser,
        RoleRequestDecisionDTO(rejection_reason=data.rejection_reason),
    )
    return RoleRequestResponse.model_validate(request)
