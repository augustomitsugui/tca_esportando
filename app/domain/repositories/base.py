from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
# isso aqui serve pra eu nao ficar repetindo o mesmo codigo de repository em 
# todos os repositorios, pq todos vao ter esses metodos basicos!!


class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None: ...

    @abstractmethod
    async def list_all(self) -> list[T]: ...

    @abstractmethod
    async def delete(self, entity_id: int) -> bool: ...
    
    @abstractmethod
    async def update(self, entity: T) -> T: ...
