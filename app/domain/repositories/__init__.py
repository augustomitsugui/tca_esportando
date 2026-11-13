from .atleta import AtletaRepository
from .treinador import TreinadorRepository
from .coordenador import CoordenadorRepository
from .esporte import EsporteRepository
from .local import LocalRepository
from .user import UserRepository
from .atleta_esporte import AtletaEsporteRepository
from .base import BaseRepository
from .esporte_treinador import EsporteTreinadorRepository
from .instituicao import InstituicaoRepository
from .local_instituicao import LocalInstituicaoRepository
from .local_esporte import LocalEsporteRepository
from .treino import TreinoRepository

__all__ = [
    "AtletaRepository",
    "AtletaEsporteRepository",
    "TreinadorRepository",
    "CoordenadorRepository",
    "EsporteRepository",
    "LocalRepository",
    "UserRepository",
    "BaseRepository",
    "EsporteTreinadorRepository",
    "InstituicaoRepository",
    "LocalInstituicaoRepository",
    "LocalEsporteRepository",
    "TreinoRepository",
]
