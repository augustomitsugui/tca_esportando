from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.local_instituicao import LocalInstituicao


class LocalInstituicaoRepository(ABC):
    @abstractmethod
    async def local_owned_by(self, local_id: UUID, user_id: UUID) -> bool: ...

    @abstractmethod
    async def institution_owned_by(
        self, institution_id: UUID, user_id: UUID
    ) -> bool: ...

    @abstractmethod
    async def vincular(self, vinculo: LocalInstituicao) -> LocalInstituicao:
        ...

    @abstractmethod
    async def desvincular(self, local_id: UUID, instituicao_id: UUID) -> None:
        ...

    @abstractmethod
    async def list_by_local(self, local_id: UUID) -> list[LocalInstituicao]:
        ...

    @abstractmethod
    async def list_by_instituicao(
        self, instituicao_id: UUID
    ) -> list[LocalInstituicao]:
        ...
