from abc import abstractmethod
from uuid import UUID

from app.domain.entities.instituicao import Instituicao
from app.domain.repositories.base import BaseRepository


class InstituicaoRepository(BaseRepository[Instituicao]):
    @abstractmethod
    async def get(self, entity_id: UUID) -> Instituicao | None:
        ...
