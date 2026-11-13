from app.domain.entities.user import UserIdentity
from app.domain.repositories.base import BaseRepository
from app.infrastructure.database.models import UserModel
from sqlalchemy import select
from uuid import UUID
from app.infrastructure.repositories.base import BaseRepositoryImpl

class UserRepositoryImpl(BaseRepositoryImpl[UserIdentity, UserModel]):

    @property
    def model_class(self) -> type[UserModel]:
        return UserModel

    def _to_entity(self, model: UserModel) -> UserIdentity:
        return UserIdentity(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            is_verified=model.is_verified,
            role=model.role,
        )

    def _to_model(self, entity: UserIdentity) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            role=entity.role,
        )

    async def buscar_por_email(self, email: str) -> UserIdentity | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return None if model is None else self._to_entity(model)