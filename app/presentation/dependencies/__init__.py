from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.application.use_cases import (
    AtletaUseCases,
    CoordenadorUseCases,
    EsporteUseCases,
    InstituicaoUseCases,
    LocalEsporteUseCases,
    LocalInstituicaoUseCases,
    LocalUseCases,
    TreinoUseCases,
    TreinadorUseCases,
    RoleRequestUseCases,
    AtletaEsporteUseCases,
)
from app.domain.entities.user import UserRole
from app.core.exceptions import Forbidden
from app.domain.services.auth_service import AuthService
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import RoleRequestModel, UserModel
from app.domain.entities.user import RoleRequestStatus
from app.infrastructure.repositories import (
    AtletaRepositoryImpl,
    CoordenadorRepositoryImpl,
    EsporteRepositoryImpl,
    EsporteTreinadorRepositoryImpl,
    InstituicaoRepositoryImpl,
    LocalEsporteRepositoryImpl,
    LocalInstituicaoRepositoryImpl,
    LocalRepositoryImpl,
    TreinoRepositoryImpl,
    TreinadorRepositoryImpl,
    RoleRequestRepositoryImpl,
    AtletaEsporteRepositoryImpl,
)
from app.infrastructure.security.user_manager import current_active_user


def get_instituicao_use_cases(
    session: AsyncSession = Depends(get_db),
) -> InstituicaoUseCases:
    return InstituicaoUseCases(InstituicaoRepositoryImpl(session))


def get_local_instituicao_use_cases(
    session: AsyncSession = Depends(get_db),
) -> LocalInstituicaoUseCases:
    return LocalInstituicaoUseCases(LocalInstituicaoRepositoryImpl(session))


def get_local_esporte_use_cases(
    session: AsyncSession = Depends(get_db),
) -> LocalEsporteUseCases:
    return LocalEsporteUseCases(LocalEsporteRepositoryImpl(session))


def get_treino_use_cases(
    session: AsyncSession = Depends(get_db),
) -> TreinoUseCases:
    return TreinoUseCases(TreinoRepositoryImpl(session))


def get_atleta_use_cases(
    session: AsyncSession = Depends(get_db),
) -> AtletaUseCases:
    return AtletaUseCases(AtletaRepositoryImpl(session))


def get_treinador_use_cases(
    session: AsyncSession = Depends(get_db),
) -> TreinadorUseCases:
    return TreinadorUseCases(TreinadorRepositoryImpl(session))


def get_coordenador_use_cases(
    session: AsyncSession = Depends(get_db),
) -> CoordenadorUseCases:
    return CoordenadorUseCases(CoordenadorRepositoryImpl(session))


def get_esporte_use_cases(
    session: AsyncSession = Depends(get_db),
) -> EsporteUseCases:
    return EsporteUseCases(
        EsporteRepositoryImpl(session),
        EsporteTreinadorRepositoryImpl(session),
    )


def get_local_use_cases(
    session: AsyncSession = Depends(get_db),
) -> LocalUseCases:
    return LocalUseCases(LocalRepositoryImpl(session))


def get_role_request_use_cases(
    session: AsyncSession = Depends(get_db),
) -> RoleRequestUseCases:
    return RoleRequestUseCases(RoleRequestRepositoryImpl(session))


def get_atleta_esporte_use_cases(
    session: AsyncSession = Depends(get_db),
) -> AtletaEsporteUseCases:
    return AtletaEsporteUseCases(
        AtletaEsporteRepositoryImpl(session)
    )


class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        user: UserModel = Depends(current_active_user),
        session: AsyncSession = Depends(get_db),
    ) -> UserModel:
        if user.is_superuser:
            return user
        AuthService.ensure_role(user.role, self.allowed_roles)
        if user.role in (UserRole.TREINADOR.value, UserRole.COORDENADOR.value):
            approved = await session.scalar(
                select(RoleRequestModel.id).where(
                    RoleRequestModel.user_id == user.id,
                    RoleRequestModel.requested_role == user.role,
                    RoleRequestModel.status == RoleRequestStatus.APROVADA.value,
                )
            )
            if approved is None:
                raise Forbidden("Seu perfil ainda aguarda aprovação.")
        return user


requer_coordenador = RoleChecker([UserRole.COORDENADOR])
requer_treinador = RoleChecker([UserRole.TREINADOR])
requer_atleta = RoleChecker([UserRole.ATLETA])
async def require_superadmin(
    user: UserModel = Depends(current_active_user),
) -> UserModel:
    if not user.is_superuser:
        raise Forbidden("Apenas o Super Admin pode executar esta ação.")
    return user


require_atleta = requer_atleta
require_treinador = requer_treinador
require_coordenador = requer_coordenador
