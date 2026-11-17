from abc import abstractmethod
from uuid import UUID

from app.domain.entities.instituicao import Instituicao
from app.domain.repositories.base import BaseRepository


class InstituicaoRepository(BaseRepository[Instituicao]):
    @abstractmethod
    async def get(self, entity_id: UUID) -> Instituicao | None:
        ...
    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Instituicao | None:
        ...

    @abstractmethod
    async def list_public(self) -> list[Instituicao]: ...

    @abstractmethod
    async def list_by_creator(self, user_id: UUID) -> list[Instituicao]: ...

    @abstractmethod
    async def coordinator_has_institution(self, user_id: UUID) -> bool: ...
