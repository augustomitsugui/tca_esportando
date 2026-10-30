from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from back.app.core.exceptions import ApplicationError
from back.app.presentation.api.auth_router import router as auth_router

app = FastAPI(
    title="FastAPI Base",
    description="Base modular para novos sistemas",
    version="1.0.0",
)
app.include_router(auth_router)


@app.exception_handler(ApplicationError)
async def application_error_handler(request: Request, exc: ApplicationError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/")
def health_check():
    return {"status": "ok"}
