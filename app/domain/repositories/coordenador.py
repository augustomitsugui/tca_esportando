from abc import abstractmethod

from app.domain.entities.coordenador import Coordenador
from app.domain.repositories.base import BaseRepository

class CoordenadorRepository(BaseRepository[Coordenador]):
    pass
    
