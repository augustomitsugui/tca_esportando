from .atleta import AtletaCreate, AtletaResponse, AtletaUpdate, AtletaResumo
from .coordenador import (
    CoordenadroResumo as CoordenadorResumo,
    CoordenadorCreate,
    CoordenadorResponse,
    CoordenadorUpdate,
)
from .esporte import EsporteCreate, EsporteResponse, EsporteUpdate, EsporteResumo
from .instituicao import InstituicaoCreate, InstituicaoResponse, InstituicaoUpdate
from .esporte_treinador import EsporteTreinadorCreate, EsporteTreinadorResponse, EsporteTreinadorUpdate, EsporteTreinadorResumo
from .local import LocalCreate, LocalResponse, LocalUpdate, LocalResumo
from .treinador import TreinadorCreate, TreinadorResponse, TreinadorUpdate, TreinadorResumo
from .local_instituicao import LocalInstituicaoCreate, LocalInstituicaoResponse

__all__ = [
    "AtletaCreate",
    "AtletaResponse",
    "AtletaUpdate",
    "AtletaResumo",
    "CoordenadorResumo",
    "CoordenadorCreate",
    "CoordenadorResponse",
    "CoordenadorUpdate",
    "EsporteCreate",
    "EsporteResponse",
    "EsporteUpdate",
    "EsporteResumo",
    "InstituicaoCreate",
    "InstituicaoResponse",
    "InstituicaoUpdate",
    "EsporteTreinadorCreate",
    "EsporteTreinadorResponse",
    "EsporteTreinadorUpdate",
    "EsporteTreinadorResumo",
    "LocalCreate",
    "LocalResponse",
    "LocalUpdate",
    "LocalResumo",
    "TreinadorCreate",
    "TreinadorResponse",
    "TreinadorUpdate",
    "TreinadorResumo",
    "LocalInstituicaoCreate",
    "LocalInstituicaoResponse"
]
