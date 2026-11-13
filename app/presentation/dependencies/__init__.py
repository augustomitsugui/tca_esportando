from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
)
from app.domain.entities.user import UserRole
from app.domain.services.auth_service import AuthService
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import UserModel
from app.infrastructure.repositories import (
    AtletaRepositoryImpl,
    CoordenadorRepositoryImpl,
    EsporteRepositoryImpl,
    InstituicaoRepositoryImpl,
    LocalEsporteRepositoryImpl,
    LocalInstituicaoRepositoryImpl,
    LocalRepositoryImpl,
    TreinoRepositoryImpl,
    TreinadorRepositoryImpl,
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
    return EsporteUseCases(EsporteRepositoryImpl(session))


def get_local_use_cases(
    session: AsyncSession = Depends(get_db),
) -> LocalUseCases:
    return LocalUseCases(LocalRepositoryImpl(session))


class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserModel = Depends(current_active_user)) -> UserModel:
        AuthService.ensure_role(user.role, self.allowed_roles)
        return user


requer_coordenador = RoleChecker([UserRole.COORDENADOR])
requer_professor = RoleChecker([UserRole.TREINADOR])
requer_professor_ou_coordenador = RoleChecker(
    [UserRole.TREINADOR, UserRole.COORDENADOR]
)
