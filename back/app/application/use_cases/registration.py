from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidReference
from app.domain.entities.user import RoleRequestRole, RoleRequestStatus, UserRole
from app.infrastructure.database.models import (
    AtletaModel,
    CoordenadorModel,
    InstituicaoModel,
    RoleRequestModel,
    TreinadorModel,
    UserModel,
)
from app.infrastructure.security.password_hasher import password_helper
from app.presentation.schemas.registration import (
    AthleteRegistration,
    CoordinatorRegistration,
    TrainerRegistration,
)


class RegistrationUseCases:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def athlete(self, data: AthleteRegistration) -> UserModel:
        user = UserModel(
            email=str(data.email),
            hashed_password=password_helper.hash(data.password),
            role=UserRole.ATLETA.value,
        )
        try:
            async with self.session.begin():
                self.session.add(user)
                await self.session.flush()
                self.session.add(
                    AtletaModel(
                        user_id=user.id,
                        nome=data.nome,
                        email=str(data.email),
                        ano=data.ano,
                        bio=data.bio,
                    )
                )
        except IntegrityError as exc:
            raise InvalidReference("O email já está cadastrado.") from exc
        await self.session.refresh(user)
        return user

    async def trainer(self, data: TrainerRegistration) -> UserModel:
        user = UserModel(
            email=str(data.email),
            hashed_password=password_helper.hash(data.password),
            role=UserRole.TREINADOR.value,
        )
        try:
            institution = await self.session.get(
                InstituicaoModel, data.institution_id
            )
            if institution is None:
                raise InvalidReference("A instituição selecionada não existe.")
            self.session.add(user)
            await self.session.flush()
            self.session.add(
                TreinadorModel(
                    user_id=user.id,
                    nome=data.nome,
                    email=str(data.email),
                    bio=data.bio,
                )
            )
            self.session.add(
                RoleRequestModel(
                    user_id=user.id,
                    requested_role=RoleRequestRole.TREINADOR.value,
                    status=RoleRequestStatus.PENDENTE.value,
                    institution_id=institution.id,
                )
            )
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise InvalidReference("O email já está cadastrado.") from exc
        await self.session.refresh(user)
        return user

    async def coordinator(self, data: CoordinatorRegistration) -> UserModel:
        if not data.institution_name.strip():
            raise InvalidReference("O nome da instituição é obrigatório.")
        user = UserModel(
            email=str(data.email),
            hashed_password=password_helper.hash(data.password),
            role=UserRole.COORDENADOR.value,
        )
        try:
            async with self.session.begin():
                self.session.add(user)
                await self.session.flush()
                self.session.add(
                    CoordenadorModel(
                        user_id=user.id,
                        instituicao_id=None,
                        nome=data.nome,
                        email=str(data.email),
                        bio=data.bio,
                    )
                )
                self.session.add(
                    RoleRequestModel(
                        user_id=user.id,
                        requested_role=RoleRequestRole.COORDENADOR.value,
                        status=RoleRequestStatus.PENDENTE.value,
                        institution_name=data.institution_name.strip(),
                        institution_description=data.institution_description,
                        institution_latitude=data.institution_latitude,
                        institution_longitude=data.institution_longitude,
                    )
                )
        except IntegrityError as exc:
            raise InvalidReference("O email já está cadastrado.") from exc
        await self.session.refresh(user)
        return user
