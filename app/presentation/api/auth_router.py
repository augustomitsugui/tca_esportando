from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import (
    AtletaModel,
    CoordenadorModel,
    RoleRequestModel,
    TreinadorModel,
    UserModel,
)
from app.infrastructure.database.session import get_db
from app.infrastructure.security.auth_backend import auth_backend
from app.infrastructure.security.user_manager import (
    current_active_user,
    fastapi_users,
)
from app.presentation.schemas.user import AuthMeResponse, UserCreate, UserRead

router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth/jwt", tags=["Auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), 
    prefix="/auth", tags=["Auth"]
)


@router.get("/auth/me", response_model=AuthMeResponse, tags=["Auth"])
async def get_authenticated_user(
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_db),
) -> AuthMeResponse:
    request = await session.scalar(
        select(RoleRequestModel)
        .where(RoleRequestModel.user_id == user.id)
        .order_by(RoleRequestModel.created_at.desc())
    )
    profile_id = None
    institution_id = None
    if user.role == "atleta":
        profile_id = await session.scalar(
            select(AtletaModel.id).where(AtletaModel.user_id == user.id)
        )
    elif user.role == "treinador":
        profile_id = await session.scalar(
            select(TreinadorModel.id).where(TreinadorModel.user_id == user.id)
        )
        institution_id = request.institution_id if request else None
    elif user.role == "coordenador":
        coordinator = await session.scalar(
            select(CoordenadorModel).where(CoordenadorModel.user_id == user.id)
        )
        if coordinator:
            profile_id = coordinator.id
            institution_id = coordinator.instituicao_id
    return AuthMeResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified,
        role=user.role,
        approval_status=request.status if request else None,
        institution_id=institution_id,
        profile_id=profile_id,
    )
