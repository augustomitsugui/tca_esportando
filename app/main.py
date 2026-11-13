from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationError
from app.presentation.api.auth_router import router as auth_router
from app.presentation.api.atleta_router import router as atleta_router
from app.presentation.api.coordenador_router import router as coordenador_router
from app.presentation.api.esporte_router import router as esporte_router
from app.presentation.api.instituicao_router import router as instituicao_router
from app.presentation.api.local_router import router as local_router
from app.presentation.api.local_instituicao_router import (
    router as local_instituicao_router,
)
from app.presentation.api.local_esporte_router import (
    router as local_esporte_router,
)
from app.presentation.api.treino_router import router as treino_router
from app.presentation.api.treinador_router import router as treinador_router
from app.presentation.api.role_request_router import router as role_request_router

app = FastAPI(
    title="FastAPI Base",
    description="Base modular para novos sistemas",
    version="1.0.0",
)
app.include_router(auth_router)
app.include_router(atleta_router)
app.include_router(coordenador_router)
app.include_router(esporte_router)
app.include_router(instituicao_router)
app.include_router(local_router)
app.include_router(local_instituicao_router)
app.include_router(local_esporte_router)
app.include_router(treino_router)
app.include_router(treinador_router)
app.include_router(role_request_router)



@app.exception_handler(ApplicationError)
async def application_error_handler(request: Request, exc: ApplicationError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/")
def health_check():
    return {"status": "ok"}
