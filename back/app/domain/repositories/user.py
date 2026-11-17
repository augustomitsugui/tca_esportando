from app.domain.entities.user import UserIdentity
from app.domain.repositories.base import BaseRepository
from uuid import UUID


class UserRepository(BaseRepository[UserIdentity]):
    async def buscar_por_email(self, email: str) -> UserIdentity | None:
        raise NotImplementedError
