from .local import localDTO as LocalDTO
from .treinador import TreinadorDTO
from .coordenador import CoordenadorDTO as CoodenadorDTO
from .treino import TreinoCreateDTO, TreinoDTO, TreinoUpdateDTO
from .esporte import EsporteDTO
from .user import UserDTO
from .atleta_esporte import AtletaEsporteDTO
from .atleta import AtletaDTO
from .instituicao import InstituicaoDTO
from .local_instituicao import LocalInstituicaoDTO
from .role_request import RoleRequestCreateDTO, RoleRequestDecisionDTO

__all__ = [
    "LocalDTO",
    "TreinadorDTO",
    "CoodenadorDTO",
    "TreinoDTO",
    "TreinoCreateDTO",
    "TreinoUpdateDTO",
    "EsporteDTO",
    "UserDTO",
    "AtletaEsporteDTO",
    "AtletaDTO",
    "InstituicaoDTO",
    "LocalInstituicaoDTO",
    "RoleRequestCreateDTO",
    "RoleRequestDecisionDTO",
]